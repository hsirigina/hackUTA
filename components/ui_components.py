"""Enhanced UI components using HTML, CSS, and JavaScript."""
import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Optional, Any


def metric_card(title: str, value: str, delta: Optional[str] = None, icon: str = "📊", color: str = "#1e88e5"):
    """
    Create a beautiful metric card with custom styling.

    Args:
        title: Card title
        value: Main metric value
        delta: Change indicator (optional)
        icon: Emoji icon
        color: Accent color (hex)
    """
    delta_html = ""
    if delta:
        delta_color = "#4caf50" if not delta.startswith("-") else "#f44336"
        delta_html = f'<div style="color: {delta_color}; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</div>'

    html = f"""
    <div style="
        background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)'"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.1)'">

        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2.5rem;">{icon}</div>
            <div style="flex: 1;">
                <div style="color: #666; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
                    {title}
                </div>
                <div style="font-size: 2rem; font-weight: 700; color: {color};">
                    {value}
                </div>
                {delta_html}
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def stat_card_row(stats: List[Dict[str, Any]]):
    """
    Create a row of statistic cards.

    Args:
        stats: List of dicts with keys: title, value, delta, icon, color
    """
    cols = st.columns(len(stats))
    for col, stat in zip(cols, stats):
        with col:
            metric_card(
                title=stat.get('title', 'Metric'),
                value=stat.get('value', '0'),
                delta=stat.get('delta'),
                icon=stat.get('icon', '📊'),
                color=stat.get('color', '#1e88e5')
            )


def info_card(title: str, content: str, icon: str = "ℹ️", bg_color: str = "#e3f2fd"):
    """
    Create an informational card.

    Args:
        title: Card title
        content: Card content (supports HTML)
        icon: Icon emoji
        bg_color: Background color
    """
    html = f"""
    <div style="
        background: {bg_color};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1e88e5;
    ">
        <div style="display: flex; align-items: start; gap: 1rem;">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 0.5rem 0; color: #1565c0;">{title}</h3>
                <div style="color: #424242; line-height: 1.6;">
                    {content}
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def progress_ring(percentage: int, label: str, color: str = "#1e88e5", size: int = 120):
    """
    Create an animated circular progress ring.

    Args:
        percentage: Progress percentage (0-100)
        label: Label text
        color: Ring color
        size: Ring size in pixels
    """
    circumference = 2 * 3.14159 * 45  # radius = 45
    offset = circumference - (percentage / 100) * circumference

    html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; margin: 1rem;">
        <svg width="{size}" height="{size}" style="transform: rotate(-90deg);">
            <circle cx="{size//2}" cy="{size//2}" r="45"
                    stroke="#e0e0e0" stroke-width="8" fill="none"/>
            <circle cx="{size//2}" cy="{size//2}" r="45"
                    stroke="{color}" stroke-width="8" fill="none"
                    stroke-dasharray="{circumference}"
                    stroke-dashoffset="{offset}"
                    stroke-linecap="round"
                    style="transition: stroke-dashoffset 1s ease;">
            </circle>
            <text x="{size//2}" y="{size//2}" text-anchor="middle" dy="7"
                  style="font-size: 1.5rem; font-weight: bold; fill: {color}; transform: rotate(90deg); transform-origin: {size//2}px {size//2}px;">
                {percentage}%
            </text>
        </svg>
        <div style="margin-top: 0.5rem; color: #666; font-weight: 500;">{label}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def timeline_item(title: str, time: str, description: str, icon: str = "📍", is_last: bool = False):
    """
    Create a timeline item.

    Args:
        title: Event title
        time: Event time
        description: Event description
        icon: Icon emoji
        is_last: Whether this is the last item (no line below)
    """
    line = "" if is_last else """
    <div style="
        position: absolute;
        left: 15px;
        top: 40px;
        bottom: -20px;
        width: 2px;
        background: #e0e0e0;
    "></div>
    """

    html = f"""
    <div style="position: relative; padding-left: 50px; padding-bottom: 20px;">
        {line}
        <div style="
            position: absolute;
            left: 0;
            top: 0;
            width: 32px;
            height: 32px;
            background: white;
            border: 2px solid #1e88e5;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            z-index: 1;
        ">{icon}</div>

        <div style="
            background: #f5f5f5;
            border-radius: 8px;
            padding: 1rem;
            border-left: 3px solid #1e88e5;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong style="color: #1e88e5;">{title}</strong>
                <span style="color: #666; font-size: 0.85rem;">{time}</span>
            </div>
            <div style="color: #424242;">{description}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def custom_button(label: str, icon: str = "", bg_color: str = "#1e88e5", text_color: str = "white",
                  onclick: str = "", full_width: bool = True):
    """
    Create a custom styled button.

    Args:
        label: Button text
        icon: Icon emoji (optional)
        bg_color: Background color
        text_color: Text color
        onclick: JavaScript onclick handler
        full_width: Whether button should be full width
    """
    width = "100%" if full_width else "auto"
    icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ''

    html = f"""
    <button onclick="{onclick}" style="
        background: {bg_color};
        color: {text_color};
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        width: {width};
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)'"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'">
        {icon_html}{label}
    </button>
    """
    st.markdown(html, unsafe_allow_html=True)


def chart_card(title: str, chart_type: str = "line", data: Optional[Dict] = None, height: int = 300):
    """
    Create a card with Chart.js visualization.

    Args:
        title: Chart title
        chart_type: Type of chart (line, bar, pie, doughnut)
        data: Chart data dict
        height: Chart height in pixels
    """
    chart_id = f"chart_{hash(title)}"

    # Default data if none provided
    if data is None:
        data = {
            'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'datasets': [{
                'label': 'Sample Data',
                'data': [12, 19, 3, 5, 2, 3, 9],
                'borderColor': '#1e88e5',
                'backgroundColor': 'rgba(30, 136, 229, 0.1)',
                'tension': 0.4
            }]
        }

    import json
    data_json = json.dumps(data)

    html = f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    ">
        <h3 style="margin: 0 0 1rem 0; color: #1e88e5;">{title}</h3>
        <canvas id="{chart_id}" height="{height}"></canvas>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const ctx = document.getElementById('{chart_id}');
        new Chart(ctx, {{
            type: '{chart_type}',
            data: {data_json},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
    """
    components.html(html, height=height + 150)


