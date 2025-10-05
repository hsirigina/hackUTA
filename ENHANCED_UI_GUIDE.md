# 🎨 Enhanced UI Components Guide

## What's New?

Your Streamlit app now has **custom HTML/CSS/JavaScript components** for a professional, modern look!

## 🚀 New Components Available

### 1. **Metric Cards** 📊
Beautiful animated cards for displaying metrics with icons and colors.

```python
from components.ui_components import metric_card

metric_card(
    title="Total Drivers",
    value="25",
    delta="+5",  # Optional change indicator
    icon="👥",
    color="#1e88e5"
)
```

**Features:**
- ✨ Hover animations
- 🎨 Custom colors
- 📈 Delta indicators (up/down arrows)
- 🎯 Professional gradients

---

### 2. **Stat Card Row** 📈
Display multiple metrics in a row.

```python
from components.ui_components import stat_card_row

stat_card_row([
    {'title': 'Active Users', 'value': '142', 'icon': '🚗', 'color': '#4caf50'},
    {'title': 'Events', 'value': '23', 'icon': '🚨', 'color': '#ff9800'},
    {'title': 'Distance', 'value': '1.2k km', 'icon': '📍', 'color': '#9c27b0'}
])
```

---

### 3. **Info Cards** ℹ️
Display information in styled boxes.

```python
from components.ui_components import info_card

info_card(
    title="Welcome!",
    content="This is your dashboard. <strong>Get started</strong> by...",
    icon="👋",
    bg_color="#e3f2fd"
)
```

---

### 4. **Progress Rings** 🎯
Animated circular progress indicators.

```python
from components.ui_components import progress_ring

progress_ring(
    percentage=75,
    label="Safety Score",
    color="#4caf50",
    size=120
)
```

**Perfect for:**
- Safety scores
- Completion rates
- Performance metrics

---

### 5. **Timeline** 📅
Visual timeline for events.

```python
from components.ui_components import timeline_item

timeline_item(
    title="Trip Started",
    time="10:30 AM",
    description="Driver began journey from Downtown",
    icon="🚗",
    is_last=False
)
```

---

### 6. **Interactive Charts** 📊
Beautiful charts using Chart.js.

```python
from components.ui_components import chart_card

chart_card(
    title="Weekly Driving Activity",
    chart_type="line",  # or "bar", "pie", "doughnut"
    data={
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'datasets': [{
            'label': 'Distance (km)',
            'data': [45, 38, 52, 41, 48, 62, 55],
            'borderColor': '#1e88e5',
            'backgroundColor': 'rgba(30, 136, 229, 0.1)'
        }]
    },
    height=300
)
```

**Chart Types:**
- 📈 Line charts
- 📊 Bar charts
- 🍩 Pie/Doughnut charts
- 📉 Area charts

---

### 7. **Alert Boxes** 🚨
Styled alerts for messages.

```python
from components.ui_components import alert_box

alert_box(
    message="New safety event detected!",
    alert_type="warning",  # success, info, warning, error
    dismissible=True
)
```

---

### 8. **Badges** 🏷️
Small tags/labels.

```python
from components.ui_components import badge

badge("Active", color="#4caf50", bg_color="#e8f5e9")
badge("Premium", color="#ff9800", bg_color="#fff3e0")
```

---

### 9. **Loading Spinner** ⏳
Animated loading indicator.

```python
from components.ui_components import loading_spinner

loading_spinner("Loading dashboard data...")
```

---

### 10. **Custom Buttons** 🔘
Styled buttons with hover effects.

```python
from components.ui_components import custom_button

custom_button(
    label="Start Session",
    icon="🚗",
    bg_color="#4caf50",
    text_color="white",
    onclick="alert('Session started!')",
    full_width=True
)
```

---

## 🎨 Color Palette

Use these colors for consistency:

```python
COLORS = {
    'primary': '#1e88e5',    # Blue
    'success': '#4caf50',    # Green
    'warning': '#ff9800',    # Orange
    'error': '#f44336',      # Red
    'purple': '#9c27b0',     # Purple
    'grey': '#757575'        # Grey
}
```

---

## 🚀 How to Use

### 1. Import Components
```python
from components.ui_components import (
    metric_card,
    stat_card_row,
    info_card,
    chart_card,
    alert_box,
    badge,
    timeline_item,
    progress_ring,
    loading_spinner,
    custom_button
)
```

### 2. Use in Your Dashboards
```python
def my_dashboard():
    st.title("My Dashboard")

    # Show metrics
    stat_card_row([
        {'title': 'Users', 'value': '100', 'icon': '👥', 'color': '#1e88e5'},
        {'title': 'Active', 'value': '75', 'icon': '🚗', 'color': '#4caf50'}
    ])

    # Show chart
    chart_card(
        title="Activity",
        chart_type="bar",
        data={...}
    )

    # Show alerts
    alert_box("System update available", alert_type="info")
```

---

## ✨ What Changed?

### **Supervisor Dashboard**
- ✅ New metric cards with icons and colors
- ✅ Hover animations
- ✅ Better visual hierarchy
- ✅ Professional gradients

### **Driver Dashboard** (Coming next)
- 📊 Interactive charts
- 🎯 Progress rings for scores
- 📅 Timeline for trip history
- 🚨 Alert boxes for events

### **Home Page** (Coming next)
- 🎨 Enhanced hero section
- 💫 Smooth animations
- 🔥 Modern card layouts
- ✨ Better call-to-actions

---

## 🔧 Advanced Customization

### Custom HTML/CSS
All components support custom HTML and CSS. You can modify:

**In `components/ui_components.py`:**
- Edit the HTML structure
- Change CSS styles
- Add JavaScript interactions
- Customize animations

### Example: Custom Metric Card
```python
def my_custom_card(value):
    html = f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    ">
        <h2>{value}</h2>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
```

---

## 📚 Resources

### **Chart.js Documentation**
- https://www.chartjs.org/docs/latest/

### **CSS Gradients**
- https://cssgradient.io/

### **Color Palettes**
- https://coolors.co/

### **Icons & Emojis**
- Use Unicode emojis: 🚗 🚨 📊 📈 👥
- Or integrate Font Awesome/Material Icons

---

## 🎯 Next Steps

1. **Test the components** - See them in action
2. **Customize colors** - Match your brand
3. **Add more charts** - Visualize your data
4. **Create new components** - Build what you need

---

## 🚀 Running the Enhanced App

```bash
cd /Users/harsh/Documents/GitHub/hackUTA
streamlit run app.py
```

Open http://localhost:8501 and see the new UI! 🎉

---

## 💡 Tips

1. **Use consistent colors** - Stick to the palette
2. **Don't overdo animations** - Keep it subtle
3. **Test responsiveness** - Check on mobile
4. **Keep it fast** - Don't use too many heavy components on one page

---

**Your app now looks professional and modern!** 🚀✨
