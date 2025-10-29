"""
Main dashboard layout and orchestration.
"""
import streamlit as st
from datetime import datetime
from src.auth.auth_service import auth_service
from src.services.data_service import (
    get_stock_data, get_current_price, clear_cache, format_inr
)
from src.services.sentiment_service import get_sentiment_analysis
from src.services.prediction_service import get_price_predictions
from src.services.technical_indicators import calculate_all_indicators
from src.services.exceptions import (
    InvalidSymbolError, NetworkError, APIRateLimitError, DataNotAvailableError
)
from src.visualization.charts import (
    create_price_chart, create_sentiment_gauge, create_prediction_chart,
    create_technical_indicator_chart, create_volume_chart
)
from src.visualization.ui_components import (
    create_section_header, create_alert, create_divider
)


def render_sidebar():
    """Render sidebar with About section and controls."""
    with st.sidebar:
        st.title("📈 Stock Dashboard")
        
        # User info
        username = auth_service.get_current_user()
        st.write(f"Welcome, **{username}**!")
        
        create_divider()
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            clear_cache()
            st.rerun()
        
        create_divider()
        
        # About section
        with st.expander("ℹ️ About", expanded=False):
            st.markdown("""
            ### LSTM Price Prediction
            
            Our Long Short-Term Memory (LSTM) neural network analyzes 60 days of historical 
            price data to predict future trends. The model learns patterns in stock movements 
            to forecast prices for the next 1-5 days.
            
            **Note:** Predictions include confidence intervals and should be used alongside 
            other analysis methods.
            
            ### Sentiment Analysis
            
            We use VADER (Valence Aware Dictionary and sEntiment Reasoner) to analyze 
            financial news and social media. The algorithm:
            
            - Fetches recent news (last 48 hours)
            - Analyzes text sentiment
            - Weights recent news more heavily
            - Provides overall sentiment score
            
            ### Technical Indicators
            
            - **Moving Averages (MA):** Trend identification
            - **RSI:** Overbought/oversold conditions
            - **MACD:** Momentum and trend strength
            - **Pivot Points:** Support/resistance levels
            """)
        
        create_divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            auth_service.logout()
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def render_stock_overview(stock_data: dict):
    """Render stock overview section with key metrics."""
    create_section_header("📊 Stock Overview", "Current market status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price",
            f"₹{stock_data['current_price']}",
            f"{stock_data['change_percent']}%"
        )
    
    with col2:
        st.metric(
            "Day High",
            f"₹{stock_data['day_high']}"
        )
    
    with col3:
        st.metric(
            "Day Low",
            f"₹{stock_data['day_low']}"
        )
    
    with col4:
        st.metric(
            "Volume",
            format_inr(stock_data['volume'])
        )


def render_sentiment_section(symbol: str):
    """Render sentiment analysis section."""
    create_section_header("💭 Sentiment Analysis", "Market sentiment from news and social media")
    
    try:
        with st.spinner("Analyzing sentiment..."):
            sentiment = get_sentiment_analysis(symbol)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Sentiment gauge
            fig = create_sentiment_gauge(sentiment)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sentiment details
            st.markdown(f"""
            ### Analysis Results
            
            - **Overall Score:** {sentiment['overall_score']} ({sentiment['category']})
            - **Confidence:** {sentiment['confidence'] * 100:.0f}%
            - **Sources Analyzed:** {sentiment['sources_analyzed']}
            
            #### Breakdown:
            - 🟢 Positive: {sentiment['breakdown']['positive']}
            - ⚪ Neutral: {sentiment['breakdown']['neutral']}
            - 🔴 Negative: {sentiment['breakdown']['negative']}
            """)
            
            if sentiment['sources_analyzed'] == 0:
                create_alert("No recent news available for sentiment analysis", "warning")
    
    except Exception as e:
        create_alert(f"Unable to fetch sentiment data: {str(e)}", "error")


def render_prediction_section(symbol: str):
    """Render price prediction section."""
    create_section_header("🔮 Price Prediction", "AI-powered price forecasts")
    
    try:
        with st.spinner("Generating predictions..."):
            predictions = get_price_predictions(symbol, days=5)
        
        if predictions:
            # Prediction chart
            fig = create_prediction_chart(predictions)
            st.plotly_chart(fig, use_container_width=True)
            
            # Prediction table
            st.markdown("### Predicted Prices (Next 5 Days)")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            for i, (date, price) in enumerate(zip(predictions['dates'], predictions['predictions'])):
                with [col1, col2, col3, col4, col5][i]:
                    st.metric(
                        date,
                        f"₹{price}"
                    )
            
            st.caption(f"Model: {predictions.get('model_type', 'LSTM')}")
        else:
            create_alert("Unable to generate predictions. Insufficient data.", "warning")
    
    except Exception as e:
        create_alert(f"Prediction error: {str(e)}", "error")


