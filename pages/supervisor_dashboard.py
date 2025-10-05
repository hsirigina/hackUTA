"""Supervisor dashboard for monitoring multiple drivers."""
import streamlit as st
from datetime import datetime, timedelta
from auth.session import session
from database.models import db, DrivingSession, DrivingEvent
from utils.decorators import require_supervisor
from components.ui_components import metric_card, stat_card_row, info_card, chart_card, alert_box


@require_supervisor
def show():
    """Display supervisor dashboard."""
    st.title("📊 Supervisor Dashboard")

    user_id = session.get_user_id()

    # Get supervised drivers
    drivers = db.get_supervised_drivers(user_id)

    if not drivers:
        info_card(
            title="No Drivers Assigned",
            content="""
            <p>You don't have any drivers assigned yet.</p>
            <p><strong>To add drivers to your supervision:</strong></p>
            <ol>
                <li>Drivers need to be registered in the system</li>
                <li>Use the 'Manage Drivers' page to link drivers to your account</li>
                <li>Or contact your administrator to assign drivers to you</li>
            </ol>
            """,
            icon="👥",
            bg_color="#fff3e0"
        )
        return

    # Calculate metrics
    db_session = db.get_session()

    # Count active sessions
    active_sessions = db_session.query(DrivingSession).filter(
        DrivingSession.driver_id.in_([d.id for d in drivers]),
        DrivingSession.is_active == True
    ).count()

    # Count events today
    today = datetime.utcnow().date()
    events_today = db_session.query(DrivingEvent).join(DrivingSession).filter(
        DrivingSession.driver_id.in_([d.id for d in drivers]),
        DrivingEvent.timestamp >= today
    ).count()

    # Total distance this week
    week_ago = datetime.utcnow() - timedelta(days=7)
    total_distance = db_session.query(DrivingSession).filter(
        DrivingSession.driver_id.in_([d.id for d in drivers]),
        DrivingSession.start_time >= week_ago
    ).with_entities(db_session.query(DrivingSession.distance).label('distance')).all()

    distance_sum = sum([d[0] for d in total_distance if d[0]]) if total_distance else 0

    db_session.close()

    # Display enhanced metric cards
    st.markdown("### 📈 Overview")
    stat_card_row([
        {
            'title': 'Total Drivers',
            'value': str(len(drivers)),
            'icon': '👥',
            'color': '#1e88e5'
        },
        {
            'title': 'Active Now',
            'value': str(active_sessions),
            'icon': '🚗',
            'color': '#4caf50'
        },
        {
            'title': 'Events Today',
            'value': str(events_today),
            'delta': '+3' if events_today > 0 else None,
            'icon': '🚨',
            'color': '#ff9800'
        },
        {
            'title': 'Distance (7d)',
            'value': f'{distance_sum:.0f} km',
            'icon': '📍',
            'color': '#9c27b0'
        }
    ])

    st.markdown("<br>", unsafe_allow_html=True)

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
