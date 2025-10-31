#!/bin/bash

# Setup script for Streamlit Cloud deployment

# Create necessary directories
mkdir -p ~/.streamlit/
mkdir -p data/cache/
mkdir -p models/

# Create Streamlit config
echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = \$PORT\n\
" > ~/.streamlit/config.toml
