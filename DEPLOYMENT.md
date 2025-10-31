# 🚀 Deployment Guide for Streamlit Cloud

This guide will help you deploy the Indian Stock Market Dashboard to Streamlit Cloud.

## 📋 Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
3. Your code pushed to a GitHub repository

## 🔧 Step-by-Step Deployment

### 1. Prepare Your GitHub Repository

1. **Create a new repository on GitHub**
   ```bash
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit: Indian Stock Dashboard"
   
   # Add remote (replace with your repo URL)
   git remote add origin https://github.com/yourusername/indian-stock-dashboard.git
   
   # Push to GitHub
   git push -u origin main
   ```

2. **Verify these files are in your repository:**
   - ✅ `app.py` (main entry point)
   - ✅ `requirements.txt` (Python dependencies)
   - ✅ `.streamlit/config.toml` (Streamlit configuration)
   - ✅ `packages.txt` (system packages - can be empty)
   - ✅ All source code in `src/` directory

### 2. Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Click "New app"**

3. **Fill in the deployment settings:**
   - **Repository:** Select your GitHub repository
   - **Branch:** `main` (or your default branch)
   - **Main file path:** `app.py`
   - **App URL:** Choose a custom URL (e.g., `indian-stock-dashboard`)

4. **Configure Secrets (Important!)**
   
   Click on "Advanced settings" → "Secrets"
   
   Add the following in TOML format:
   ```toml
   # Optional: Add if you have API keys
   SECRET_KEY = "your_random_secret_key_here"
   NEWS_API_KEY = "your_news_api_key_if_you_have_one"
   ```

5. **Click "Deploy!"**

### 3. Wait for Deployment

- Streamlit Cloud will:
  - Install Python dependencies from `requirements.txt`
  - Install system packages from `packages.txt`
  - Run your app
  - Provide you with a public URL

- Initial deployment takes 2-5 minutes
- You'll see logs in real-time

### 4. Access Your App

Once deployed, you'll get a URL like:
```
https://your-app-name.streamlit.app
```

Share this URL with anyone to access your dashboard!

## 🔐 Important Security Notes

### For Production Deployment:

1. **Never commit sensitive data:**
   - The `.gitignore` file already excludes:
     - `.env` files
     - `data/users.json` (user credentials)
     - Cache files
   
2. **Use Streamlit Secrets for sensitive data:**
   - API keys
   - Secret keys
   - Database credentials

3. **User Data Storage:**
   - By default, user data is stored in `data/users.json`
   - On Streamlit Cloud, this resets on each deployment
   - For production, consider using:
     - Streamlit Cloud's persistent storage
     - External database (PostgreSQL, MongoDB)
     - Firebase Authentication

## 🐛 Troubleshooting

### Common Issues:

1. **Module not found errors:**
   - Check `requirements.txt` has all dependencies
   - Verify package names and versions

2. **App crashes on startup:**
   - Check logs in Streamlit Cloud dashboard
   - Verify `app.py` path is correct
   - Ensure all imports are correct

3. **Data not persisting:**
   - User accounts reset on each deployment
   - This is normal for file-based storage on Streamlit Cloud
   - Users need to sign up again after redeployment

4. **Slow performance:**
   - First load is slower (cold start)
   - Subsequent loads are faster
   - Consider upgrading to Streamlit Cloud paid plan for better performance

### Check Logs:

In Streamlit Cloud dashboard:
- Click on your app
- Click "Manage app"
- View logs in real-time

## 🔄 Updating Your App

To update your deployed app:

1. **Make changes locally**
2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. **Streamlit Cloud auto-deploys** (usually within 1-2 minutes)

## 📊 Monitoring

### Streamlit Cloud provides:

- **Analytics:** View app usage and visitors
- **Logs:** Real-time application logs
- **Resource usage:** CPU and memory monitoring
- **Uptime:** App availability status

## 🎯 Optimization Tips

1. **Caching:**
   - Already implemented with `@st.cache_data`
   - Reduces API calls and improves performance

2. **Lazy Loading:**
   - LSTM models load only when needed
   - News fetched only when requested

3. **Error Handling:**
   - Comprehensive error handling implemented
   - Graceful degradation for API failures

## 💰 Cost

- **Free Tier:**
  - 1 GB RAM
  - 1 CPU core
  - Unlimited public apps
  - Community support

- **Paid Tiers:**
  - More resources
  - Private apps
  - Custom domains
  - Priority support

## 🔗 Useful Links

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Forums](https://discuss.streamlit.io/)
- [Deployment Troubleshooting](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/app-dependencies)

## 📝 Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Can create new user account
- [ ] Can login with credentials
- [ ] Stock search works (try "Reliance" or "Nifty 50")
- [ ] Charts display correctly
- [ ] Sentiment analysis shows results
- [ ] Price predictions generate
- [ ] Technical indicators calculate
- [ ] Refresh button works
- [ ] Logout works
- [ ] Mobile responsive (test on phone)

## 🎉 You're Live!

Congratulations! Your Indian Stock Market Dashboard is now live and accessible to anyone with the URL.

### Share Your App:

- Share the URL on social media
- Add to your portfolio
- Include in your resume
- Get feedback from users

---

**Need Help?** Open an issue on GitHub or check Streamlit Community forums.
