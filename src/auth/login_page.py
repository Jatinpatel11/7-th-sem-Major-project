"""
Login page UI with elegant design and signup functionality.
"""
import streamlit as st
from src.auth.auth_service import auth_service


def render_login_page():
    """Render the login/signup page with modern fintech styling."""
    
    # Custom CSS for login page
    st.markdown("""
        <style>
        /* Login page specific styling */
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .login-header {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        
        .login-title {
            font-size: 32px;
            font-weight: 600;
            color: #1abc9c;
            margin-bottom: 10px;
        }
        
        .login-subtitle {
            font-size: 16px;
            color: #7f8c8d;
        }
        
        /* Gradient background */
        .stApp {
            background: linear-gradient(135deg, #ffffff 0%, #e8f8f5 50%, #d1f2eb 100%);
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            padding: 12px;
            font-size: 14px;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #1abc9c;
            box-shadow: 0 0 0 2px rgba(26, 188, 156, 0.1);
        }
        
        /* Buttons */
        .stButton > button {
            width: 100%;
            background-color: #1abc9c;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 12px 24px;
            font-weight: 500;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #16a085;
            box-shadow: 0 4px 12px rgba(26, 188, 156, 0.3);
        }
        
        /* Card styling */
        .login-card {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            justify-content: center;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 10px 24px;
            border-radius: 8px;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #1abc9c;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Header
        st.markdown("""
            <div class="login-header">
                <div class="login-title">📈 Indian Stock Dashboard</div>
                <div class="login-subtitle">Real-time analysis with AI-powered insights</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for Login and Signup
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input(
                    "Username",
                    placeholder="Enter your username",
                    key="login_username"
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if not username or not password:
                        st.error("Please enter both username and password")
                    else:
                        success, message = auth_service.authenticate_user(username, password)
                        
                        if success:
                            auth_service.login(username)
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.form("signup_form", clear_on_submit=True):
                new_username = st.text_input(
                    "Username",
                    placeholder="Choose a username",
                    key="signup_username"
                )
                new_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Choose a password (min 6 characters)",
                    key="signup_password"
                )
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm your password",
                    key="signup_confirm"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                signup_submit = st.form_submit_button("Sign Up", use_container_width=True)
                
                if signup_submit:
                    if not new_username or not new_password or not confirm_password:
                        st.error("Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = auth_service.create_user(new_username, new_password)
                        
                        if success:
                            st.success(f"{message}! Please login with your credentials.")
                        else:
                            st.error(message)
        
        # Footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align: center; color: #95a5a6; font-size: 12px;">
                <p>Powered by Yahoo Finance, VADER Sentiment Analysis & LSTM Models</p>
            </div>
        """, unsafe_allow_html=True)
