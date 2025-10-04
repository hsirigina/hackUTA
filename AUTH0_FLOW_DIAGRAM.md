# 🔄 Auth0 Authentication Flow

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY                             │
└─────────────────────────────────────────────────────────────────┘

1. User Opens App
   ↓
┌──────────────────┐
│  Streamlit App   │  http://localhost:8501
│  (Login Page)    │
└──────────────────┘
   ↓ [Click "Login with Auth0"]
   ↓
┌──────────────────┐
│  Auth0 Login     │  https://your-tenant.us.auth0.com
│  (Universal      │  - User enters email/password
│   Login Page)    │  - Auth0 validates credentials
└──────────────────┘
   ↓ [Login Success]
   ↓
┌──────────────────┐
│  Auth0 Actions   │  - Runs "Add User Metadata" action
│  (Post-Login)    │  - Adds role, supervisor_id to token
└──────────────────┘
   ↓
   ↓ [Redirect with code]
   ↓
┌──────────────────┐
│  Streamlit App   │  http://localhost:8501/callback?code=xxx
│  (Callback)      │  - Exchanges code for token
│                  │  - Gets user info
└──────────────────┘
   ↓
   ↓ [Set session & redirect]
   ↓
┌──────────────────┐
│  Dashboard       │  Role-based dashboard
│  (Authenticated) │  - Supervisor → Monitor drivers
│                  │  - Driver → Personal stats
└──────────────────┘
```

## Authentication Components

### 1. Auth0 Tenant
```
Your Tenant: your-name-hackuta.us.auth0.com
├── Application: "Driving Tracker"
│   ├── Client ID: abc123...
│   ├── Client Secret: xyz789...
│   └── Callback URL: http://localhost:8501/callback
│
├── Users:
│   ├── supervisor@test.com
│   │   └── app_metadata:
│   │       ├── role: "supervisor"
│   │       └── supervised_users: ["auth0|driver1_id"]
│   │
│   └── driver@test.com
│       └── app_metadata:
│           ├── role: "driver"
│           └── supervisor_id: "auth0|supervisor_id"
│
├── Roles:
│   ├── supervisor
│   └── driver
│
└── Actions (Login Flow):
    └── Add User Metadata
        └── Adds custom claims to token
```

### 2. Your Application
```
Streamlit App (Port 8501)
├── auth/
│   ├── auth0_config.py → Handles OAuth2 flow
│   └── session.py → Manages user session
│
├── pages/
│   ├── supervisor_dashboard.py → For supervisors
│   └── driver_dashboard.py → For drivers
│
└── database/
    └── models.py → Stores user relationships
```

### 3. Data Flow
```
Arduino Device
    ↓ [HTTP POST with API Key]
Flask API (Port 5000)
    ↓ [Validates & stores]
SQLite Database
    ↓ [Queries by user role]
Streamlit Dashboard
    ↓ [Displays to user]
User Browser
```

## OAuth2 Flow Details

### Step-by-Step Technical Flow

```
┌─────────┐                                           ┌─────────┐
│ Browser │                                           │  Auth0  │
└────┬────┘                                           └────┬────┘
     │                                                      │
     │  1. GET /                                           │
     │─────────────────────────────────────────────────────│
     │                                                      │
     │  2. Click "Login"                                   │
     │─────────────────────────────────────────────────────│
     │                                                      │
     │  3. Redirect to Auth0                               │
     │─────────────────────────────────────────────────────▶
     │  GET /authorize?                                    │
     │    client_id=xxx&                                   │
     │    redirect_uri=http://localhost:8501/callback&     │
     │    response_type=code&                              │
     │    scope=openid profile email                       │
     │                                                      │
     │  4. Show login form                                 │
     │◀─────────────────────────────────────────────────────
     │                                                      │
     │  5. Submit credentials                              │
     │─────────────────────────────────────────────────────▶
     │                                                      │
     │  6. Run Actions (Add Metadata)                      │
     │                                                      │
     │  7. Redirect back with code                         │
     │◀─────────────────────────────────────────────────────
     │  http://localhost:8501/callback?code=AUTH_CODE      │
     │                                                      │
     │  8. Exchange code for token                         │
     │─────────────────────────────────────────────────────▶
     │  POST /oauth/token                                  │
     │    grant_type=authorization_code&                   │
     │    code=AUTH_CODE&                                  │
     │    client_id=xxx&                                   │
     │    client_secret=xxx                                │
     │                                                      │
     │  9. Return access token & ID token                  │
     │◀─────────────────────────────────────────────────────
     │  {                                                  │
     │    "access_token": "...",                          │
     │    "id_token": "...",                              │
     │    "token_type": "Bearer"                          │
     │  }                                                  │
     │                                                      │
     │  10. Get user info                                  │
     │─────────────────────────────────────────────────────▶
     │  GET /userinfo                                      │
     │  Authorization: Bearer ACCESS_TOKEN                 │
     │                                                      │
     │  11. Return user details                            │
     │◀─────────────────────────────────────────────────────
     │  {                                                  │
     │    "sub": "auth0|123",                             │
     │    "email": "user@test.com",                       │
     │    "role": "driver",                               │
     │    "supervisor_id": "auth0|456"                    │
     │  }                                                  │
     │                                                      │
     │  12. Set session & show dashboard                   │
     │                                                      │
