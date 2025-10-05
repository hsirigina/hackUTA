"""Demo page showcasing all custom UI components."""
import streamlit as st
from components.ui_components import (
    metric_card, stat_card_row, info_card, chart_card, alert_box,
    badge, timeline_item, progress_ring, loading_spinner, custom_button
)

st.set_page_config(page_title="Component Demo", page_icon="🎨", layout="wide")

st.title("🎨 Enhanced UI Components Demo")
st.markdown("Preview all the custom components available in your app!")

st.divider()

# 1. Metric Cards
st.header("1. Metric Cards 📊")
st.markdown("Beautiful animated cards for displaying metrics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Single Card")
    metric_card(
        title="Active Users",
        value="1,234",
        delta="+12%",
        icon="👥",
        color="#1e88e5"
    )

with col2:
    st.subheader("Different Colors")
    metric_card(
        title="Revenue",
        value="$45.2K",
        delta="+8.5%",
        icon="💰",
        color="#4caf50"
    )

st.divider()

# 2. Stat Card Row
st.header("2. Stat Card Row 📈")
st.markdown("Multiple metrics in a row")

stat_card_row([
    {'title': 'Total Drivers', 'value': '125', 'icon': '🚗', 'color': '#1e88e5'},
    {'title': 'Active Now', 'value': '42', 'icon': '🟢', 'color': '#4caf50'},
    {'title': 'Events Today', 'value': '18', 'delta': '+5', 'icon': '🚨', 'color': '#ff9800'},
    {'title': 'Distance', 'value': '2.1k km', 'icon': '📍', 'color': '#9c27b0'}
])

st.divider()

# 3. Info Cards
st.header("3. Info Cards ℹ️")

col1, col2 = st.columns(2)

with col1:
    info_card(
        title="Getting Started",
        content="Welcome to your dashboard! <strong>Here's how to begin:</strong><br>1. Connect your device<br>2. Start tracking<br>3. View insights",
        icon="🚀",
        bg_color="#e3f2fd"
    )

with col2:
    info_card(
        title="Pro Tip",
        content="Use keyboard shortcuts to navigate faster. Press <code>?</code> for help.",
        icon="💡",
        bg_color="#fff3e0"
    )

st.divider()

# 4. Progress Rings
st.header("4. Progress Rings 🎯")
st.markdown("Circular progress indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    progress_ring(85, "Safety Score", "#4caf50", 120)

with col2:
    progress_ring(72, "Completion", "#1e88e5", 120)

with col3:
    progress_ring(94, "Performance", "#ff9800", 120)

with col4:
    progress_ring(60, "Efficiency", "#9c27b0", 120)

st.divider()

# 5. Charts
st.header("5. Interactive Charts 📊")

col1, col2 = st.columns(2)

with col1:
    chart_card(
        title="Weekly Activity",
        chart_type="line",
        data={
            'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'datasets': [{
                'label': 'Distance (km)',
                'data': [45, 52, 38, 48, 55, 62, 48],
                'borderColor': '#1e88e5',
                'backgroundColor': 'rgba(30, 136, 229, 0.1)',
                'tension': 0.4
            }]
        },
        height=250
    )

with col2:
    chart_card(
        title="Event Distribution",
        chart_type="doughnut",
        data={
            'labels': ['Safe Driving', 'Harsh Brake', 'Speeding', 'Sharp Turn'],
            'datasets': [{
                'data': [65, 15, 12, 8],
                'backgroundColor': ['#4caf50', '#ff9800', '#f44336', '#9c27b0']
            }]
        },
        height=250
    )

st.divider()

# 6. Alert Boxes
st.header("6. Alert Boxes 🚨")

col1, col2 = st.columns(2)

with col1:
    alert_box("Operation completed successfully!", "success", dismissible=True)
    alert_box("Please review the new updates.", "info", dismissible=True)

with col2:
    alert_box("Warning: High speed detected!", "warning", dismissible=True)
    alert_box("Error: Connection failed. Please retry.", "error", dismissible=True)

st.divider()

# 7. Badges
st.header("7. Badges 🏷️")

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("**Status Badges:**")

with col2:
    badge("Active", "#4caf50", "#e8f5e9")
    badge("Premium", "#ff9800", "#fff3e0")
    badge("Verified", "#1e88e5", "#e3f2fd")
    badge("Beta", "#9c27b0", "#f3e5f5")
    badge("New", "#f44336", "#ffebee")

st.divider()

# 8. Timeline
st.header("8. Timeline 📅")

timeline_item("Trip Started", "10:30 AM", "Driver began journey from Downtown", "🚗", False)
timeline_item("Speed Alert", "10:45 AM", "Vehicle exceeded speed limit on Highway 101", "⚠️", False)
timeline_item("Rest Stop", "11:15 AM", "15-minute break at Service Plaza", "☕", False)
timeline_item("Trip Ended", "12:00 PM", "Arrived at destination safely", "✅", True)

st.divider()

# 9. Custom Buttons
st.header("9. Custom Buttons 🔘")

col1, col2, col3 = st.columns(3)

with col1:
    custom_button("Start Session", "🚗", "#4caf50", "white", "alert('Started!')", True)

with col2:
    custom_button("View Report", "📊", "#1e88e5", "white", "alert('Report!')", True)

with col3:
    custom_button("Download", "⬇️", "#9c27b0", "white", "alert('Download!')", True)

st.divider()

# 10. Loading Spinner
st.header("10. Loading Spinner ⏳")

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("Show Loading"):
        with col2:
            loading_spinner("Loading dashboard data...")
            import time
            time.sleep(2)
            st.success("Loaded!")

st.divider()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎨 These components are now available throughout your app!</p>
    <p>Use them in dashboards, pages, and anywhere you need enhanced UI.</p>
    <p><strong>Check ENHANCED_UI_GUIDE.md for usage instructions</strong></p>
</div>
""", unsafe_allow_html=True)
