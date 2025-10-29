"""
Chart generation module using Plotly for interactive visualizations.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Optional


# Custom color theme
COLORS = {
    "primary": "#1abc9c",
    "secondary": "#16a085",
    "background": "#f8f9fa",
    "text": "#2c3e50",
    "positive": "#27ae60",
    "negative": "#e74c3c",
    "neutral": "#95a5a6"
}


def create_price_chart(data: pd.DataFrame, indicators: Optional[Dict] = None, 
                       title: str = "Stock Price History") -> go.Figure:
    """Create interactive price chart with technical indicators.
    
    Args:
        data: DataFrame with stock price data
        indicators: Dictionary with technical indicators
        title: Chart title
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price',
        increasing_line_color=COLORS['positive'],
        decreasing_line_color=COLORS['negative']
    ))
    
    # Add moving averages if provided
    if indicators and 'moving_averages' in indicators:
        mas = indicators['moving_averages']
        colors = ['#3498db', '#9b59b6', '#e67e22']
        
        for i, (period, value) in enumerate(mas.items()):
            if value is not None and period.startswith('MA_'):
                period_num = int(period.split('_')[1])
                if len(data) >= period_num:
                    ma_series = data['Close'].rolling(window=period_num).mean()
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=ma_series,
                        name=f'MA {period_num}',
                        line=dict(color=colors[i % len(colors)], width=2)
                    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        yaxis_title='Price (INR)',
        xaxis_title='Date',
        template='plotly_white',
        hovermode='x unified',
        height=500,
        font=dict(family="Inter, sans-serif", color=COLORS['text']),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor='white',
        xaxis_rangeslider_visible=False
    )
    
    return fig


def create_sentiment_gauge(sentiment: Dict) -> go.Figure:
    """Create sentiment gauge visualization.
    
    Args:
        sentiment: Dictionary with sentiment data
    
    Returns:
        Plotly Figure object
    """
    score = sentiment.get('overall_score', 0)
    category = sentiment.get('category', 'Neutral')
    
    # Normalize score to 0-100 scale
    gauge_value = (score + 1) * 50  # Convert from [-1, 1] to [0, 100]
    
    # Determine color based on category
    if category == "Positive":
        color = COLORS['positive']
    elif category == "Negative":
        color = COLORS['negative']
    else:
        color = COLORS['neutral']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=gauge_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Sentiment: {category}", 'font': {'size': 24}},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': COLORS['text']},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': COLORS['text'],
            'steps': [
                {'range': [0, 33], 'color': '#ffebee'},
                {'range': [33, 67], 'color': '#fff9e6'},
                {'range': [67, 100], 'color': '#e8f8f5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        font=dict(family="Inter, sans-serif", color=COLORS['text']),
        paper_bgcolor='white'
    )
    
    return fig


def create_prediction_chart(prediction_data: Dict) -> go.Figure:
    """Create price prediction chart comparing actual vs predicted prices.
    
    Args:
        prediction_data: Dictionary with prediction data
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Add historical actual prices
    if 'historical_actual' in prediction_data and 'historical_dates' in prediction_data:
        fig.add_trace(go.Scatter(
            x=prediction_data['historical_dates'],
            y=prediction_data['historical_actual'],
            name='Historical',
            line=dict(color=COLORS['primary'], width=2),
            mode='lines'
        ))
    
    # Add predictions
    if 'predictions' in prediction_data and 'dates' in prediction_data:
        fig.add_trace(go.Scatter(
            x=prediction_data['dates'],
            y=prediction_data['predictions'],
            name='Predicted',
            line=dict(color=COLORS['secondary'], width=2, dash='dash'),
            mode='lines+markers',
            marker=dict(size=8)
        ))
        
        # Add confidence interval
        if 'confidence_interval' in prediction_data:
            ci = prediction_data['confidence_interval']
            fig.add_trace(go.Scatter(
                x=prediction_data['dates'] + prediction_data['dates'][::-1],
                y=ci['upper'] + ci['lower'][::-1],
                fill='toself',
                fillcolor='rgba(26, 188, 156, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval',
                showlegend=True
            ))
    
    fig.update_layout(
        title='Price Prediction (Next 5 Days)',
        yaxis_title='Price (INR)',
        xaxis_title='Date',
        template='plotly_white',
        hovermode='x unified',
        height=400,
        font=dict(family="Inter, sans-serif", color=COLORS['text']),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor='white'
    )
    
    return fig


def create_technical_indicator_chart(indicator_name: str, data: pd.DataFrame, 
                                     indicator_data: Dict) -> go.Figure:
    """Create chart for technical indicators (RSI, MACD).
    
    Args:
        indicator_name: Name of the indicator ('RSI' or 'MACD')
        data: DataFrame with stock data
        indicator_data: Dictionary with indicator values
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    if indicator_name == 'RSI':
        # Calculate RSI series
        import pandas_ta as ta
        rsi_series = ta.rsi(data['Close'], length=14)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=rsi_series,
            name='RSI',
            line=dict(color=COLORS['primary'], width=2)
        ))
        
        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color=COLORS['negative'], 
                     annotation_text="Overbought")
        fig.add_hline(y=30, line_dash="dash", line_color=COLORS['positive'], 
                     annotation_text="Oversold")
        
        fig.update_layout(
            title='Relative Strength Index (RSI)',
            yaxis_title='RSI',
            yaxis_range=[0, 100]
        )
    
    elif indicator_name == 'MACD':
        # Calculate MACD series
        import pandas_ta as ta
        macd_data = ta.macd(data['Close'])
        
        if macd_data is not None and not macd_data.empty:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=macd_data['MACD_12_26_9'],
                name='MACD',
                line=dict(color=COLORS['primary'], width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=macd_data['MACDs_12_26_9'],
                name='Signal',
                line=dict(color=COLORS['secondary'], width=2)
            ))
            
            fig.add_trace(go.Bar(
                x=data.index,
                y=macd_data['MACDh_12_26_9'],
                name='Histogram',
                marker_color=COLORS['neutral']
            ))
        
        fig.update_layout(
            title='MACD (Moving Average Convergence Divergence)',
            yaxis_title='MACD'
        )
    
    fig.update_layout(
        xaxis_title='Date',
        template='plotly_white',
        hovermode='x unified',
        height=300,
        font=dict(family="Inter, sans-serif", color=COLORS['text']),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor='white'
    )
    
    return fig


def create_volume_chart(data: pd.DataFrame) -> go.Figure:
    """Create volume chart.
    
    Args:
        data: DataFrame with stock data
    
    Returns:
        Plotly Figure object
    """
    colors = [COLORS['positive'] if data['Close'].iloc[i] >= data['Open'].iloc[i] 
              else COLORS['negative'] for i in range(len(data))]
    
    fig = go.Figure(data=[go.Bar(
        x=data.index,
        y=data['Volume'],
        marker_color=colors,
        name='Volume'
    )])
    
    fig.update_layout(
        title='Trading Volume',
        yaxis_title='Volume',
        xaxis_title='Date',
        template='plotly_white',
        height=250,
        font=dict(family="Inter, sans-serif", color=COLORS['text']),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor='white'
    )
    
    return fig
