"""Driver dashboard for viewing personal driving statistics."""
import streamlit as st
from datetime import datetime, timedelta
from auth.session import session
from database.models import db, DrivingSession, DrivingEvent, DrivingMetric
from utils.decorators import require_driver


@require_driver
def show():
    """Display driver dashboard."""
    st.title("📊 My Driving Dashboard")

    user_id = session.get_user_id()
    user_name = session.get_user_name()

    st.write(f"Welcome, **{user_name}**!")

    # Check if user has a supervisor
    supervisor_id = session.get_supervisor_id()
    if supervisor_id:
        st.info("👁️ Your driving is being monitored by your supervisor")

    # Get current session status
    db_session = db.get_session()
    active_session = db_session.query(DrivingSession).filter_by(
        driver_id=user_id,
        is_active=True
    ).first()

    if active_session:
        st.success("🟢 Currently Driving")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Started:** {active_session.start_time.strftime('%H:%M:%S')}")
        with col2:
            duration = (datetime.utcnow() - active_session.start_time).seconds // 60
            st.write(f"**Duration:** {duration} minutes")

        if st.button("🛑 End Session", type="primary"):
            active_session.is_active = False
            active_session.end_time = datetime.utcnow()
            active_session.duration = (active_session.end_time - active_session.start_time).seconds
            db_session.commit()
            st.rerun()
    else:
        if st.button("🚗 Start Driving Session", type="primary"):
            new_session = DrivingSession(
                driver_id=user_id,
                start_time=datetime.utcnow(),
                is_active=True
            )
            db_session.add(new_session)
            db_session.commit()
            st.rerun()

    db_session.close()

    st.divider()

    # Statistics
    st.subheader("📈 Your Statistics")

    # Time period selector
    period = st.selectbox("Time Period", ["Today", "Last 7 Days", "Last 30 Days", "All Time"])

    # Calculate date range
    now = datetime.utcnow()
    if period == "Today":
        start_date = now.replace(hour=0, minute=0, second=0)
    elif period == "Last 7 Days":
        start_date = now - timedelta(days=7)
    elif period == "Last 30 Days":
        start_date = now - timedelta(days=30)
    else:
        start_date = datetime(2000, 1, 1)

    # Query sessions
    db_session = db.get_session()
    sessions = db_session.query(DrivingSession).filter(
        DrivingSession.driver_id == user_id,
        DrivingSession.start_time >= start_date
    ).all()

    # Calculate metrics
    total_sessions = len(sessions)
    total_distance = sum([s.distance for s in sessions if s.distance])
    total_duration = sum([s.duration for s in sessions if s.duration]) // 3600  # hours

    # Count events
    events = db_session.query(DrivingEvent).join(DrivingSession).filter(
        DrivingSession.driver_id == user_id,
        DrivingEvent.timestamp >= start_date
    ).all()

    total_events = len(events)
    high_severity = len([e for e in events if e.severity == 'high'])

    db_session.close()

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Trips", total_sessions)

    with col2:
        st.metric("Distance", f"{total_distance:.1f} km")

    with col3:
        st.metric("Drive Time", f"{total_duration} hrs")

    with col4:
        st.metric("Safety Events", total_events, delta=f"{high_severity} high" if high_severity > 0 else None)

    st.divider()

    # Recent sessions
    st.subheader("🚗 Recent Trips")

    if sessions:
        for session_item in sorted(sessions, key=lambda x: x.start_time, reverse=True)[:5]:
            with st.expander(
                f"{session_item.start_time.strftime('%Y-%m-%d %H:%M')} - "
                f"{session_item.distance:.1f} km" if session_item.distance else "In Progress",
                expanded=False
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Start:** {session_item.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    if session_item.end_time:
                        st.write(f"**End:** {session_item.end_time.strftime('%Y-%m-%d %H:%M:%S')}")

                with col2:
                    if session_item.duration:
                        st.write(f"**Duration:** {session_item.duration // 60} min")
                    if session_item.distance:
                        st.write(f"**Distance:** {session_item.distance:.2f} km")

                # Show events for this session
                session_events = [e for e in events if e.session_id == session_item.id]
                if session_events:
                    st.write("**Events:**")
                    for event in session_events:
                        severity_emoji = {'low': '🟡', 'medium': '🟠', 'high': '🔴'}.get(event.severity, '⚪')
                        st.write(f"{severity_emoji} {event.event_type.replace('_', ' ').title()} - {event.timestamp.strftime('%H:%M:%S')}")
    else:
        st.info("No trips recorded yet. Start a driving session to begin tracking!")

    st.divider()

    # Safety tips
    st.subheader("💡 Safety Tips")

    tips = [
        "🚦 Always maintain safe following distance",
        "⚡ Avoid harsh acceleration and braking",
        "🛣️ Observe speed limits",
        "👀 Stay alert and avoid distractions",
        "🌧️ Adjust speed for weather conditions"
    ]

    for tip in tips:
        st.write(tip)
