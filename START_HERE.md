# 🚀 START HERE - Your Complete Guide

Welcome to the Driving Tracker with Auth0! This guide will get you up and running in **30-45 minutes**.

## 📋 What You're Building

A **driving monitoring system** with:
- ✅ Auth0 authentication (supervisor/driver roles)
- ✅ Parent-child account relationships
- ✅ Streamlit dashboard
- ✅ Arduino data integration
- ✅ Real-time metrics tracking

## 🎯 Quick Start (3 Steps)

### Step 1: Auth0 Setup (15-20 min)
Follow the **step-by-step checklist**:

📄 **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** ← Start here!

This will guide you through:
- Creating Auth0 account
- Setting up your application
- Creating test users
- Configuring roles

Need more details? See:
- 📖 [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md) - Detailed instructions (updated for 2025!)
- 🔄 [AUTH0_FLOW_DIAGRAM.md](AUTH0_FLOW_DIAGRAM.md) - Visual diagrams and technical flow
- 🆕 [AUTH0_DASHBOARD_UPDATE_2025.md](AUTH0_DASHBOARD_UPDATE_2025.md) - **See "Triggers" instead of "Flows"? Read this!**

### Step 2: Configure Your App (5 min)

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your Auth0 credentials:**
   ```bash
   nano .env  # or use any text editor
   ```

3. **Add your Auth0 values** (from Step 1):
   ```
   AUTH0_DOMAIN=your-tenant.us.auth0.com
   AUTH0_CLIENT_ID=your_client_id
   AUTH0_CLIENT_SECRET=your_client_secret
   ```

4. **Generate secrets:**
   ```bash
   # Generate SECRET_KEY
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"

   # Generate ARDUINO_API_KEY
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### Step 3: Run the App (2 min)

**Option A: Use Quick Start Script** (Recommended)
```bash
./quickstart.sh
```

**Option B: Manual Start**
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py

# (Optional) Run Arduino API in another terminal
python api_endpoint.py
```

## 🎉 Success!

Open your browser to: **http://localhost:8501**

### Test Credentials:
```
Supervisor Account:
  Email: supervisor@test.com
  Password: Test1234!

Driver Account:
  Email: driver@test.com
  Password: Test1234!
```

## 📚 Documentation Overview

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[START_HERE.md](START_HERE.md)** | This file - overview & quick start | First time setup |
| **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** | Step-by-step Auth0 setup checklist | Setting up Auth0 |
| **[AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md)** | Detailed Auth0 configuration guide | Need detailed instructions |
| **[AUTH0_FLOW_DIAGRAM.md](AUTH0_FLOW_DIAGRAM.md)** | Visual flow diagrams & architecture | Understanding how it works |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues & solutions | When something breaks |
| **[README.md](README.md)** | Full project documentation | Reference & deployment |

## 🏗️ Project Structure

```
hackUTA/
├── 📄 Documentation
│   ├── START_HERE.md              ← You are here!
│   ├── SETUP_CHECKLIST.md         ← Auth0 setup checklist
│   ├── AUTH0_SETUP_GUIDE.md       ← Detailed Auth0 guide
│   ├── AUTH0_FLOW_DIAGRAM.md      ← Visual diagrams
│   ├── TROUBLESHOOTING.md         ← Fix common issues
│   └── README.md                  ← Full documentation
│
├── 🚀 Application
│   ├── app.py                     ← Main Streamlit app
│   ├── api_endpoint.py            ← Flask API for Arduino
│   └── quickstart.sh              ← Quick start script
│
├── 🔐 Authentication
│   └── auth/
│       ├── auth0_config.py        ← Auth0 integration
│       └── session.py             ← Session management
│
├── 💾 Database
│   └── database/
│       └── models.py              ← User & driving data models
│
├── 📊 Dashboards
│   └── pages/
│       ├── supervisor_dashboard.py ← Supervisor view
│       └── driver_dashboard.py     ← Driver view
│
├── 🛠️ Utilities
│   └── utils/
│       └── decorators.py          ← Role-based access
│
└── ⚙️ Configuration
    ├── .env.example               ← Environment template
    ├── .gitignore                 ← Git ignore rules
    └── requirements.txt           ← Python dependencies
```

