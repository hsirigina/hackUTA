# 🚗 Driving Tracker with Auth0

A comprehensive driving monitoring system built with Streamlit and Auth0, featuring a multi-tier supervisor/driver architecture for real-time driving metrics tracking from Arduino devices.

## 📚 Quick Links

- **🚀 [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Start here! Step-by-step setup checklist
- **📖 [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md)** - Detailed Auth0 configuration guide
- **🔄 [AUTH0_FLOW_DIAGRAM.md](AUTH0_FLOW_DIAGRAM.md)** - Visual diagrams & technical flow
- **⚡ Quick Start**: Run `./quickstart.sh` after Auth0 setup

## 📋 Features

- **Auth0 Authentication**: Secure login with role-based access control
- **Multi-Tier Architecture**: Supervisor/Driver relationships (parent-child, manager-employee)
- **Real-Time Monitoring**: Live driving metrics from Arduino devices
- **Role-Based Dashboards**:
  - **Supervisors**: Monitor multiple drivers, view aggregated stats, manage alerts
  - **Drivers**: View personal driving stats, trip history, safety metrics
- **Event Tracking**: Harsh braking, speeding, and other driving events
- **RESTful API**: Secure endpoints for Arduino data ingestion

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Arduino   │────▶│  Flask API   │────▶│   Database  │
│   Device    │     │  (Port 5000) │     │   (SQLite)  │
└─────────────┘     └──────────────┘     └─────────────┘
                                                  │
                                                  ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    User     │────▶│  Streamlit   │────▶│   Auth0     │
│  (Browser)  │     │  (Port 8501) │     │   (OAuth)   │
└─────────────┘     └──────────────┘     └─────────────┘
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.9 or higher
- Auth0 account (free tier works)
- Arduino with GPS/sensors (optional for testing)

### 2. Clone and Install

```bash
git clone <repository-url>
cd hackUTA

# Install dependencies
pip install -r requirements.txt
```

### 3. Auth0 Configuration

1. Go to [Auth0 Dashboard](https://manage.auth0.com/)
2. Create a new application (Regular Web Application)
3. Configure settings:
   - **Allowed Callback URLs**: `http://localhost:8501/callback`
   - **Allowed Logout URLs**: `http://localhost:8501`
   - **Allowed Web Origins**: `http://localhost:8501`

4. Set up roles in Auth0:
   - Create `supervisor` role
   - Create `driver` role

5. Add user metadata (in Actions/Flows):
   ```javascript
   // Example: Set user role and relationships
   exports.onExecutePostLogin = async (event, api) => {
     api.user.setAppMetadata("role", "driver");
     api.user.setAppMetadata("supervisor_id", null);
     api.user.setAppMetadata("supervised_users", []);
   };
   ```

### 4. Environment Setup

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Auth0 credentials
nano .env
```

Update the following in `.env`:
```
AUTH0_DOMAIN=your-tenant.us.auth0.com
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret
ARDUINO_API_KEY=generate_a_secure_random_key
```

### 5. Initialize Database

```bash
# Database will be created automatically on first run
# To manually initialize:
python -c "from database.models import db; db.create_tables()"
```

## 🎯 Running the Application

### Start the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard will be available at: `http://localhost:8501`

### Start the Arduino API (separate terminal)

```bash
python api_endpoint.py
```

The API will be available at: `http://localhost:5000`

## 📡 Arduino Integration

### API Endpoints

All endpoints require the `X-API-Key` header with your API key.

#### 1. Start Driving Session
```bash
POST /api/session/start
Content-Type: application/json
X-API-Key: your_api_key

{
  "driver_id": "auth0|123456789"
}
```

#### 2. Submit Driving Metrics
```bash
POST /api/driving/metric
Content-Type: application/json
X-API-Key: your_api_key

{
  "session_id": 123,
  "speed": 60.5,
  "acceleration": 2.3,
  "latitude": 32.7767,
  "longitude": -96.7970,
  "heading": 180.0,
  "rpm": 3000
}
```

#### 3. Submit Driving Events
```bash
POST /api/driving/event
Content-Type: application/json
X-API-Key: your_api_key

{
  "session_id": 123,
  "event_type": "harsh_brake",
  "severity": "high",
  "speed_at_event": 65.0,
  "latitude": 32.7767,
  "longitude": -96.7970
}
```

#### 4. End Session
```bash
POST /api/session/end
Content-Type: application/json
X-API-Key: your_api_key

{
  "session_id": 123
}
```

### Arduino Example Code (Pseudocode)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* apiKey = "your_api_key";
const char* serverUrl = "http://your-server:5000";
int sessionId = 0;

void startSession(String driverId) {
  HTTPClient http;
  http.begin(serverUrl + "/api/session/start");
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", apiKey);

  String payload = "{\"driver_id\":\"" + driverId + "\"}";
  int httpCode = http.POST(payload);

  if (httpCode == 201) {
    // Parse response to get session_id
    sessionId = parseSessionId(http.getString());
  }
}

void sendMetrics(float speed, float accel) {
  HTTPClient http;
  http.begin(serverUrl + "/api/driving/metric");
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", apiKey);

  String payload = "{\"session_id\":" + String(sessionId) +
                   ",\"speed\":" + String(speed) +
                   ",\"acceleration\":" + String(accel) + "}";
  http.POST(payload);
}
```

## 👥 User Roles & Relationships

### Supervisor Role
- Can view multiple driver dashboards
- Access to aggregated statistics
- Can manage driver assignments
- Receives alerts for all supervised drivers

### Driver Role
- Personal dashboard view
- Trip history and statistics
- Safety metrics and tips
- Session management (start/stop)

### Setting Up Relationships

Currently, relationships are managed through Auth0 user metadata. To assign a supervisor:

1. Go to Auth0 Dashboard → Users
2. Select a driver user
3. Update `app_metadata`:
   ```json
   {
     "role": "driver",
     "supervisor_id": "auth0|supervisor_user_id"
   }
   ```

For supervisor, update their metadata:
```json
{
  "role": "supervisor",
  "supervised_users": ["auth0|driver1_id", "auth0|driver2_id"]
}
```

## 🗂️ Project Structure

```
hackUTA/
├── app.py                    # Main Streamlit application
├── api_endpoint.py          # Flask API for Arduino
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
│
├── auth/                   # Authentication modules
│   ├── __init__.py
│   ├── auth0_config.py    # Auth0 configuration
│   └── session.py         # Session management
│
├── database/              # Database models
│   ├── __init__.py
│   └── models.py         # SQLAlchemy models
│
├── pages/                # Dashboard pages
│   ├── __init__.py
│   ├── supervisor_dashboard.py
│   └── driver_dashboard.py
│
└── utils/                # Utility functions
    ├── __init__.py
    └── decorators.py     # Role-based decorators
```

## 🔒 Security Considerations

1. **API Keys**: Always use strong, randomly generated API keys
2. **HTTPS**: Use HTTPS in production (not HTTP)
3. **Environment Variables**: Never commit `.env` file to version control
4. **Auth0 Rules**: Validate and sanitize user metadata
5. **Database**: Use PostgreSQL in production instead of SQLite

## 🐛 Troubleshooting

### Auth0 Login Not Working
- Verify callback URLs in Auth0 dashboard
- Check `.env` file has correct credentials
- Clear browser cache/cookies

### Arduino Can't Connect to API
- Verify API is running on correct port
- Check API key in both `.env` and Arduino code
- Ensure firewall allows connections

### Database Errors
- Delete `driving_tracker.db` and restart to recreate
- Check file permissions

## 📝 Next Steps

- [ ] Add driver invitation system
- [ ] Implement real-time notifications
- [ ] Add GPS mapping visualization
- [ ] Create detailed analytics reports
- [ ] Deploy to production server
- [ ] Add mobile app support

## 🏆 HackUTA Project

This project was built for HackUTA with Auth0 as the authentication sponsor track.

## 📄 License

MIT License - feel free to use for your hackathon projects!
