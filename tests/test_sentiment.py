"""
Unit tests for sentiment analysis service.
"""
import pytest
from unittest.mock import Mock, patch
from src.services.sentiment_service import SentimentService


@pytest.fixture
def sentiment_service():
    """Create a SentimentService instance for testing."""
    return SentimentService()


def test_analyze_sentiment_positive(sentiment_service):
    """Test positive sentiment detection."""
    text = "Stock reaches all-time high with strong fundamentals and excellent growth"
    result = sentiment_service.analyze_sentiment(text)
    
    assert result['category'] == "Positive"
    assert result['compound'] > 0
    assert result['positive'] > 0


def test_analyze_sentiment_negative(sentiment_service):
    """Test negative sentiment detection."""
    text = "Stock crashes amid terrible earnings and massive losses"
    result = sentiment_service.analyze_sentiment(text)
    
    assert result['category'] == "Negative"
    assert result['compound'] < 0
    assert result['negative'] > 0


def test_analyze_sentiment_neutral(sentiment_service):
    """Test neutral sentiment detection."""
    text = "The company released its quarterly report today"
    result = sentiment_service.analyze_sentiment(text)
    
    assert result['category'] == "Neutral"
    assert -0.05 <= result['compound'] <= 0.05


def test_analyze_sentiment_empty_text(sentiment_service):
    """Test handling of empty text."""
    result = sentiment_service.analyze_sentiment("")
    
    assert result is not None
    assert 'category' in result
    assert 'compound' in result


@patch('src.services.sentiment_service.fetch_news')
def test_get_overall_sentiment_positive(mock_fetch_news, sentiment_service):
    """Test overall sentiment with positive news."""
    mock_news = [
        {
            'title': 'Stock soars to new heights',
            'description': 'Excellent performance and strong growth',
            'published': '2025-10-28T10:00:00'
        },
        {
            'title': 'Company reports record profits',
            'description': 'Outstanding quarterly results',
            'published': '2025-10-28T09:00:00'
        }
    ]
    mock_fetch_news.return_value = mock_news
    
    result = sentiment_service.get_overall_sentiment("TestStock")
    
    assert result['category'] == "Positive"
    assert result['overall_score'] > 0
    assert result['sources_analyzed'] == 2
    assert result['breakdown']['positive'] > 0


@patch('src.services.sentiment_service.fetch_news')
def test_get_overall_sentiment_negative(mock_fetch_news, sentiment_service):
    """Test overall sentiment with negative news."""
    mock_news = [
        {
            'title': 'Stock plummets on bad news',
            'description': 'Terrible earnings and massive losses',
            'published': '2025-10-28T10:00:00'
        },
        {
            'title': 'Company faces crisis',
            'description': 'Awful situation with declining revenue',
            'published': '2025-10-28T09:00:00'
        }
    ]
    mock_fetch_news.return_value = mock_news
    
    result = sentiment_service.get_overall_sentiment("TestStock")
    
    assert result['category'] == "Negative"
    assert result['overall_score'] < 0
    assert result['sources_analyzed'] == 2
    assert result['breakdown']['negative'] > 0


@patch('src.services.sentiment_service.fetch_news')
def test_get_overall_sentiment_no_news(mock_fetch_news, sentiment_service):
    """Test handling when no news is available."""
    mock_fetch_news.return_value = []
    
    result = sentiment_service.get_overall_sentiment("TestStock")
    
    assert result['category'] == "Neutral"
    assert result['overall_score'] == 0.0
    assert result['sources_analyzed'] == 0
    assert 'note' in result


@patch('src.services.sentiment_service.fetch_news')
def test_get_overall_sentiment_mixed(mock_fetch_news, sentiment_service):
    """Test overall sentiment with mixed news."""
    mock_news = [
        {
            'title': 'Stock shows great performance',
            'description': 'Excellent growth',
            'published': '2025-10-28T10:00:00'
        },
        {
            'title': 'Company faces challenges',
            'description': 'Some difficulties ahead',
            'published': '2025-10-28T09:00:00'
        },
        {
            'title': 'Quarterly report released',
            'description': 'Company announces results',
            'published': '2025-10-28T08:00:00'
        }
    ]
    mock_fetch_news.return_value = mock_news
    
    result = sentiment_service.get_overall_sentiment("TestStock")
    
    assert result is not None
    assert result['sources_analyzed'] == 3
    assert result['breakdown']['positive'] + result['breakdown']['neutral'] + result['breakdown']['negative'] == 3


@patch('src.services.sentiment_service.fetch_news')
def test_sentiment_weighting(mock_fetch_news, sentiment_service):
    """Test that recent news is weighted more heavily."""
    # First news is very positive, second is slightly negative
    mock_news = [
        {
            'title': 'Amazing breakthrough and fantastic results',
            'description': 'Incredible performance',
            'published': '2025-10-28T10:00:00'
        },
        {
            'title': 'Minor setback',
            'description': 'Small issue',
            'published': '2025-10-28T08:00:00'
        }
    ]
    mock_fetch_news.return_value = mock_news
    
    result = sentiment_service.get_overall_sentiment("TestStock")
    
    # Overall should be positive since first (more recent) news is weighted higher
    assert result['overall_score'] > 0


def test_neutral_sentiment_fallback(sentiment_service):
    """Test neutral sentiment fallback."""
    result = sentiment_service._neutral_sentiment("Test reason")
    
    assert result['category'] == "Neutral"
    assert result['overall_score'] == 0.0
    assert result['confidence'] == 0.0
    assert result['sources_analyzed'] == 0
    assert result['note'] == "Test reason"
