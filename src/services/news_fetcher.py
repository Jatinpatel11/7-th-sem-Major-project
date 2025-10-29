"""
News fetcher module for retrieving financial news from various sources.
"""
import requests
from typing import List, Dict
from datetime import datetime, timedelta
import feedparser
from urllib.parse import quote


def fetch_google_news(stock_name: str, limit: int = 10) -> List[Dict]:
    """Fetch news from Google News RSS feed.
    
    Args:
        stock_name: Name of the stock or company
        limit: Maximum number of news articles to fetch
    
    Returns:
        List of news articles with title, description, link, and published date
    """
    try:
        # Google News RSS feed URL
        query = f"{stock_name} stock India"
        encoded_query = quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
        
        # Parse RSS feed
        feed = feedparser.parse(url)
        
        news_list = []
        cutoff_date = datetime.now() - timedelta(hours=48)  # Last 48 hours
        
        for entry in feed.entries[:limit]:
            try:
                # Parse published date
                published = datetime(*entry.published_parsed[:6])
                
                # Only include recent news
                if published < cutoff_date:
                    continue
                
                news_list.append({
                    'title': entry.title,
                    'description': entry.get('summary', entry.title),
                    'link': entry.link,
                    'published': published.isoformat(),
                    'source': 'Google News'
                })
            except Exception as e:
                print(f"Error parsing news entry: {e}")
                continue
        
        return news_list
    
    except Exception as e:
        print(f"Error fetching Google News: {e}")
        return []


def fetch_news(stock_name: str, limit: int = 10) -> List[Dict]:
    """Fetch financial news for a stock from available sources.
    
    Args:
        stock_name: Name of the stock or company
        limit: Maximum number of news articles to fetch
    
    Returns:
        List of news articles
    """
    news_list = []
    
    # Try Google News first
    google_news = fetch_google_news(stock_name, limit)
    news_list.extend(google_news)
    
    # Could add more sources here (NewsAPI, etc.) if API keys are available
    
    return news_list[:limit]


def filter_recent_news(news_list: List[Dict], hours: int = 48) -> List[Dict]:
    """Filter news to only include recent articles.
    
    Args:
        news_list: List of news articles
        hours: Number of hours to look back
    
    Returns:
        Filtered list of recent news articles
    """
    cutoff_date = datetime.now() - timedelta(hours=hours)
    recent_news = []
    
    for news in news_list:
        try:
            published = datetime.fromisoformat(news['published'])
            if published >= cutoff_date:
                recent_news.append(news)
        except Exception:
            # If date parsing fails, include the article anyway
            recent_news.append(news)
    
    return recent_news
