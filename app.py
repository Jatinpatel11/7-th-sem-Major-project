"""
Main application entry point for Indian Stock Dashboard.
"""
import streamlit as st
from src.auth.auth_service import auth_service
from src.auth.login_page import render_login_page
from src.dashboard.dashboard import render_dashboard


# Page configuration
st.set_page_config(
    page_title="Indian Stock Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load custom CSS styling."""
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # CSS file not found, use default styling


# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None


def main():
    """Main application logic."""
    # Load custom CSS
    load_css()
    
    # Check authentication status
    if not auth_service.is_authenticated():
        # Show login page
        render_login_page()
    else:
        # Show dashboard
        render_dashboard()


if __name__ == "__main__":
    main()
