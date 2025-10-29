"""
Technical indicators service for stock analysis.
"""
import pandas as pd
import pandas_ta as ta
import streamlit as st
from typing import Dict
import numpy as np


@st.cache_data(ttl=3600)  # Cache for 1 hour
def calculate_moving_averages(data: pd.DataFrame, periods: list = [20, 50, 200]) -> Dict:
    """Calculate moving averages for given periods.
    
    Args:
        data: DataFrame with stock data
        periods: List of periods for moving averages
    
    Returns:
        Dictionary with moving average values
    """
    try:
        result = {}
        for period in periods:
            if len(data) >= period:
                ma = data['Close'].rolling(window=period).mean().iloc[-1]
                result[f"MA_{period}"] = round(ma, 2)
            else:
                result[f"MA_{period}"] = None
        
        return result
    except Exception as e:
        print(f"Error calculating moving averages: {e}")
        return {f"MA_{p}": None for p in periods}


@st.cache_data(ttl=3600)
def calculate_rsi(data: pd.DataFrame, period: int = 14) -> Dict:
    """Calculate Relative Strength Index (RSI).
    
    Args:
        data: DataFrame with stock data
        period: RSI period (default: 14)
    
    Returns:
        Dictionary with RSI values
    """
    try:
        if len(data) < period:
            return {"current": None, "overbought": 70, "oversold": 30}
        
        rsi = ta.rsi(data['Close'], length=period)
        current_rsi = rsi.iloc[-1]
        
        return {
            "current": round(current_rsi, 2),
            "overbought": 70,
            "oversold": 30,
            "signal": "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral"
        }
    except Exception as e:
        print(f"Error calculating RSI: {e}")
        return {"current": None, "overbought": 70, "oversold": 30, "signal": "N/A"}


@st.cache_data(ttl=3600)
def calculate_macd(data: pd.DataFrame) -> Dict:
    """Calculate MACD (Moving Average Convergence Divergence).
    
    Args:
        data: DataFrame with stock data
    
    Returns:
        Dictionary with MACD values
    """
    try:
        if len(data) < 26:
            return {"macd": None, "signal": None, "histogram": None}
        
        macd_data = ta.macd(data['Close'])
        
        if macd_data is None or macd_data.empty:
            return {"macd": None, "signal": None, "histogram": None}
        
        macd_line = macd_data[f'MACD_12_26_9'].iloc[-1]
        signal_line = macd_data[f'MACDs_12_26_9'].iloc[-1]
        histogram = macd_data[f'MACDh_12_26_9'].iloc[-1]
        
        return {
            "macd": round(macd_line, 2),
            "signal": round(signal_line, 2),
            "histogram": round(histogram, 2),
            "trend": "Bullish" if histogram > 0 else "Bearish"
        }
    except Exception as e:
        print(f"Error calculating MACD: {e}")
        return {"macd": None, "signal": None, "histogram": None, "trend": "N/A"}


@st.cache_data(ttl=3600)
def calculate_pivot_points(data: pd.DataFrame) -> Dict:
    """Calculate pivot points for support and resistance levels.
    
    Args:
        data: DataFrame with stock data
    
    Returns:
        Dictionary with pivot points
    """
    try:
        if len(data) < 1:
            return {}
        
        # Use last day's data
        high = data['High'].iloc[-1]
        low = data['Low'].iloc[-1]
        close = data['Close'].iloc[-1]
        
        # Calculate pivot point
        pivot = (high + low + close) / 3
        
        # Calculate support and resistance levels
        r1 = 2 * pivot - low
        r2 = pivot + (high - low)
        r3 = high + 2 * (pivot - low)
        
        s1 = 2 * pivot - high
        s2 = pivot - (high - low)
        s3 = low - 2 * (high - pivot)
        
        return {
            "pivot": round(pivot, 2),
            "resistance_1": round(r1, 2),
            "resistance_2": round(r2, 2),
            "resistance_3": round(r3, 2),
            "support_1": round(s1, 2),
            "support_2": round(s2, 2),
            "support_3": round(s3, 2)
        }
    except Exception as e:
        print(f"Error calculating pivot points: {e}")
        return {}


@st.cache_data(ttl=3600)
def calculate_support_resistance(data: pd.DataFrame) -> Dict:
    """Calculate support and resistance levels based on pivot points.
    
    Args:
        data: DataFrame with stock data
    
    Returns:
        Dictionary with support and resistance levels
    """
    try:
        pivot_points = calculate_pivot_points(data)
        
        if not pivot_points:
            return {"support_levels": [], "resistance_levels": []}
        
        support_levels = [
            pivot_points.get("support_1"),
            pivot_points.get("support_2"),
            pivot_points.get("support_3")
        ]
        
        resistance_levels = [
            pivot_points.get("resistance_1"),
            pivot_points.get("resistance_2"),
            pivot_points.get("resistance_3")
        ]
        
        return {
            "support_levels": [s for s in support_levels if s is not None],
            "resistance_levels": [r for r in resistance_levels if r is not None]
        }
    except Exception as e:
        print(f"Error calculating support/resistance: {e}")
        return {"support_levels": [], "resistance_levels": []}


@st.cache_data(ttl=3600)
def calculate_all_indicators(data: pd.DataFrame) -> Dict:
    """Calculate all technical indicators at once.
    
    Args:
        data: DataFrame with stock data
    
    Returns:
        Dictionary with all indicators
    """
    return {
        "moving_averages": calculate_moving_averages(data),
        "rsi": calculate_rsi(data),
        "macd": calculate_macd(data),
        "pivot_points": calculate_pivot_points(data),
        "support_resistance": calculate_support_resistance(data)
    }
