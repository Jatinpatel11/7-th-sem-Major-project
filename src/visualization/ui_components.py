"""
Reusable UI components for the dashboard.
"""
import streamlit as st
from typing import Optional


def create_metric_card(title: str, value: str, delta: Optional[str] = None, 
                      delta_color: str = "normal"):
    """Create a styled metric card.
    
    Args:
        title: Metric title
        value: Metric value
        delta: Change value (optional)
        delta_color: Color for delta ("normal", "inverse", "off")
    """
    st.metric(
        label=title,
        value=value,
        delta=delta,
        delta_color=delta_color
    )


def create_info_card(title: str, content: str, icon: str = "ℹ️"):
    """Create an information card with custom styling.
    
    Args:
        title: Card title
        content: Card content
        icon: Icon to display
    """
    st.markdown(f"""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
        ">
            <h3 style="color: #1abc9c; margin: 0 0 10px 0;">
                {icon} {title}
            </h3>
            <p style="color: #2c3e50; margin: 0;">
                {content}
            </p>
        </div>
    """, unsafe_allow_html=True)


def create_section_header(title: str, subtitle: Optional[str] = None):
    """Create a styled section header.
    
    Args:
        title: Section title
        subtitle: Optional subtitle
    """
    st.markdown(f"""
        <div style="margin: 30px 0 20px 0;">
            <h2 style="color: #1abc9c; margin: 0; font-size: 28px;">
                {title}
            </h2>
            {f'<p style="color: #7f8c8d; margin: 5px 0 0 0;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def create_stat_box(label: str, value: str, color: str = "#1abc9c"):
    """Create a small stat box.
    
    Args:
        label: Stat label
        value: Stat value
        color: Box color
    """
    st.markdown(f"""
        <div style="
            background: {color};
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 12px; opacity: 0.9;">{label}</div>
            <div style="font-size: 24px; font-weight: 600; margin-top: 5px;">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def create_alert(message: str, alert_type: str = "info"):
    """Create a styled alert box.
    
    Args:
        message: Alert message
        alert_type: Type of alert ("info", "success", "warning", "error")
    """
    colors = {
        "info": {"bg": "#e8f8f5", "border": "#1abc9c", "icon": "ℹ️"},
        "success": {"bg": "#d5f4e6", "border": "#27ae60", "icon": "✅"},
        "warning": {"bg": "#fff9e6", "border": "#f39c12", "icon": "⚠️"},
        "error": {"bg": "#ffebee", "border": "#e74c3c", "icon": "❌"}
    }
    
    style = colors.get(alert_type, colors["info"])
    
    st.markdown(f"""
        <div style="
            background: {style['bg']};
            border-left: 4px solid {style['border']};
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
        ">
            <span style="font-size: 18px; margin-right: 10px;">{style['icon']}</span>
            <span style="color: #2c3e50;">{message}</span>
        </div>
    """, unsafe_allow_html=True)


def create_loading_spinner(text: str = "Loading..."):
    """Create a loading spinner with text.
    
    Args:
        text: Loading text
    """
    with st.spinner(text):
        pass


def create_divider():
    """Create a styled divider."""
    st.markdown("""
        <hr style="
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, #1abc9c, transparent);
            margin: 30px 0;
        ">
    """, unsafe_allow_html=True)
