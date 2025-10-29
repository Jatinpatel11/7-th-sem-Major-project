"""
Unit tests for data service.
"""
import pytest
from unittest.mock import Mock, patch
import pandas as pd
from src.services.data_service import (
    format_indian_stock_symbol,
    format_inr,
    get_stock_data,
    get_current_price,
    get_stock_info
)
from src.services.exceptions import (
    InvalidSymbolError,
    DataNotAvailableError,
    NetworkError
)


def test_format_indian_stock_symbol_common_names():
    """Test symbol formatting for common stock names."""
    assert format_indian_stock_symbol("reliance") == "RELIANCE.NS"
    assert format_indian_stock_symbol("TCS") == "TCS.NS"
    assert format_indian_stock_symbol("Nifty 50") == "^NSEI"
    assert format_indian_stock_symbol("Bank Nifty") == "^NSEBANK"
    assert format_indian_stock_symbol("Sensex") == "^BSESN"


def test_format_indian_stock_symbol_with_suffix():
    """Test that symbols with .NS or .BO are returned as-is."""
    assert format_indian_stock_symbol("RELIANCE.NS") == "RELIANCE.NS"
    assert format_indian_stock_symbol("TCS.BO") == "TCS.BO"


def test_format_indian_stock_symbol_default():
    """Test default NSE suffix for unknown symbols."""
    assert format_indian_stock_symbol("UNKNOWN") == "UNKNOWN.NS"
    assert format_indian_stock_symbol("TEST") == "TEST.NS"


def test_format_inr_crores():
    """Test INR formatting for crores."""
    assert format_inr(15000000) == "₹1.50 Cr"
    assert format_inr(100000000) == "₹10.00 Cr"


def test_format_inr_lakhs():
    """Test INR formatting for lakhs."""
    assert format_inr(500000) == "₹5.00 L"
    assert format_inr(1500000) == "₹15.00 L"


def test_format_inr_thousands():
    """Test INR formatting for thousands."""
    assert format_inr(5000) == "₹5.00 K"
    assert format_inr(50000) == "₹50.00 K"


def test_format_inr_small_amounts():
    """Test INR formatting for small amounts."""
    assert format_inr(500) == "₹500.00"
    assert format_inr(99.99) == "₹99.99"


@patch('src.services.data_service.yf.Ticker')
def test_get_stock_data_success(mock_ticker):
    """Test successful stock data retrieval."""
    # Mock data
    mock_data = pd.DataFrame({
        'Open': [100, 101, 102],
        'High': [105, 106, 107],
        'Low': [95, 96, 97],
        'Close': [102, 103, 104],
        'Volume': [1000000, 1100000, 1200000]
    })
    
    mock_instance = Mock()
    mock_instance.history.return_value = mock_data
    mock_ticker.return_value = mock_instance
    
    result = get_stock_data("RELIANCE")
    
    assert result is not None
    assert len(result) == 3
    assert 'Close' in result.columns


@patch('src.services.data_service.yf.Ticker')
def test_get_stock_data_empty_data(mock_ticker):
    """Test handling of empty data."""
    mock_instance = Mock()
    mock_instance.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_instance
    
    with pytest.raises(DataNotAvailableError):
        get_stock_data("INVALID")


@patch('src.services.data_service.yf.Ticker')
def test_get_current_price_success(mock_ticker):
    """Test successful current price retrieval."""
    # Mock data
    mock_hist = pd.DataFrame({
        'Close': [100, 102],
        'High': [105, 107],
        'Low': [95, 97],
        'Volume': [1000000, 1100000]
    })
    
    mock_info = {
        'longName': 'Reliance Industries',
        'previousClose': 100
    }
    
    mock_instance = Mock()
    mock_instance.history.return_value = mock_hist
    mock_instance.info = mock_info
    mock_ticker.return_value = mock_instance
    
    result = get_current_price("RELIANCE")
    
    assert result is not None
    assert result['current_price'] == 102
    assert result['day_high'] == 107
    assert result['day_low'] == 97
    assert result['volume'] == 1100000
    assert result['currency'] == 'INR'
    assert 'change_percent' in result


@patch('src.services.data_service.yf.Ticker')
def test_get_current_price_percentage_change(mock_ticker):
    """Test percentage change calculation."""
    mock_hist = pd.DataFrame({
        'Close': [100, 110],
        'High': [105, 115],
        'Low': [95, 105],
        'Volume': [1000000, 1100000]
    })
    
    mock_info = {'longName': 'Test Stock', 'previousClose': 100}
    
    mock_instance = Mock()
    mock_instance.history.return_value = mock_hist
    mock_instance.info = mock_info
    mock_ticker.return_value = mock_instance
    
    result = get_current_price("TEST")
    
    # 10% increase from 100 to 110
    assert result['change_percent'] == 10.0


@patch('src.services.data_service.yf.Ticker')
def test_get_stock_info_success(mock_ticker):
    """Test successful stock info retrieval."""
    mock_info = {
        'longName': 'Reliance Industries Limited',
        'sector': 'Energy',
        'industry': 'Oil & Gas',
        'marketCap': 1500000000000,
        'trailingPE': 25.5,
        'dividendYield': 0.005,
        'fiftyTwoWeekHigh': 2800,
        'fiftyTwoWeekLow': 2000
    }
    
    mock_instance = Mock()
    mock_instance.info = mock_info
    mock_ticker.return_value = mock_instance
    
    result = get_stock_info("RELIANCE")
    
    assert result is not None
    assert result['name'] == 'Reliance Industries Limited'
    assert result['sector'] == 'Energy'
    assert result['industry'] == 'Oil & Gas'
    assert result['currency'] == 'INR'
    assert result['52_week_high'] == 2800
    assert result['52_week_low'] == 2000
