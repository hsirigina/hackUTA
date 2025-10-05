"""Modern UI components matching the reference design."""
import streamlit as st
import streamlit.components.v1 as components
from typing import List, Dict, Any


def gradient_card(title: str, value: str, icon: str, gradient: str, subtitle: str = ""):
    """
    Create a gradient card like in the reference design.

    Args:
        title: Card title (e.g., "Miles Driven")
        value: Main value (e.g., "34.05")
        icon: Icon HTML or emoji
        gradient: CSS gradient (e.g., "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
        subtitle: Optional subtitle text
    """
    subtitle_html = f'<div style="font-size: 0.85rem; opacity: 0.9; margin-top: 0.25rem;">{subtitle}</div>' if subtitle else ''

    html = f"""
    <div style="
        background: {gradient};
        border-radius: 20px;
        padding: 1.8rem 1.5rem;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 24px rgba(0,0,0,0.15)'"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)'">

        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="
                background: rgba(255,255,255,0.25);
                border-radius: 12px;
                padding: 0.8rem;
                font-size: 1.8rem;
                display: flex;
                align-items: center;
                justify-content: center;
            ">{icon}</div>
        </div>

        <div>
            <div style="font-size: 0.9rem; opacity: 0.95; font-weight: 500; margin-bottom: 0.3rem;">
                {title}
            </div>
            <div style="font-size: 2rem; font-weight: 700;">
                {value}
            </div>
            {subtitle_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def analytics_item(label: str, value: str, sublabel: str = "", arrow: bool = True):
    """
    Create an analytics list item.

    Args:
        label: Main label
        value: Value to display
        sublabel: Optional sublabel
        arrow: Whether to show arrow
    """
    arrow_html = '<span style="color: #999;">→</span>' if arrow else ''
    sublabel_html = f'<div style="font-size: 0.8rem; color: #999; margin-top: 0.2rem;">{sublabel}</div>' if sublabel else ''

    html = f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
        border-bottom: 1px solid #f0f0f0;
        transition: background 0.2s ease;
    " onmouseover="this.style.background='#f8f9fa'"
       onmouseout="this.style.background='transparent'">
        <div>
            <div style="font-weight: 600; color: #333;">{value}</div>
            {sublabel_html}
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color: #666; font-size: 0.9rem;">{label}</span>
            {arrow_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def earnings_card(balance: str, gradient: str = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"):
    """
    Create an earnings/balance card.

    Args:
        balance: Balance amount
        gradient: CSS gradient
    """
    html = f"""
    <div style="
        background: {gradient};
        border-radius: 20px;
        padding: 1.8rem;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="
                background: rgba(255,255,255,0.25);
                border-radius: 12px;
                padding: 0.8rem;
                font-size: 1.5rem;
            ">💰</div>
        </div>

        <div style="font-size: 0.9rem; opacity: 0.95; margin-bottom: 0.5rem;">
            Personal balance
        </div>
        <div style="font-size: 2.2rem; font-weight: 700; margin-bottom: 1.5rem;">
            {balance}
        </div>

        <button style="
            background: white;
            color: #f5576c;
            border: none;
            border-radius: 10px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            transition: transform 0.2s ease;
        " onmouseover="this.style.transform='scale(1.02)'"
           onmouseout="this.style.transform='scale(1)'">
            Withdraw
        </button>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def modern_page_header(title: str, subtitle: str = "", tabs: List[str] = None):
    """
    Create a modern page header with optional tabs.

    Args:
        title: Page title
        subtitle: Optional subtitle
        tabs: List of tab names
    """
    subtitle_html = f'<div style="color: #666; font-size: 0.95rem; margin-top: 0.3rem;">{subtitle}</div>' if subtitle else ''

    tabs_html = ""
    if tabs:
        tab_items = ""
        for i, tab in enumerate(tabs):
            active = "background: #f0f0f0; color: #333;" if i == 0 else ""
            tab_items += f'''
            <button style="
                background: transparent;
                border: none;
                padding: 0.5rem 1.2rem;
                border-radius: 8px;
                cursor: pointer;
                font-size: 0.9rem;
                color: #999;
                transition: all 0.2s ease;
                {active}
            " onmouseover="if(!this.style.background.includes('#f0f0f0')) this.style.background='#f8f9fa'"
               onmouseout="if(!this.style.background.includes('#f0f0f0')) this.style.background='transparent'">
                {tab}
            </button>
            '''
        tabs_html = f'<div style="display: flex; gap: 0.5rem; margin-top: 1rem;">{tab_items}</div>'

    html = f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-size: 2rem; font-weight: 700; color: #1a1a1a; margin: 0;">
            {title}
        </h1>
        {subtitle_html}
        {tabs_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def sidebar_nav_item(icon: str, label: str, active: bool = False):
    """
    Create a sidebar navigation item.

    Args:
        icon: Icon HTML or emoji
        label: Navigation label
        active: Whether item is active
    """
    bg_color = "#e8f4fd" if active else "transparent"
    icon_color = "#1e88e5" if active else "#666"
    text_color = "#1e88e5" if active else "#666"

    html = f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        background: {bg_color};
        color: {text_color};
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 0.3rem;
    " onmouseover="if(this.style.background=='transparent') this.style.background='#f5f5f5'"
       onmouseout="if(this.style.background!='rgb(232, 244, 253)') this.style.background='transparent'">
        <span style="font-size: 1.3rem; color: {icon_color};">{icon}</span>
        <span style="font-weight: 500;">{label}</span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def invite_card(code: str):
    """
    Create an invite friends card.

    Args:
        code: Invite code
    """
    html = f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 1.8rem;
        color: white;
        text-align: center;
    ">
        <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">
            Invite Friends
        </div>
        <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 1.5rem;">
            Share your invite code
        </div>

        <div style="
            background: white;
            color: #667eea;
            border-radius: 10px;
            padding: 0.8rem;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 1rem;
        ">
            {code}
        </div>

        <button style="
            background: rgba(255,255,255,0.25);
            color: white;
            border: 1px solid rgba(255,255,255,0.4);
            border-radius: 10px;
            padding: 0.7rem 2rem;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            transition: background 0.2s ease;
        " onmouseover="this.style.background='rgba(255,255,255,0.35)'"
           onmouseout="this.style.background='rgba(255,255,255,0.25)'">
            Invite friends
        </button>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def apply_modern_theme():
    """Apply modern theme styling to the entire app."""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Global Styles */
        * {
            font-family: 'Inter', sans-serif;
        }

        /* Main container */
        .main {
            background: #f8f9fc;
            padding: 2rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: white;
            padding: 1.5rem 1rem;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: white;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Card containers */
        .element-container {
            margin-bottom: 1rem;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        /* Expanders */
        .streamlit-expanderHeader {
            border-radius: 10px;
            background: white;
        }

        /* Remove extra padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
