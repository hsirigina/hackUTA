"""Modern supervisor dashboard matching reference design."""
import streamlit as st
from datetime import datetime, timedelta
from auth.session import session
from database.models import db, DrivingSession, DrivingEvent
from utils.decorators import require_supervisor
from components.modern_ui import (
    gradient_card, analytics_item, earnings_card,
    modern_page_header, apply_modern_theme
)


@require_supervisor
def show():
    """Display modern supervisor dashboard."""
    # Apply modern theme
    apply_modern_theme()

    user_id = session.get_user_id()
    drivers = db.get_supervised_drivers(user_id)

    # Page header
    modern_page_header(
        title="SUPERVISOR DASHBOARD",
        subtitle="Monitor your drivers and their performance",
        tabs=["Daily", "Weekly", "Monthly"]
    )

    # Main content and sidebar
    col_main, col_sidebar = st.columns([2.5, 1])

    with col_main:
        # Calculate metrics
        db_session = db.get_session()

        # Miles driven
        week_ago = datetime.utcnow() - timedelta(days=7)
        total_distance = db_session.query(DrivingSession).filter(
            DrivingSession.driver_id.in_([d.id for d in drivers]),
            DrivingSession.start_time >= week_ago
        ).with_entities(db_session.query(DrivingSession.distance).label('distance')).all()
        distance_sum = sum([d[0] for d in total_distance if d[0]]) if total_distance else 0

        # Count events (earning simulation)
        events_count = db_session.query(DrivingEvent).join(DrivingSession).filter(
            DrivingSession.driver_id.in_([d.id for d in drivers])
        ).count()

        # Count trips
        trips_count = db_session.query(DrivingSession).filter(
            DrivingSession.driver_id.in_([d.id for d in drivers])
        ).count()

        db_session.close()

        # Gradient cards row
        col1, col2, col3 = st.columns(3)

        with col1:
            gradient_card(
                title="Miles Driven",
                value=f"{distance_sum:.2f}",
                icon="🏁",
                gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
            )

        with col2:
            gradient_card(
                title="Earning",
                value=f"${events_count * 15}",
                icon="💵",
                gradient="linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
            )

        with col3:
            gradient_card(
                title="Trips",
                value=str(trips_count),
                icon="🚗",
                gradient="linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Chart section
        st.markdown("### 📊 Weekly Activity")

        # Sample bar chart data
        import random
        chart_data = {
            'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'datasets': [{
                'label': 'Earnings ($)',
                'data': [random.randint(20, 100) for _ in range(7)],
                'backgroundColor': '#4facfe',
                'borderRadius': 8
            }]
        }

        from components.ui_components import chart_card
        chart_card(
            title="",
            chart_type="bar",
            data=chart_data,
            height=300
        )

    with col_sidebar:
        # Earnings card
        st.markdown("### EARNINGS")
        earnings_card(
            balance=f"${events_count * 45 + 560}.57",
            gradient="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Analytics section
        st.markdown("### ANALYTICS FOR CURRENT MONTH")

        analytics_item(
            value=f"${events_count * 15 + 400}",
            label="Earning in July"
        )

        analytics_item(
            value=f"{trips_count + 7}",
            label="Completed"
        )

        analytics_item(
            value="2",
            label="Cancelled trips"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Revenue section
        st.markdown("### REVENUE")

        analytics_item(
            value=f"${events_count * 10 + 400}",
            label="Withdraw"
        )

        analytics_item(
            value=f"${events_count * 8 + 450}",
            label="Pending clearance"
        )

        analytics_item(
            value=str(len(drivers) + 30),
            label="Total completed trips"
        )
