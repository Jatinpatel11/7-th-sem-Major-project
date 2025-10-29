"""
Model trainer for creating placeholder LSTM models.
This script can be run separately to train models on historical data.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.services.lstm_model import create_lstm_model
from src.services.data_service import get_stock_data
import os


def create_training_data(data: np.ndarray, lookback: int = 60):
    """Create training sequences from historical data.
    
    Args:
        data: Scaled price data
        lookback: Number of previous days to use
    
    Returns:
        Tuple of (X_train, y_train)
    """
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i, 0])
        y.append(data[i, 0])
    
    return np.array(X), np.array(y)


def train_and_save_model(symbol: str, model_name: str, epochs: int = 50):
    """Train and save an LSTM model for a stock.
    
    Args:
        symbol: Stock symbol to train on
        model_name: Name to save the model as
        epochs: Number of training epochs
    """
    print(f"Training model for {symbol}...")
    
    # Get historical data
    data = get_stock_data(symbol, period="5y")
    if data is None or len(data) < 100:
        print(f"Insufficient data for {symbol}")
        return
    
    # Prepare data
    prices = data['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(prices)
    
    # Create training sequences
    X_train, y_train = create_training_data(scaled_data, lookback=60)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    
    # Create and train model
    model = create_lstm_model(lookback_window=60, features=1)
    
    print(f"Training on {len(X_train)} samples...")
    model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )
    
    # Save model
    os.makedirs("models", exist_ok=True)
    model_path = f"models/{model_name}.h5"
    model.save(model_path)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    # Train models for major indices
    print("Creating placeholder models...")
    print("Note: These are basic models. For production, train with more data and tuning.")
    
    # Create a simple general model
    try:
        train_and_save_model("^NSEI", "general_model", epochs=20)
        print("General model created successfully")
    except Exception as e:
        print(f"Error creating general model: {e}")
        print("Models will use linear regression fallback")