def loading_spinner(message: str = "Loading..."):
    """Show an animated loading spinner."""
    html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem;">
        <div style="
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #1e88e5;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
        <p style="margin-top: 1rem; color: #666;">{message}</p>
    </div>

    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)


def badge(text: str, color: str = "#1e88e5", bg_color: str = "#e3f2fd"):
    """Create a small badge/pill."""
    html = f"""
    <span style="
        background: {bg_color};
        color: {color};
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
    ">{text}</span>
    """
    st.markdown(html, unsafe_allow_html=True)


def alert_box(message: str, alert_type: str = "info", dismissible: bool = False):
    """
    Create an alert box.

    Args:
        message: Alert message
        alert_type: Type (success, info, warning, error)
        dismissible: Whether alert can be dismissed
    """
    colors = {
        'success': {'bg': '#e8f5e9', 'border': '#4caf50', 'icon': '✅'},
        'info': {'bg': '#e3f2fd', 'border': '#1e88e5', 'icon': 'ℹ️'},
        'warning': {'bg': '#fff3e0', 'border': '#ff9800', 'icon': '⚠️'},
        'error': {'bg': '#ffebee', 'border': '#f44336', 'icon': '❌'}
    }

    style = colors.get(alert_type, colors['info'])
    dismiss_btn = """
    <button onclick="this.parentElement.style.display='none'" style="
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: #666;
    ">×</button>
    """ if dismissible else ""

    html = f"""
    <div style="
        background: {style['bg']};
        border-left: 4px solid {style['border']};
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    ">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 1.5rem;">{style['icon']}</span>
            <span>{message}</span>
        </div>
        {dismiss_btn}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
