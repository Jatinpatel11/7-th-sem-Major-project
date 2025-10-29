"""
Data service for fetching stock market data from Yahoo Finance.
"""
import yfinance as yf
import pandas as pd
import streamlit as st
from typing import Dict, Optional
from datetime import datetime
import requests
from src.services.exceptions import (
    InvalidSymbolError,
    APIRateLimitError,
    NetworkError,
    DataNotAvailableError
)


# Symbol mapping for common Indian stock names
STOCK_SYMBOL_MAP = {
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "hdfc bank": "HDFCBANK.NS",
    "hdfcbank": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS",
    "icicibank": "ICICIBANK.NS",
    "wipro": "WIPRO.NS",
    "bharti airtel": "BHARTIARTL.NS",
    "airtel": "BHARTIARTL.NS",
    "itc": "ITC.NS",
    "sbi": "SBIN.NS",
    "state bank": "SBIN.NS",
    "axis bank": "AXISBANK.NS",
    "axisbank": "AXISBANK.NS",
    "maruti": "MARUTI.NS",
    "asian paints": "ASIANPAINT.NS",
    "asianpaint": "ASIANPAINT.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "bajfinance": "BAJFINANCE.NS",
    "hul": "HINDUNILVR.NS",
    "hindustan unilever": "HINDUNILVR.NS",
    "nifty 50": "^NSEI",
    "nifty": "^NSEI",
    "nifty50": "^NSEI",
    "bank nifty": "^NSEBANK",
    "banknifty": "^NSEBANK",
    "sensex": "^BSESN",
}


def format_indian_stock_symbol(name: str) -> str:
    """Format stock name to proper Indian stock symbol.
    
    Args:
        name: Stock name or symbol
        
    Returns:
        Formatted symbol with .NS or .BO suffix, or index symbol
    """
    name_lower = name.lower().strip()
    
    # Check if it's in our mapping
    if name_lower in STOCK_SYMBOL_MAP:
        return STOCK_SYMBOL_MAP[name_lower]
    
    # If already has .NS or .BO suffix, return as is
    if name.upper().endswith('.NS') or name.upper().endswith('.BO'):
        return name.upper()
    
    # If it starts with ^, it's likely an index
    if name.startswith('^'):
        return name.upper()
    
    # Default to NSE (.NS) for Indian stocks
    return f"{name.upper()}.NS"


