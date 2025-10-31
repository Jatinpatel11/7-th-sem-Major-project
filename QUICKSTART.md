# ⚡ Quick Start Guide

## 🚀 Deploy to Streamlit Cloud in 5 Minutes

### Step 1: Push to GitHub (2 minutes)

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Indian Stock Dashboard - Initial commit"

# Create main branch
git branch -M main

# Add your GitHub repository (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/indian-stock-dashboard.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud (3 minutes)

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository:** `YOUR_USERNAME/indian-stock-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy!"**

### Step 3: Wait & Access

- Wait 2-5 minutes for deployment
- Get your URL: `https://your-app-name.streamlit.app`
- Share and enjoy! 🎉

## 🧪 Test Locally First (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Open browser
# http://localhost:8501
```

## 📝 Quick Test Checklist

Once deployed, test these:

1. ✅ Sign up with a new account
2. ✅ Login with credentials
3. ✅ Search "Reliance" or "Nifty 50"
4. ✅ View stock price and charts
5. ✅ Check sentiment analysis
6. ✅ See price predictions
7. ✅ View technical indicators
8. ✅ Click refresh button
9. ✅ Logout

## 🎯 Popular Stocks to Try

- **Indices:** Nifty 50, Bank Nifty, Sensex
- **Stocks:** Reliance, TCS, Infosys, HDFC Bank, ITC

## 🐛 Issues?

### App won't start?
- Check `app.py` is in root directory
- Verify all files from SETUP.md are present
- Check Streamlit Cloud logs

### Module errors?
- Ensure `requirements.txt` has all packages
- Check package versions are compatible

### Stock not found?
- Try adding `.NS` suffix (e.g., "RELIANCE.NS")
- Use common names: "Reliance", "TCS", "Nifty 50"

## 📚 More Help

- **Full Setup:** See `SETUP.md`
- **Deployment Details:** See `DEPLOYMENT.md`
- **Code Documentation:** See `README.md`

## 🎉 That's It!

Your Indian Stock Market Dashboard is now live!

**Your URL:** `https://your-app-name.streamlit.app`

Share it with the world! 🌍
