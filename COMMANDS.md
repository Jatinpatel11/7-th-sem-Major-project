# 💻 Command Reference

## 🚀 Deployment Commands

### Push to GitHub
```bash
# First time setup
git init
git add .
git commit -m "Indian Stock Dashboard - Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Update Existing Repository
```bash
git add .
git commit -m "Update: description of changes"
git push
```

## 🧪 Local Testing Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application
```bash
streamlit run app.py
```

### Run with Specific Port
```bash
streamlit run app.py --server.port 8502
```

### Run Tests
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

## 🔍 Verification Commands

### Check Files Exist
```bash
# Windows
dir app.py requirements.txt packages.txt

# Linux/Mac
ls app.py requirements.txt packages.txt .streamlit/config.toml
```

### Check Python Syntax
```bash
python -m py_compile app.py
```

### Check Imports
```bash
python -c "import src.auth.auth_service; import src.dashboard.dashboard; print('Imports OK')"
```

### Find All Python Files
```bash
# Windows
dir /s /b *.py

# Linux/Mac
find . -name "*.py"
```

### Count Files
```bash
# Windows
dir /s /b | find /c /v ""

# Linux/Mac
find . -type f | wc -l
```

## 📦 Package Management

### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Update Requirements
```bash
pip freeze > requirements.txt
```

### Install from Requirements
```bash
pip install -r requirements.txt
```

### Upgrade Package
```bash
pip install --upgrade streamlit
```

## 🔧 Streamlit Commands

### Clear Cache
```bash
streamlit cache clear
```

### Show Config
```bash
streamlit config show
```

### Check Version
```bash
streamlit version
```

### Open Browser Automatically
```bash
streamlit run app.py --server.headless false
```

## 🐛 Debugging Commands

### Check Python Version
```bash
python --version
```

### Check Pip Version
```bash
pip --version
```

### List Installed Packages
```bash
pip list
```

### Check Package Version
```bash
pip show streamlit
```

### Python Interactive Test
```bash
python
>>> import streamlit as st
>>> import yfinance as yf
>>> print("All imports working!")
>>> exit()
```

## 📊 Git Commands

### Check Status
```bash
git status
```

### View Commit History
```bash
git log --oneline
```

### Create New Branch
```bash
git checkout -b feature-name
```

### Switch Branch
```bash
git checkout main
```

### Pull Latest Changes
```bash
git pull origin main
```

### View Remote URL
```bash
git remote -v
```

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

## 🔒 Security Commands

### Generate Secret Key
```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Check for Secrets in Code
```bash
# Windows
findstr /s /i "password\|secret\|api_key" *.py

# Linux/Mac
grep -r -i "password\|secret\|api_key" --include="*.py" .
```

## 📁 File Operations

### Create Directory
```bash
# Windows
mkdir data\cache

# Linux/Mac
mkdir -p data/cache
```

### Copy File
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### Remove File
```bash
# Windows
del file.txt

# Linux/Mac
rm file.txt
```

### View File Content
```bash
# Windows
type requirements.txt

# Linux/Mac
cat requirements.txt
```

## 🌐 Network Commands

### Check Internet Connection
```bash
# Windows
ping google.com

# Linux/Mac
ping -c 4 google.com
```

### Test API Endpoint
```bash
curl https://query1.finance.yahoo.com/v8/finance/chart/RELIANCE.NS
```

## 📈 Performance Commands

### Measure App Load Time
```bash
time streamlit run app.py
```

### Check Memory Usage
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python
```

## 🔄 Maintenance Commands

### Clean Python Cache
```bash
# Windows
del /s /q __pycache__
del /s /q *.pyc

# Linux/Mac
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Clean Git Cache
```bash
git rm -r --cached .
git add .
git commit -m "Clean cache"
```

## 📱 Streamlit Cloud Commands

### View Logs (via CLI)
```bash
# Not directly available, use web dashboard
# https://share.streamlit.io
```

### Trigger Redeploy
```bash
# Push any change to GitHub
git commit --allow-empty -m "Trigger redeploy"
git push
```

## 🎯 Quick Commands

### Full Local Test
```bash
pip install -r requirements.txt && streamlit run app.py
```

### Quick Deploy
```bash
git add . && git commit -m "Update" && git push
```

### Clean and Run
```bash
# Windows
del /s /q __pycache__ && streamlit run app.py

# Linux/Mac
find . -type d -name __pycache__ -exec rm -r {} + && streamlit run app.py
```

## 📝 Documentation Commands

### Generate File Tree
```bash
# Windows
tree /F

# Linux/Mac
tree -L 3
```

### Count Lines of Code
```bash
# Windows
(for /r %f in (*.py) do @type "%f") | find /c /v ""

# Linux/Mac
find . -name "*.py" -exec wc -l {} + | tail -1
```

## 🆘 Emergency Commands

### Kill Streamlit Process
```bash
# Windows
taskkill /F /IM streamlit.exe

# Linux/Mac
pkill -f streamlit
```

### Reset Git Repository
```bash
# WARNING: This deletes all local changes
git reset --hard HEAD
git clean -fd
```

### Reinstall All Packages
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 📞 Help Commands

### Streamlit Help
```bash
streamlit --help
```

### Python Help
```bash
python --help
```

### Git Help
```bash
git --help
```

### Pip Help
```bash
pip --help
```

---

## 🎯 Most Used Commands

```bash
# 1. Run app locally
streamlit run app.py

# 2. Push to GitHub
git add . && git commit -m "Update" && git push

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
pytest tests/

# 5. Check status
git status
```

---

**Tip:** Bookmark this file for quick reference! 📌
