"""Main Streamlit application for Driving Tracker with Auth0 authentication."""
import streamlit as st
from auth.auth0_config import auth0_config
from auth.session import session
from database.models import db
from pages import supervisor_dashboard, driver_dashboard
from pages import supervisor_dashboard_modern

# Initialize session first (before page config)
# This allows us to check authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Page configuration with dynamic sidebar
st.set_page_config(
    page_title="Driving Tracker - Real-Time Driving Insights",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="auto",  # Auto-show when logged in
    menu_items={
        'Get Help': 'https://github.com/your-repo/issues',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': "# Driving Tracker\nBuilt for HackUTA with Auth0 authentication"
    }
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

            # Extract role from Auth0 custom claims or default to 'driver'
            namespace = 'https://drivingtracker.com'
            role = user_info.get(f'{namespace}/role', user_info.get('role', 'driver'))
            supervisor_id = user_info.get(f'{namespace}/supervisor_id', user_info.get('supervisor_id'))
            supervised_users = user_info.get(f'{namespace}/supervised_users', user_info.get('supervised_users', []))

            # Add to user_info for easy access
            user_info['role'] = role
            user_info['supervisor_id'] = supervisor_id
            user_info['supervised_users'] = supervised_users

            # Store user in database
            db.get_or_create_user(user_info)

            # Set session
            session.set_user(user_info, token)

            # Clear query params and redirect to clean URL
            st.query_params.clear()

            # Rerun to show authenticated state
            st.rerun()

        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            st.write("Debug info:", str(e))
            st.query_params.clear()


def login_page():
    """Display welcome/home page with embedded login."""

    # Custom CSS for better styling
    st.markdown("""
    <style>
    .big-title {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(120deg, #1e88e5, #64b5f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1e88e5;
        margin: 1rem 0;
    }
    .login-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
        margin: 2rem auto;
        max-width: 500px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown('<h1 class="big-title">🚗 Driving Tracker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Monitor and improve driving behavior with real-time insights</p>', unsafe_allow_html=True)

    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)

    # Main content in columns
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### 🎯 What We Do")
        st.markdown("""
        Track driving metrics in real-time using Arduino sensors and gain actionable
        insights into driving behavior. Perfect for parents monitoring teen drivers,
        fleet managers tracking employees, or driving instructors coaching students.
        """)

        st.markdown("### ✨ Key Features")

        st.markdown("""
        <div class="feature-box">
            <h4>📊 Real-Time Metrics</h4>
            Live tracking of speed, acceleration, location, and more from Arduino devices
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-box">
            <h4>👥 Supervisor/Driver Roles</h4>
            Multi-tier account system for parent-child or manager-employee relationships
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-box">
            <h4>📈 Detailed Analytics</h4>
            Comprehensive reports, trip history, and performance insights
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-box">
            <h4>🚨 Safety Alerts</h4>
            Instant notifications for harsh braking, speeding, and other risky behaviors
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Login Box
        st.markdown("""
        <div class="login-box">
            <h3 style="text-align: center; margin-bottom: 1.5rem;">🔐 Get Started</h3>
            <p style="text-align: center; color: #666; margin-bottom: 1.5rem;">
                Sign in with Auth0 to access your dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Login Button
        if st.button("🔐 Login / Sign Up with Auth0", use_container_width=True, type="primary"):
            # Check if we just logged out - force login prompt
            force_login = st.session_state.get('just_logged_out', False)

            authorization_url, state = auth0_config.get_authorization_url(force_login=force_login)
            st.session_state.oauth_state = state

            # Clear the logout flag
            if 'just_logged_out' in st.session_state:
                del st.session_state.just_logged_out

            st.markdown(f'<meta http-equiv="refresh" content="0;url={authorization_url}">', unsafe_allow_html=True)
            st.write("Redirecting to Auth0...")

        st.markdown("<br>", unsafe_allow_html=True)

        # Info box
        st.info("""
        **New User?**
        Click the button above to create your account through Auth0's secure authentication.

        **Existing User?**
        Use the same button to log in.
        """)

        # Demo credentials (for testing)
        with st.expander("🧪 Demo Credentials"):
            st.markdown("""
            **Supervisor Account:**
            - Email: `supervisor@test.com`
            - Password: `Test1234!`

            **Driver Account:**
            - Email: `driver@test.com`
            - Password: `Test1234!`
            """)

    # Footer section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🏆 Use Cases")
        st.markdown("""
        - 👨‍👩‍👧 Parents & Teen Drivers
        - 🚛 Fleet Management
        - 🏫 Driving Schools
        - 🏢 Corporate Fleets
        """)

    with col2:
        st.markdown("### 🔒 Security")
        st.markdown("""
        - Auth0 Authentication
        - End-to-end Encryption
        - Role-based Access
        - Secure API Keys
        """)

    with col3:
        st.markdown("### 🎓 About")
        st.markdown("""
        Built for **HackUTA** using:
        - Streamlit
        - Auth0
        - Arduino IoT
        - Real-time Analytics
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("🔐 Powered by Auth0 • Built with ❤️ for HackUTA")


def main_app():
    """Main application after authentication."""
    # Sidebar
    with st.sidebar:
        st.title("🚗 Driving Tracker")

        user_name = session.get_user_name()
        user_role = session.get_user_role()

        # User info box
        st.markdown(f"""
        <div style="background: #f0f2f6; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <div style="font-weight: 600; font-size: 1.1rem;">{user_name}</div>
            <div style="color: #666; font-size: 0.9rem;">Role: {user_role.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)

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

        # Logout button (prominent)
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            # Set flag to force login prompt after logout
            st.session_state.just_logged_out = True

            # Clear session
            logout_url = session.logout()

            # Redirect to Auth0 logout, then back to home
            st.markdown(f'<meta http-equiv="refresh" content="0;url={logout_url}">', unsafe_allow_html=True)
            st.rerun()

        # Quick logout helper text
        st.caption("Click logout to test different accounts")

    # Main content area
    if session.is_supervisor():
        if "Dashboard" in page:
            supervisor_dashboard_modern.show()
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
