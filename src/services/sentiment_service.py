"""
Sentiment analysis service using VADER for financial text analysis.
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
from datetime import datetime
import streamlit as st
from src.services.news_fetcher import fetch_news


class SentimentService:
    """Service for analyzing sentiment from financial news and text."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of a single text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary with sentiment scores and category
        """
        try:
            scores = self.analyzer.polarity_scores(text)
            
            # Determine category based on compound score
            compound = scores['compound']
            if compound >= 0.05:
                category = "Positive"
            elif compound <= -0.05:
                category = "Negative"
            else:
                category = "Neutral"
            
            return {
                "compound": compound,
                "positive": scores['pos'],
                "neutral": scores['neu'],
                "negative": scores['neg'],
                "category": category
            }
        
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {
                "compound": 0.0,
                "positive": 0.0,
                "neutral": 1.0,
                "negative": 0.0,
                "category": "Neutral"
            }
    
    def get_overall_sentiment(self, stock_name: str, news_limit: int = 15) -> Dict:
        """Get overall sentiment from multiple news sources.
        
        Args:
            stock_name: Name of the stock to analyze
            news_limit: Maximum number of news articles to analyze
        
        Returns:
            Dictionary with overall sentiment analysis results
        """
        try:
            # Fetch news
            news_list = fetch_news(stock_name, limit=news_limit)
            
            if not news_list:
                return self._neutral_sentiment("No news available")
            
            # Analyze each news article
            sentiments = []
            positive_count = 0
            neutral_count = 0
            negative_count = 0
            
            for i, news in enumerate(news_list):
                # Combine title and description for analysis
                text = f"{news['title']} {news.get('description', '')}"
                sentiment = self.analyze_sentiment(text)
                
                # Weight recent news more heavily (exponential decay)
                weight = 1.0 / (1 + i * 0.1)  # More recent = higher weight
                sentiment['weight'] = weight
                sentiments.append(sentiment)
                
                # Count categories
                if sentiment['category'] == "Positive":
                    positive_count += 1
                elif sentiment['category'] == "Negative":
                    negative_count += 1
                else:
                    neutral_count += 1
            
            # Calculate weighted average
            total_weight = sum(s['weight'] for s in sentiments)
            weighted_score = sum(s['compound'] * s['weight'] for s in sentiments) / total_weight
            
            # Determine overall category
            if weighted_score >= 0.05:
                overall_category = "Positive"
            elif weighted_score <= -0.05:
                overall_category = "Negative"
            else:
                overall_category = "Neutral"
            
            # Calculate confidence (based on consistency of sentiments)
            if sentiments:
                avg_abs_deviation = sum(abs(s['compound'] - weighted_score) for s in sentiments) / len(sentiments)
                confidence = max(0.0, min(1.0, 1.0 - avg_abs_deviation))
            else:
                confidence = 0.0
            
            return {
                "overall_score": round(weighted_score, 3),
                "category": overall_category,
                "confidence": round(confidence, 2),
                "sources_analyzed": len(news_list),
                "breakdown": {
                    "positive": positive_count,
                    "neutral": neutral_count,
                    "negative": negative_count
                },
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"Error getting overall sentiment: {e}")
            return self._neutral_sentiment("Error analyzing sentiment")
    
    def _neutral_sentiment(self, reason: str = "") -> Dict:
        """Return neutral sentiment as fallback.
        
        Args:
            reason: Reason for neutral sentiment
        
        Returns:
            Dictionary with neutral sentiment
        """
        return {
            "overall_score": 0.0,
            "category": "Neutral",
            "confidence": 0.0,
            "sources_analyzed": 0,
            "breakdown": {
                "positive": 0,
                "neutral": 0,
                "negative": 0
            },
            "timestamp": datetime.now().isoformat(),
            "note": reason
        }


# Global instance
sentiment_service = SentimentService()


@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_sentiment_analysis(stock_name: str) -> Dict:
    """Get cached sentiment analysis for a stock.
    
    Args:
        stock_name: Name of the stock
    
    Returns:
        Sentiment analysis results
    """
    return sentiment_service.get_overall_sentiment(stock_name)