@st.cache_data(ttl=3600)  # Cache for 1 hour for historical data
def get_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """Fetch historical stock data from Yahoo Finance.
    
    Args:
        symbol: Stock symbol (will be formatted for Indian stocks)
        period: Time period for historical data (default: 1y)
                Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    
    Returns:
        DataFrame with historical stock data
        
    Raises:
        InvalidSymbolError: If symbol is invalid or not found
        NetworkError: If network connectivity issues occur
        DataNotAvailableError: If no data is available
    """
    try:
        formatted_symbol = format_indian_stock_symbol(symbol)
        stock = yf.Ticker(formatted_symbol)
        data = stock.history(period=period)
        
        if data.empty:
            raise DataNotAvailableError(f"No data available for symbol: {formatted_symbol}")
        
        return data
    
    except requests.exceptions.ConnectionError:
        raise NetworkError("Network connection issue. Please check your internet connection.")
    except requests.exceptions.Timeout:
        raise NetworkError("Request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise APIRateLimitError("Rate limit exceeded. Please try again in a few minutes.")
        raise InvalidSymbolError(f"Invalid stock symbol: {symbol}")
    except DataNotAvailableError:
        raise
    except Exception as e:
        print(f"Error fetching stock data for {symbol}: {e}")
        raise InvalidSymbolError(f"Unable to fetch data for symbol: {symbol}")


@st.cache_data(ttl=300)  # Cache for 5 minutes for real-time data
def get_current_price(symbol: str) -> Dict:
    """Fetch current price and key metrics for a stock.
    
    Args:
        symbol: Stock symbol (will be formatted for Indian stocks)
    
    Returns:
        Dictionary with current price data
        
    Raises:
        InvalidSymbolError: If symbol is invalid or not found
        NetworkError: If network connectivity issues occur
        DataNotAvailableError: If no data is available
    """
    try:
        formatted_symbol = format_indian_stock_symbol(symbol)
        stock = yf.Ticker(formatted_symbol)
        
        # Get current data
        info = stock.info
        hist = stock.history(period="1d")
        
        if hist.empty:
            raise DataNotAvailableError(f"No current data available for symbol: {formatted_symbol}")
        
        current_price = hist['Close'].iloc[-1]
        day_high = hist['High'].iloc[-1]
        day_low = hist['Low'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        
        # Calculate percentage change
        if len(hist) > 1:
            prev_close = hist['Close'].iloc[-2]
        else:
            prev_close = info.get('previousClose', current_price)
        
        change_percent = ((current_price - prev_close) / prev_close) * 100 if prev_close else 0
        
        return {
            "symbol": formatted_symbol,
            "name": info.get('longName', formatted_symbol),
            "current_price": round(current_price, 2),
            "day_high": round(day_high, 2),
            "day_low": round(day_low, 2),
            "volume": int(volume),
            "change_percent": round(change_percent, 2),
            "currency": "INR",
            "timestamp": datetime.now().isoformat()
        }
    
    except requests.exceptions.ConnectionError:
        raise NetworkError("Network connection issue. Please check your internet connection.")
    except requests.exceptions.Timeout:
        raise NetworkError("Request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise APIRateLimitError("Rate limit exceeded. Please try again in a few minutes.")
        raise InvalidSymbolError(f"Invalid stock symbol: {symbol}")
    except DataNotAvailableError:
        raise
    except Exception as e:
        print(f"Error fetching current price for {symbol}: {e}")
        raise InvalidSymbolError(f"Unable to fetch data for symbol: {symbol}")


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_stock_info(symbol: str) -> Dict:
    """Fetch additional stock information and metadata.
    
    Args:
        symbol: Stock symbol (will be formatted for Indian stocks)
    
    Returns:
        Dictionary with stock information
        
    Raises:
        InvalidSymbolError: If symbol is invalid or not found
        NetworkError: If network connectivity issues occur
    """
    try:
        formatted_symbol = format_indian_stock_symbol(symbol)
        stock = yf.Ticker(formatted_symbol)
        info = stock.info
        
        return {
            "symbol": formatted_symbol,
            "name": info.get('longName', formatted_symbol),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "market_cap": info.get('marketCap', 0),
            "pe_ratio": info.get('trailingPE', 0),
            "dividend_yield": info.get('dividendYield', 0),
            "52_week_high": info.get('fiftyTwoWeekHigh', 0),
            "52_week_low": info.get('fiftyTwoWeekLow', 0),
            "currency": "INR"
        }
    
    except requests.exceptions.ConnectionError:
        raise NetworkError("Network connection issue. Please check your internet connection.")
    except requests.exceptions.Timeout:
        raise NetworkError("Request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise APIRateLimitError("Rate limit exceeded. Please try again in a few minutes.")
        raise InvalidSymbolError(f"Invalid stock symbol: {symbol}")
    except Exception as e:
        print(f"Error fetching stock info for {symbol}: {e}")
        raise InvalidSymbolError(f"Unable to fetch data for symbol: {symbol}")


def clear_cache():
    """Clear all cached data for refresh functionality."""
    st.cache_data.clear()


def format_inr(amount: float) -> str:
    """Format amount in Indian Rupee format.
    
    Args:
        amount: Amount to format
    
    Returns:
        Formatted string with INR symbol
    """
    if amount >= 10000000:  # 1 Crore
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh
        return f"₹{amount/100000:.2f} L"
    elif amount >= 1000:
        return f"₹{amount/1000:.2f} K"
    else:
        return f"₹{amount:.2f}"
