"""Main Streamlit application for Driving Tracker with Auth0 authentication."""
import streamlit as st
from auth.auth0_config import auth0_config
from auth.session import session
from database.models import db
from pages import supervisor_dashboard, driver_dashboard

# Page configuration
st.set_page_config(
    page_title="Driving Tracker",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db.create_tables()

# Initialize session
session.init_session()


def handle_callback():
    """Handle OAuth callback from Auth0."""
    query_params = st.query_params

    if 'code' in query_params:
        try:
            # Get the full callback URL
            callback_url = f"{auth0_config.callback_url}?code={query_params['code']}"
            if 'state' in query_params:
                callback_url += f"&state={query_params['state']}"

            # Exchange code for token
            token = auth0_config.exchange_code_for_token(callback_url)

            # Get user info
            user_info = auth0_config.get_user_info(token)

            # For now, extract role from user_info or default to 'driver'
            # In production, you'd fetch this from Auth0 user metadata
            role = user_info.get('role', 'driver')
            user_info['role'] = role

            # Store user in database
            db.get_or_create_user(user_info)

            # Set session
            session.set_user(user_info, token)

            # Clear query params
            st.query_params.clear()

            # Rerun to show authenticated state
            st.rerun()

        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            st.query_params.clear()


def login_page():
    """Display login page."""
    st.title("🚗 Driving Tracker")
    st.subheader("Monitor and improve driving behavior")

    st.markdown("""
    ### Welcome to Driving Tracker

    Track driving metrics in real-time and gain insights into driving behavior.

    **Features:**
    - 📊 Real-time driving metrics from Arduino
    - 👥 Supervisor/Driver relationship management
    - 📈 Detailed analytics and reports
    - 🚨 Event alerts (harsh braking, speeding, etc.)
    """)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("🔐 Login with Auth0", use_container_width=True, type="primary"):
            authorization_url, state = auth0_config.get_authorization_url()
            st.session_state.oauth_state = state
            st.markdown(f'<meta http-equiv="refresh" content="0;url={authorization_url}">', unsafe_allow_html=True)
            st.write("Redirecting to Auth0...")


def main_app():
    """Main application after authentication."""
    # Sidebar
    with st.sidebar:
        st.title("🚗 Driving Tracker")

        user_name = session.get_user_name()
        user_role = session.get_user_role()

        st.write(f"**{user_name}**")
        st.write(f"*{user_role.capitalize()}*")

        st.divider()

        # Navigation based on role
        if session.is_supervisor():
            page = st.radio(
                "Navigation",
                ["📊 Dashboard", "👥 Manage Drivers", "⚙️ Settings"],
                label_visibility="collapsed"
            )
        else:
            page = st.radio(
                "Navigation",
                ["📊 My Dashboard", "📈 My Stats", "⚙️ Settings"],
                label_visibility="collapsed"
            )

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            logout_url = session.logout()
            st.markdown(f'<meta http-equiv="refresh" content="0;url={logout_url}">', unsafe_allow_html=True)
            st.rerun()

    # Main content area
    if session.is_supervisor():
        if "Dashboard" in page:
            supervisor_dashboard.show()
        elif "Manage Drivers" in page:
            st.title("👥 Manage Drivers")
            st.info("Driver management interface coming soon...")
        elif "Settings" in page:
            st.title("⚙️ Settings")
            st.info("Settings interface coming soon...")
    else:
        if "Dashboard" in page:
            driver_dashboard.show()
        elif "Stats" in page:
            st.title("📈 My Stats")
            st.info("Statistics interface coming soon...")
        elif "Settings" in page:
            st.title("⚙️ Settings")
            st.info("Settings interface coming soon...")


def main():
    """Main application entry point."""
    # Handle OAuth callback
    handle_callback()

    # Show appropriate page based on authentication status
    if session.is_authenticated():
        main_app()
    else:
        login_page()


if __name__ == "__main__":
    main()
