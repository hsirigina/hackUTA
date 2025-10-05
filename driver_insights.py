# tesla_sleek_dashboard_v2.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components


st.set_page_config(page_title="Tesla Style Driving Dashboard", layout="wide")

# -------------------------
# Custom CSS for sleek Tesla UI
# -------------------------
st.markdown("""
<style>
body {background-color:#0d0d0d; color:#fff; font-family: 'Roboto', sans-serif;}
.metric-grid {display:flex; justify-content:space-between; gap:20px; margin-top:30px;}
.metric-card {flex:1; background:#1c1c1c; border-radius:20px; padding:20px; box-shadow:0px 6px 25px rgba(0,0,0,0.5);}
.metric-title {color:#aaa; font-size:14px; margin-bottom:5px; letter-spacing:1px;}
.metric-value {font-size:32px; font-weight:bold; margin-bottom:5px;}
.sparkline {width:100%; height:40px;}
.safety-container {width:100%; background:#1a1a1a; border-radius:20px; height:50px; margin-bottom:10px; box-shadow:0px 4px 20px rgba(0,0,0,0.6);}
.safety-fill {height:100%; border-radius:20px; line-height:50px; color:#fff; font-size:24px; font-weight:800; text-align:center; transition: width 0.8s ease-in-out;}
.current-speed {font-size:28px; font-weight:bold; text-align:center; margin:15px 0; color:#00ff99;}
</style>
""", unsafe_allow_html=True)

# Page title
title_html = """
<div style='display:flex; justify-content:center; margin-top:10px;'>
  <h1 style="color:#ffffff; font-family: 'Roboto', sans-serif; font-weight:200; letter-spacing:1px; margin:0;">Driver A's Current Drive</h1>
</div>
"""

st.markdown(title_html, unsafe_allow_html=True)
# st.title("Driver A's Current Drive")

# -------------------------
# Session state for data
# -------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["timestamp","accel","gyro","hard_brake","sharp_turn","agg_accel","speed"])

# -------------------------
# Fake data generator
# -------------------------
def generate_mock_data(prev_speed=30):
    # acceleration in g's
    accel = np.random.randn()*0.3
    gyro = np.random.randn()*2
    
    hard_brake = accel < -0.5
    sharp_turn = abs(gyro) > 15
    aggressive_accel = accel > 0.5
    
    # simple speed integration in MPH
    delta_speed = accel * 3.6  # scaling factor to simulate MPH change
    speed = max(0, prev_speed + delta_speed)
    
    return {"timestamp":datetime.now(timezone.utc),
            "accel":accel,"gyro":gyro,
            "hard_brake":hard_brake,"sharp_turn":sharp_turn,
            "agg_accel":aggressive_accel,"speed":speed}

# Append new data
prev_speed = st.session_state.data["speed"].iloc[-1] if len(st.session_state.data)>0 else 30
new_data = generate_mock_data(prev_speed)
st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_data])], ignore_index=True).tail(100)

# -------------------------
# Compute Safety Score
# -------------------------
def compute_safety_score(df):
    score = 100
    score -= df["hard_brake"].sum()*5
    score -= df["sharp_turn"].sum()*3
    score -= df["agg_accel"].sum()*3
    return max(0,int(score))

score = compute_safety_score(st.session_state.data)

# -------------------------
# Safety Score bar (solid color)
# -------------------------
if score >= 85:
    color = "#00ff99"
elif score >=70:
    color = "#ffff66"
else:
    color = "#ff4d4d"

# st.markdown(f"""
# <div class="safety-container">
#   <div class="safety-fill" style="width:{score}%; background:{color};">{score}</div>
# </div>
# """, unsafe_allow_html=True)

# -------------------------
# Speedometer Display
# -------------------------
current_speed = st.session_state.data["speed"].iloc[-1]
max_speed = 120  # realistic max for gauge

needle_angle = (current_speed / max_speed) * 180 - 90
arc_progress = (current_speed / max_speed) * 360

speedometer_html = f"""
<div style="display:flex; justify-content:center; align-items:center; margin:30px 0;">
  <div style="position: relative; width: 250px; height: 125px;">
    <!-- Arc Background -->
    <svg viewBox="0 0 250 125" style="position:absolute; top:0; left:0;">
      <path d="M10,125 A115,115 0 0,1 240,125" fill="none" stroke="#333" stroke-width="20"/>
      <path d="M10,125 A115,115 0 0,1 240,125" fill="none" stroke="#00ff99" stroke-width="20"
        stroke-dasharray="{arc_progress} 360" stroke-linecap="round"/>
    </svg>

    <!-- Needle -->
    <div style="
      position: absolute;
      bottom: 0;
      left: 50%;
      width: 4px;
      height: 110px;
      background: #ff4d4d;
      transform-origin: bottom center;
      transform: rotate({needle_angle}deg);
      transition: transform 0.5s ease-in-out;
    "></div>

    <!-- Speed Label -->
    <div style="
      position:absolute;
      bottom:-50px;
      left:50%;
      transform:translateX(-50%);
      font-size:32px;
      font-weight:bold;
      color:#fff;
    ">{current_speed:.0f}</div>

    <!-- Units -->
    <div style="
      position:absolute;
      bottom:-80px;
      left:50%;
      transform:translateX(-50%);
      font-size:14px;
      color:#aaa;
      letter-spacing:1px;
    ">MPH</div>
  </div>
</div>
"""

# st.markdown(speedometer_html, unsafe_allow_html=True)
components.html(speedometer_html, height=260)

# -------------------------
# Sparkline generator
# -------------------------
def sparkline(data):
    points = " ".join([f"{i},{10-(d*5):.1f}" for i,d in enumerate(data)])
    return f"<svg class='sparkline' viewBox='0 0 100 20' preserveAspectRatio='none'><polyline fill='none' stroke='#00ff99' stroke-width='2' points='{points}'/></svg>"

# -------------------------
# Metric tiles
# -------------------------
tiles_html = f"""
<div class="metric-grid">
  <div class="metric-card">
    <div class="metric-title">Hard Brakes</div>
    <div class="metric-value red">{st.session_state.data['hard_brake'].sum()}</div>
    {sparkline(st.session_state.data['hard_brake'].astype(int).tolist())}
  </div>
  <div class="metric-card">
    <div class="metric-title">Sharp Turns</div>
    <div class="metric-value yellow">{st.session_state.data['sharp_turn'].sum()}</div>
    {sparkline(st.session_state.data['sharp_turn'].astype(int).tolist())}
  </div>
  <div class="metric-card">
    <div class="metric-title">Aggressive Acceleration</div>
    <div class="metric-value red">{st.session_state.data['agg_accel'].sum()}</div>
    {sparkline(st.session_state.data['agg_accel'].astype(int).tolist())}
  </div>
</div>
"""
st.markdown(tiles_html, unsafe_allow_html=True)

# -------------------------
# Auto-refresh every 1 second
# -------------------------
st_autorefresh(interval=1000, key="dashboard_refresh")

# -------------------------
# Centered numeric safety score beneath the metric cards
# -------------------------
score_html = f"""
<div style='display:flex; justify-content:center; margin-top:75px;'>
  <div style='background:transparent; text-align:center;'>
    <div style='font-size:60px; font-weight:900; color:{color}; line-height:1; letter-spacing:2px;'>{score}</div>
    <div style='font-size:14px; color:#aaa; margin-top:6px; letter-spacing:1px;'>Overall Driver Safety Score</div>
  </div>
</div>
"""

st.markdown(score_html, unsafe_allow_html=True)


# -------------------------
# Driver camera (webcam) preview
# -------------------------
# Driver camera preview removed by request.