## 🎯 What Each Role Sees

### 👔 Supervisor Dashboard
- Monitor multiple drivers
- View all driver statistics
- See driving events (harsh braking, speeding)
- Aggregate analytics
- Manage driver relationships

### 🚗 Driver Dashboard
- Personal driving statistics
- Start/stop driving sessions
- Trip history
- Safety events
- Performance tips

## 🔌 Arduino Integration

Once your app is running, connect Arduino using the API:

### Example Arduino Code:
```cpp
// Start session
POST http://localhost:5000/api/session/start
Headers: X-API-Key: your_api_key
Body: {"driver_id": "auth0|123"}

// Send metrics every second
POST http://localhost:5000/api/driving/metric
Headers: X-API-Key: your_api_key
Body: {
  "session_id": 123,
  "speed": 60.5,
  "acceleration": 2.3,
  "latitude": 32.7767,
  "longitude": -96.7970
}

// Send events when detected
POST http://localhost:5000/api/driving/event
Headers: X-API-Key: your_api_key
Body: {
  "session_id": 123,
  "event_type": "harsh_brake",
  "severity": "high"
}

// End session
POST http://localhost:5000/api/session/end
Headers: X-API-Key: your_api_key
Body: {"session_id": 123}
```

Full API documentation in [README.md](README.md#arduino-integration)

## ❓ Common Questions

### Q: Do I need an Arduino to test?
**A:** No! You can test the dashboards without Arduino. Use the driver dashboard to manually start/stop sessions.

### Q: Can I add more users?
**A:** Yes! Create them in Auth0 Dashboard → Users, then set their `app_metadata` with role and relationships.

### Q: How do I link a driver to supervisor?
**A:**
1. Get both user IDs from Auth0
2. Add `supervisor_id` to driver's `app_metadata`
3. Add driver ID to supervisor's `supervised_users` array

See [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md#step-6-create-test-users) for details.

### Q: Can I use this for my hackathon?
**A:** Absolutely! This is built for HackUTA with Auth0 sponsor track. Feel free to customize!

### Q: How do I deploy this?
**A:** See [README.md](README.md#next-steps) for deployment instructions (Streamlit Cloud, Heroku, etc.)

## 🆘 Need Help?

1. **Not working?** → Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Auth0 confused?** → See [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md)
3. **How does it work?** → Read [AUTH0_FLOW_DIAGRAM.md](AUTH0_FLOW_DIAGRAM.md)

## ✅ Pre-Flight Checklist

Before you start, make sure you have:

- [ ] Python 3.9+ installed
- [ ] Internet connection (for Auth0)
- [ ] Text editor (VS Code, nano, etc.)
- [ ] Terminal/command line access
- [ ] 30-45 minutes of time

## 🏆 For HackUTA Judges

### Auth0 Integration Highlights:
- ✅ **OAuth2 Authorization Code Flow** - Industry standard
- ✅ **Role-Based Access Control (RBAC)** - Supervisor/Driver roles
- ✅ **Custom User Metadata** - Parent-child relationships
- ✅ **Actions/Flows** - Custom token claims
- ✅ **Secure Session Management** - Token-based auth
- ✅ **Multi-Tier Architecture** - Hierarchical access control

### Technical Stack:
- **Frontend**: Streamlit (Python)
- **Authentication**: Auth0 (OAuth2)
- **Database**: SQLAlchemy + SQLite
- **API**: Flask (for Arduino)
- **Security**: API Key auth, Role decorators

## 🚀 Let's Go!

Ready to start? Follow these steps:

1. **Open** → [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
2. **Follow** → Each checkbox step by step
3. **Run** → `./quickstart.sh`
4. **Test** → Login and explore!

---

**Good luck with your hackathon! 🎉**

Questions? Open an issue or check the troubleshooting guide.
