"""
Prediction service for stock price forecasting using LSTM models.
"""
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.services.data_service import get_stock_data, format_indian_stock_symbol


class PredictionService:
    """Service for predicting stock prices using LSTM models."""
    
    def __init__(self, models_dir: str = "models"):
        """Initialize the prediction service.
        
        Args:
            models_dir: Directory containing pre-trained models
        """
        self.models_dir = models_dir
        self.lookback_window = 60
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def load_model(self, stock_symbol: str) -> Optional[keras.Model]:
        """Load pre-trained model for a stock symbol.
        
        Args:
            stock_symbol: Stock symbol to load model for
        
        Returns:
            Loaded Keras model or None if not found
        """
        try:
            # Format symbol for filename
            symbol_clean = stock_symbol.replace('.', '_').replace('^', '')
            model_path = os.path.join(self.models_dir, f"{symbol_clean}_lstm.h5")
            
            if os.path.exists(model_path):
                return keras.models.load_model(model_path)
            
            # Try general model as fallback
            general_model_path = os.path.join(self.models_dir, "general_model.h5")
            if os.path.exists(general_model_path):
                return keras.models.load_model(general_model_path)
            
            return None
        
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    def prepare_data(self, historical_data: pd.DataFrame) -> tuple:
        """Prepare historical data for prediction.
        
        Args:
            historical_data: DataFrame with historical stock data
        
        Returns:
            Tuple of (scaled_data, scaler, original_data)
        """
        # Use closing prices
        data = historical_data['Close'].values.reshape(-1, 1)
        
        # Scale data
        scaled_data = self.scaler.fit_transform(data)
        
        return scaled_data, self.scaler, data
    
    def create_sequences(self, data: np.ndarray, lookback: int) -> np.ndarray:
        """Create sequences for LSTM input.
        
        Args:
            data: Scaled data array
            lookback: Number of previous timesteps to use
        
        Returns:
            Array of sequences
        """
        sequences = []
        for i in range(lookback, len(data)):
            sequences.append(data[i-lookback:i, 0])
        
        return np.array(sequences)
    
    def predict_prices(self, symbol: str, days: int = 5) -> Optional[Dict]:
        """Generate price predictions for the next N days.
        
        Args:
            symbol: Stock symbol
            days: Number of days to predict (1-5)
        
        Returns:
            Dictionary with predictions and metadata
        """
        try:
            # Get historical data
            historical_data = get_stock_data(symbol, period="1y")
            if historical_data is None or len(historical_data) < self.lookback_window:
                return None
            
            # Prepare data
            scaled_data, scaler, original_data = self.prepare_data(historical_data)
            
            # Load model (or use simple regression as fallback)
            formatted_symbol = format_indian_stock_symbol(symbol)
            model = self.load_model(formatted_symbol)
            
            if model is None:
                # Use simple linear regression as fallback
                return self._simple_prediction(original_data, days)
            
            # Make predictions
            predictions = []
            current_sequence = scaled_data[-self.lookback_window:].copy()
            
            for _ in range(days):
                # Reshape for model input
                X = current_sequence.reshape(1, self.lookback_window, 1)
                
                # Predict next value
                pred_scaled = model.predict(X, verbose=0)[0, 0]
                predictions.append(pred_scaled)
                
                # Update sequence for next prediction
                current_sequence = np.append(current_sequence[1:], [[pred_scaled]], axis=0)
            
            # Inverse transform predictions
            predictions_array = np.array(predictions).reshape(-1, 1)
            predictions_actual = scaler.inverse_transform(predictions_array).flatten()
            
            # Generate prediction dates
            last_date = historical_data.index[-1]
            prediction_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') 
                               for i in range(days)]
            
            # Calculate confidence intervals (±5%)
            confidence_lower = predictions_actual * 0.95
            confidence_upper = predictions_actual * 1.05
            
            return {
                "predictions": [round(p, 2) for p in predictions_actual],
                "dates": prediction_dates,
                "confidence_interval": {
                    "lower": [round(l, 2) for l in confidence_lower],
                    "upper": [round(u, 2) for u in confidence_upper]
                },
                "historical_actual": original_data[-30:].flatten().tolist(),
                "historical_dates": [d.strftime('%Y-%m-%d') for d in historical_data.index[-30:]],
                "model_type": "LSTM"
            }
        
        except Exception as e:
            print(f"Error predicting prices: {e}")
            return None
    
    def _simple_prediction(self, data: np.ndarray, days: int) -> Dict:
        """Simple linear regression prediction as fallback.
        
        Args:
            data: Historical price data
            days: Number of days to predict
        
        Returns:
            Dictionary with predictions
        """
        # Use last 30 days for trend
        recent_data = data[-30:].flatten()
        
        # Calculate simple linear trend
        x = np.arange(len(recent_data))
        coeffs = np.polyfit(x, recent_data, 1)
        
        # Predict future values
        future_x = np.arange(len(recent_data), len(recent_data) + days)
        predictions = np.polyval(coeffs, future_x)
        
        # Generate dates
        prediction_dates = [(datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d') 
                           for i in range(days)]
        
        # Confidence intervals (±7% for simple model)
        confidence_lower = predictions * 0.93
        confidence_upper = predictions * 1.07
        
        return {
            "predictions": [round(p, 2) for p in predictions],
            "dates": prediction_dates,
            "confidence_interval": {
                "lower": [round(l, 2) for l in confidence_lower],
                "upper": [round(u, 2) for u in confidence_upper]
            },
            "historical_actual": recent_data.tolist(),
            "historical_dates": [(datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d') 
                                for i in range(len(recent_data))],
            "model_type": "Linear Regression (Fallback)"
        }


# Global instance
prediction_service = PredictionService()


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_price_predictions(symbol: str, days: int = 5) -> Optional[Dict]:
    """Get cached price predictions for a stock.
    
    Args:
        symbol: Stock symbol
        days: Number of days to predict
    
    Returns:
        Prediction results
    """
    return prediction_service.predict_prices(symbol, days)
