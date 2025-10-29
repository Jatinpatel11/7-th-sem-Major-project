# 📈 Indian Stock Market Dashboard

A modern, AI-powered stock market dashboard for Indian stocks and indices with real-time data, sentiment analysis, price predictions, and technical indicators.

## ✨ Features

- **🔐 User Authentication** - Secure login/signup with bcrypt password hashing
- **📊 Real-time Stock Data** - Live prices, volume, and market data from Yahoo Finance
- **💭 Sentiment Analysis** - AI-powered sentiment analysis using VADER on financial news
- **🔮 Price Predictions** - LSTM neural network for 1-5 day price forecasts
- **📈 Technical Indicators** - RSI, MACD, Moving Averages, Pivot Points
- **🎯 Support & Resistance** - Automated calculation of key price levels
- **🎨 Modern UI** - Clean, professional fintech-style interface with green-white theme
- **📱 Responsive Design** - Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd indian-stock-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file (optional):
```bash
cp .env.example .env
# Edit .env with your API keys if needed
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser and navigate to:
```
http://localhost:8501
```

## 📖 Usage

### First Time Setup

1. **Sign Up**: Create a new account on the login page
2. **Login**: Use your credentials to access the dashboard
3. **Search**: Enter a stock name or symbol (e.g., "Reliance", "Nifty 50", "TCS")
4. **Analyze**: View comprehensive analysis including:
   - Current price and key metrics
   - Historical price charts
   - Sentiment analysis from news
   - AI price predictions
   - Technical indicators

### Supported Stocks & Indices

- **Major Indices**: Nifty 50, Bank Nifty, Sensex
- **Popular Stocks**: Reliance, TCS, Infosys, HDFC Bank, ITC, Wipro, and more
- **Format**: Use stock names or symbols (e.g., "RELIANCE.NS" or just "Reliance")

## 🏗️ Project Structure

```
indian-stock-dashboard/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── src/
│   ├── auth/                      # Authentication module
│   │   ├── auth_service.py
│   │   └── login_page.py
│   ├── services/                  # Business logic services
│   │   ├── data_service.py        # Stock data fetching
│   │   ├── sentiment_service.py   # Sentiment analysis
│   │   ├── prediction_service.py  # Price predictions
│   │   ├── technical_indicators.py # Technical analysis
│   │   ├── news_fetcher.py        # News retrieval
│   │   ├── lstm_model.py          # LSTM model architecture
│   │   └── exceptions.py          # Custom exceptions
│   ├── visualization/             # UI components
│   │   ├── charts.py              # Plotly charts
│   │   └── ui_components.py       # Reusable UI elements
│   └── dashboard/
│       └── dashboard.py           # Main dashboard layout
├── models/                        # Pre-trained LSTM models
├── data/                          # User data and cache
├── tests/                         # Unit tests
└── assets/
    └── styles.css                 # Custom CSS styling
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables (optional):

```env
# News API for sentiment analysis (optional)
NEWS_API_KEY=your_news_api_key_here

# Application secret key
SECRET_KEY=your_secret_key_here
```

### Streamlit Configuration

The app uses custom theme settings in `.streamlit/config.toml`:
- Primary Color: #1abc9c (mint green)
- Background: White with gradient
- Font: Sans-serif

## 🧪 Testing

Run unit tests:

```bash
# Install pytest
pip install pytest pytest-mock

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_auth_service.py

# Run with coverage
pytest --cov=src tests/
```

## 🎨 Features in Detail

### Authentication System
- Secure password hashing with bcrypt (cost factor: 12)
- Session management using Streamlit session state
- JSON-based user storage (can be upgraded to database)

### Data Service
- Real-time data from Yahoo Finance API
- Caching (5 min for real-time, 1 hour for historical)
- Support for NSE (.NS) and BSE (.BO) stocks
- Automatic symbol formatting

### Sentiment Analysis
- VADER sentiment analyzer for financial text
- Google News RSS feed integration
- Weighted scoring (recent news weighted higher)
- Confidence calculation

### Price Prediction
- LSTM neural network with 60-day lookback
- Confidence intervals for predictions
- Linear regression fallback for stocks without trained models
- 1-5 day forecasts

### Technical Indicators
- Moving Averages (20, 50, 200 periods)
- RSI (14 period) with overbought/oversold signals
- MACD with histogram
- Pivot points for support/resistance

## 🔒 Security

- Passwords hashed with bcrypt
- No plain text password storage
- Session-based authentication
- Input validation and sanitization
- Error handling for API failures

## 📊 Performance

- Streamlit caching for optimal performance
- 5-minute cache for real-time data
- 1-hour cache for historical data
- 30-minute cache for sentiment analysis
- Lazy loading of LSTM models

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Stock symbol not found**
   - Try adding .NS suffix (e.g., "RELIANCE.NS")
   - Check spelling of stock name
   - Verify stock is listed on NSE or BSE

3. **Sentiment analysis shows no data**
   - This is normal if no recent news is available
   - Try a more popular stock with more news coverage

4. **Predictions not working**
   - Ensure sufficient historical data (60+ days)
   - System will use linear regression fallback if LSTM model unavailable

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Yahoo Finance** for stock market data
- **VADER** for sentiment analysis
- **Streamlit** for the web framework
- **TensorFlow** for LSTM models
- **Plotly** for interactive charts

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

**Note:** This dashboard is for educational and informational purposes only. It should not be used as the sole basis for investment decisions. Always conduct thorough research and consult with financial advisors before making investment decisions.