def render_technical_indicators(symbol: str, data):
    """Render technical indicators section."""
    create_section_header("📈 Technical Indicators", "Advanced technical analysis")
    
    try:
        with st.spinner("Calculating indicators..."):
            indicators = calculate_all_indicators(data)
        
        # Moving Averages
        st.markdown("### Moving Averages")
        col1, col2, col3 = st.columns(3)
        mas = indicators['moving_averages']
        
        with col1:
            st.metric("MA 20", f"₹{mas.get('MA_20', 'N/A')}")
        with col2:
            st.metric("MA 50", f"₹{mas.get('MA_50', 'N/A')}")
        with col3:
            st.metric("MA 200", f"₹{mas.get('MA_200', 'N/A')}")
        
        # RSI and MACD
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### RSI (Relative Strength Index)")
            rsi = indicators['rsi']
            st.metric("Current RSI", rsi.get('current', 'N/A'), rsi.get('signal', ''))
            
            if rsi.get('current'):
                fig = create_technical_indicator_chart('RSI', data, rsi)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### MACD")
            macd = indicators['macd']
            st.metric("MACD", macd.get('macd', 'N/A'), macd.get('trend', ''))
            
            if macd.get('macd'):
                fig = create_technical_indicator_chart('MACD', data, macd)
                st.plotly_chart(fig, use_container_width=True)
        
        # Support and Resistance
        st.markdown("### Support & Resistance Levels")
        pivot = indicators['pivot_points']
        
        if pivot:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Resistance Levels**")
                st.write(f"R3: ₹{pivot.get('resistance_3', 'N/A')}")
                st.write(f"R2: ₹{pivot.get('resistance_2', 'N/A')}")
                st.write(f"R1: ₹{pivot.get('resistance_1', 'N/A')}")
            
            with col2:
                st.markdown("**Support Levels**")
                st.write(f"S1: ₹{pivot.get('support_1', 'N/A')}")
                st.write(f"S2: ₹{pivot.get('support_2', 'N/A')}")
                st.write(f"S3: ₹{pivot.get('support_3', 'N/A')}")
            
            st.write(f"**Pivot Point:** ₹{pivot.get('pivot', 'N/A')}")
    
    except Exception as e:
        create_alert(f"Error calculating indicators: {str(e)}", "error")


def render_dashboard():
    """Main dashboard rendering function."""
    # Render sidebar
    render_sidebar()
    
    # Main content
    st.title("📈 Indian Stock Market Dashboard")
    st.markdown("Real-time analysis with AI-powered insights")
    
    # Search bar
    col1, col2 = st.columns([3, 1])
    with col1:
        symbol = st.text_input(
            "Search for a stock or index",
            placeholder="e.g., Reliance, Nifty 50, TCS, Bank Nifty",
            key="stock_search"
        )
    with col2:
        search_button = st.button("🔍 Analyze", use_container_width=True, type="primary")
    
    # If symbol is provided
    if symbol and (search_button or st.session_state.get('last_symbol') == symbol):
        st.session_state['last_symbol'] = symbol
        
        try:
            # Fetch stock data
            with st.spinner(f"Fetching data for {symbol}..."):
                stock_data = get_current_price(symbol)
                historical_data = get_stock_data(symbol, period="1y")
            
            # Stock Overview
            render_stock_overview(stock_data)
            
            create_divider()
            
            # Price Chart
            create_section_header("📊 Price Chart", "Historical price movement")
            indicators = calculate_all_indicators(historical_data)
            fig = create_price_chart(historical_data, indicators, 
                                    title=f"{stock_data['name']} - Price History")
            st.plotly_chart(fig, use_container_width=True)
            
            # Volume Chart
            fig_volume = create_volume_chart(historical_data)
            st.plotly_chart(fig_volume, use_container_width=True)
            
            create_divider()
            
            # Sentiment Analysis
            render_sentiment_section(symbol)
            
            create_divider()
            
            # Price Prediction
            render_prediction_section(symbol)
            
            create_divider()
            
            # Technical Indicators
            render_technical_indicators(symbol, historical_data)
        
        except InvalidSymbolError as e:
            create_alert(f"Invalid stock symbol: {symbol}. Please check and try again.", "error")
        except NetworkError as e:
            create_alert(str(e), "error")
        except APIRateLimitError as e:
            create_alert(str(e), "warning")
        except DataNotAvailableError as e:
            create_alert(str(e), "warning")
        except Exception as e:
            create_alert(f"An error occurred: {str(e)}", "error")
    
    elif not symbol:
        # Welcome message
        st.info("👋 Welcome! Enter a stock symbol or name above to get started.")
        
        st.markdown("""
        ### Popular Indian Stocks & Indices
        
        Try searching for:
        - **Indices:** Nifty 50, Bank Nifty, Sensex
        - **Stocks:** Reliance, TCS, Infosys, HDFC Bank, ITC, Wipro
        
        ### Features
        
        - 📊 Real-time stock prices and charts
        - 💭 AI-powered sentiment analysis
        - 🔮 LSTM price predictions
        - 📈 Technical indicators (RSI, MACD, Moving Averages)
        - 🎯 Support & resistance levels
        """)
