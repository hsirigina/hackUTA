"""Supervisor dashboard for monitoring multiple drivers."""
import streamlit as st
from datetime import datetime, timedelta
from auth.session import session
from database.models import db, DrivingSession, DrivingEvent
from utils.decorators import require_supervisor


@require_supervisor
def show():
    """Display supervisor dashboard."""
    st.title("📊 Supervisor Dashboard")

    user_id = session.get_user_id()

    # Get supervised drivers
    drivers = db.get_supervised_drivers(user_id)

    if not drivers:
        st.info("👥 You don't have any drivers assigned yet.")
        st.markdown("""
        ### Getting Started

        To add drivers to your supervision:
        1. Drivers need to be registered in the system
        2. Use the 'Manage Drivers' page to link drivers to your account
        3. Or contact your administrator to assign drivers to you
        """)
        return

    # Summary metrics
    st.subheader("📈 Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Drivers", len(drivers))

    with col2:
        # Count active sessions
        db_session = db.get_session()
        active_sessions = db_session.query(DrivingSession).filter(
            DrivingSession.driver_id.in_([d.id for d in drivers]),
            DrivingSession.is_active == True
        ).count()
        db_session.close()
        st.metric("Active Drivers", active_sessions)

    with col3:
        # Count events today
        db_session = db.get_session()
        today = datetime.utcnow().date()
        events_today = db_session.query(DrivingEvent).join(DrivingSession).filter(
            DrivingSession.driver_id.in_([d.id for d in drivers]),
            DrivingEvent.timestamp >= today
        ).count()
        db_session.close()
        st.metric("Events Today", events_today)

    with col4:
        # Total distance this week
        db_session = db.get_session()
        week_ago = datetime.utcnow() - timedelta(days=7)
        total_distance = db_session.query(DrivingSession).filter(
            DrivingSession.driver_id.in_([d.id for d in drivers]),
            DrivingSession.start_time >= week_ago
        ).with_entities(db_session.query(DrivingSession.distance).label('distance')).all()
        db_session.close()

        distance_sum = sum([d[0] for d in total_distance if d[0]]) if total_distance else 0
        st.metric("Distance (7d)", f"{distance_sum:.1f} km")

    st.divider()

    # Driver list
    st.subheader("👥 Monitored Drivers")

    for driver in drivers:
        with st.expander(f"🚗 {driver.name or driver.email}", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Email:** {driver.email}")
                st.write(f"**Driver ID:** {driver.id[:20]}...")

                # Get latest session
                db_session = db.get_session()
                latest_session = db_session.query(DrivingSession).filter_by(
                    driver_id=driver.id
                ).order_by(DrivingSession.start_time.desc()).first()

                if latest_session:
                    if latest_session.is_active:
                        st.success("🟢 Currently driving")
                        st.write(f"Started: {latest_session.start_time.strftime('%Y-%m-%d %H:%M')}")
                    else:
                        st.write(f"Last drive: {latest_session.start_time.strftime('%Y-%m-%d %H:%M')}")
                        if latest_session.distance:
                            st.write(f"Distance: {latest_session.distance:.1f} km")
                else:
                    st.info("No driving sessions yet")

                db_session.close()

            with col2:
                if st.button("View Details", key=f"view_{driver.id}"):
                    st.session_state.selected_driver = driver.id
                    st.info("Detailed view coming soon...")

    st.divider()

    # Recent events across all drivers
    st.subheader("🚨 Recent Events")

    db_session = db.get_session()
    recent_events = db_session.query(DrivingEvent).join(DrivingSession).filter(
        DrivingSession.driver_id.in_([d.id for d in drivers])
    ).order_by(DrivingEvent.timestamp.desc()).limit(10).all()
    db_session.close()

    if recent_events:
        for event in recent_events:
            severity_emoji = {
                'low': '🟡',
                'medium': '🟠',
                'high': '🔴'
            }.get(event.severity, '⚪')

            # Get driver info
            driver = next((d for d in drivers if d.id == event.session.driver_id), None)
            driver_name = driver.name if driver else "Unknown"

            col1, col2, col3, col4 = st.columns([1, 2, 2, 3])

            with col1:
                st.write(severity_emoji)

            with col2:
                st.write(event.event_type.replace('_', ' ').title())

            with col3:
                st.write(driver_name)

            with col4:
                st.write(event.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    else:
        st.info("No events recorded yet")