```

## Token Structure

### ID Token (JWT)
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "auth0|123456789",
    "email": "driver@test.com",
    "name": "Test Driver",
    "https://drivingtracker.com/role": "driver",
    "https://drivingtracker.com/supervisor_id": "auth0|987654321",
    "iss": "https://your-tenant.us.auth0.com/",
    "aud": "your_client_id",
    "iat": 1234567890,
    "exp": 1234571490
  },
  "signature": "..."
}
```

## User Relationships in Database

```
Database: driving_tracker.db

┌─────────────────────────────────────────────┐
│               USERS TABLE                    │
├──────────────┬──────────┬──────────────────┤
│ id           │ role     │ supervisor_id    │
├──────────────┼──────────┼──────────────────┤
│ auth0|123    │supervisor│ NULL             │ ← Supervisor
│ auth0|456    │ driver   │ auth0|123        │ ← Driver 1
│ auth0|789    │ driver   │ auth0|123        │ ← Driver 2
└──────────────┴──────────┴──────────────────┘

Query Examples:
1. Get all drivers for supervisor:
   SELECT * FROM users WHERE supervisor_id = 'auth0|123'

2. Get supervisor for driver:
   SELECT * FROM users WHERE id = 'auth0|456'
   → Then: SELECT * FROM users WHERE id = result.supervisor_id
```

## Session Flow

```
┌──────────────────────────────────────────────────┐
│            STREAMLIT SESSION STATE               │
├──────────────────────────────────────────────────┤
│                                                  │
│  st.session_state.user = {                      │
│    "sub": "auth0|123",                          │
│    "email": "user@test.com",                    │
│    "name": "Test User",                         │
│    "role": "driver",                            │
│    "supervisor_id": "auth0|456"                 │
│  }                                               │
│                                                  │
│  st.session_state.token = {                     │
│    "access_token": "...",                       │
│    "id_token": "...",                           │
│    "expires_in": 86400                          │
│  }                                               │
│                                                  │
│  st.session_state.authenticated = True          │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Security Best Practices

### ✅ What We Do
1. **OAuth2 Authorization Code Flow** - Most secure flow for web apps
2. **HTTPS in Production** - Encrypt all traffic (use for deployment)
3. **API Key Authentication** - Protect Arduino endpoints
4. **Role-Based Access Control** - Users only see their data
5. **Token Validation** - Verify tokens on every request
6. **Session Management** - Secure session storage

### 🔒 What Auth0 Handles
1. **Password Storage** - Bcrypt hashing
2. **Brute Force Protection** - Rate limiting
3. **Multi-Factor Auth** - Available if needed
4. **Token Signing** - RS256 algorithm
5. **CSRF Protection** - State parameter

## Common Auth0 Dashboard Locations

```
Auth0 Dashboard (https://manage.auth0.com/)
│
├── Applications
│   └── Applications
│       └── "Driving Tracker"
│           ├── Settings (credentials, URLs)
│           ├── Connections (login methods)
│           └── APIs (if needed)
│
├── User Management
│   ├── Users (create/edit users)
│   │   └── app_metadata (set roles)
│   └── Roles (manage roles)
│
├── Actions
│   ├── Flows
│   │   └── Login (drag actions here)
│   └── Library (your custom actions)
│
└── Monitoring
    ├── Logs (see login attempts)
    └── Streams (export logs)
```

## Testing Your Setup

### Test Checklist
```
□ Supervisor Login
  □ Login with supervisor@test.com
  □ See supervisor dashboard
  □ See list of drivers (should show driver@test.com)
  □ See aggregate statistics

□ Driver Login
  □ Login with driver@test.com
  □ See driver dashboard
  □ See "monitored by supervisor" message
  □ Can start/stop sessions

□ API Testing (with Postman/curl)
  □ POST /api/session/start
  □ POST /api/driving/metric
  □ POST /api/driving/event
  □ POST /api/session/end
```

## Next Steps After Setup

1. **Customize Branding** (Auth0)
   - Add logo
   - Customize login page colors
   - Add custom domain (optional)

2. **Add More Users**
   - Create additional test users
   - Set up supervisor/driver relationships
   - Assign roles

3. **Configure Arduino**
   - Use API endpoints
   - Send real driving data
   - Test event triggers

4. **Deploy** (when ready)
   - Use Streamlit Cloud or Heroku
   - Update Auth0 URLs to production
   - Use PostgreSQL instead of SQLite

---

**Remember**: The detailed setup instructions are in [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md)!
