# 🔧 Troubleshooting Guide

Common issues and how to fix them.

## Auth0 Issues

### ❌ "Callback URL mismatch" Error

**Error Message:**
```
The redirect URI is wrong. You sent http://localhost:8501/callback
and we expected http://localhost:8501
```

**Solution:**
1. Go to [Auth0 Dashboard](https://manage.auth0.com/)
2. Navigate to Applications → Applications → Your App
3. Scroll to "Application URIs" section
4. In **Allowed Callback URLs**, make sure you have:
   ```
   http://localhost:8501/callback
   ```
5. Click "Save Changes"
6. Try logging in again

---

### ❌ "Unauthorized" Error

**Error Message:**
```
Unauthorized client
```

**Solution:**
1. Check your `.env` file has correct credentials:
   ```bash
   cat .env | grep AUTH0
   ```
2. Verify these match your Auth0 dashboard:
   - `AUTH0_DOMAIN` (e.g., `yourname-hackuta.us.auth0.com`)
   - `AUTH0_CLIENT_ID` (long alphanumeric string)
   - `AUTH0_CLIENT_SECRET` (even longer string)
3. Make sure there are NO spaces before/after the `=` sign
4. Restart your Streamlit app

---

### ❌ Login Page Shows But Nothing Happens

**Possible Causes:**

**1. Action Not Deployed**
- Go to Actions → Flows → Login
- Make sure "Add User Metadata" is in the flow
- Check it's deployed (green checkmark)

**2. Action Not Applied**
- After adding action to flow, click "Apply" (top right)

**3. Browser Cache**
- Clear browser cache and cookies
- Or try incognito/private mode

---

### ❌ User Role Not Showing

**Symptoms:**
- User logs in but gets error: "Access denied"
- Dashboard shows wrong role

**Solution:**
1. Go to Auth0 Dashboard → Users
2. Click on the user
3. Scroll to "Metadata" section
4. In **app_metadata** field, add:
   ```json
   {
     "role": "driver",
     "supervisor_id": null
   }
   ```
   Or for supervisor:
   ```json
   {
     "role": "supervisor",
     "supervised_users": []
   }
   ```
5. Click "Save"
6. Log out and log back in

---

### ❌ Supervisor Can't See Drivers

**Symptoms:**
- Supervisor logs in successfully
- Dashboard shows "You don't have any drivers assigned yet"

**Solution:**

**Step 1: Get User IDs**
1. Go to Auth0 Dashboard → Users
2. Click on supervisor user → Copy their `user_id` (e.g., `auth0|abc123`)
3. Click on driver user → Copy their `user_id` (e.g., `auth0|xyz789`)

**Step 2: Update Driver's Metadata**
1. Click on driver user
2. Update **app_metadata**:
   ```json
   {
     "role": "driver",
     "supervisor_id": "auth0|abc123"
   }
   ```
   ⚠️ Use the ACTUAL supervisor user_id here!
3. Click "Save"

**Step 3: Update Supervisor's Metadata**
1. Click on supervisor user
2. Update **app_metadata**:
   ```json
   {
     "role": "supervisor",
     "supervised_users": ["auth0|xyz789"]
   }
   ```
   ⚠️ Use the ACTUAL driver user_id here!
3. Click "Save"

**Step 4: Test**
1. Log out of the app
2. Log back in as supervisor
3. You should now see the driver!

---

## Application Issues

### ❌ "Module not found" Error

**Error Message:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or if using virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### ❌ Database Error on Startup

**Error Message:**
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file
```

**Solution:**
```bash
# Delete the database and recreate
rm driving_tracker.db

# Restart the app (database will be created automatically)
streamlit run app.py
```

---

### ❌ Port Already in Use

**Error Message:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**

**Option 1: Kill the process**
```bash
# For Streamlit (port 8501)
lsof -ti:8501 | xargs kill -9

# For Flask API (port 5000)
lsof -ti:5000 | xargs kill -9
```

**Option 2: Use different port**
```bash
# Streamlit on different port
streamlit run app.py --server.port 8502

# Flask API on different port
# Edit .env: API_PORT=5001
```

---

### ❌ ".env file not found" Error

**Solution:**
```bash
# Copy the example file
cp .env.example .env

# Edit with your credentials
nano .env  # or use any text editor
```

---

## Arduino/API Issues

### ❌ Arduino Can't Connect to API

**Symptoms:**
- Arduino shows connection error
- No data appearing in dashboard

**Solution:**

**1. Verify API is Running**
```bash
# Check if Flask is running
curl http://localhost:5000/api/health

# Should return:
# {"status":"healthy","timestamp":"..."}
```

**2. Check API Key**
- Make sure Arduino code has the same API key as `.env`
- Check `.env`:
  ```bash
  cat .env | grep ARDUINO_API_KEY
  ```

**3. Check Firewall**
```bash
# On macOS, allow Python to accept connections
# System Preferences → Security & Privacy → Firewall → Allow Python
```

**4. Test with curl**
```bash
curl -X POST http://localhost:5000/api/session/start \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{"driver_id": "auth0|123"}'
```

---

### ❌ API Returns "Unauthorized"

**Error:**
```json
{"error": "Unauthorized"}
```

**Solution:**
1. Check you're sending the API key in header:
   ```
   X-API-Key: your_secret_key
   ```
2. Verify API key in `.env` matches
3. Make sure there are no spaces in the key

---

### ❌ API Returns "Invalid or inactive session"

**Error:**
```json
{"error": "Invalid or inactive session"}
```

**Solution:**
1. Start a session first:
   ```bash
   curl -X POST http://localhost:5000/api/session/start \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key" \
     -d '{"driver_id": "auth0|your_driver_id"}'
   ```
2. Use the returned `session_id` for metrics/events
3. Make sure the session is still active (not ended)

---

## Development Issues

### ❌ Changes Not Reflecting

**Solution:**
1. **Streamlit**: App auto-reloads, but you can force it:
   - Click "Always rerun" in the top-right menu
   - Or press `R` in the browser

2. **Flask API**: Restart manually:
   ```bash
   # Stop with Ctrl+C, then:
   python api_endpoint.py
   ```

3. **Database changes**:
   ```bash
   # Delete and recreate
   rm driving_tracker.db
   python -c "from database.models import db; db.create_tables()"
   ```

---

### ❌ Streamlit Shows "Connection Error"

**Symptoms:**
- Red banner: "Unable to connect to Streamlit"

**Solution:**
1. Refresh the page
2. Check Streamlit is still running in terminal
3. Restart Streamlit:
   ```bash
   streamlit run app.py
   ```

---

## Testing Tips

### Quick Test Commands

**1. Test Auth0 Connection**
```python
# Run this in terminal
python3 << EOF
from auth.auth0_config import auth0_config
print("✅ Auth0 Domain:", auth0_config.domain)
print("✅ Client ID:", auth0_config.client_id[:20] + "...")
EOF
```

**2. Test Database**
```python
# Run this in terminal
python3 << EOF
from database.models import db
db.create_tables()
print("✅ Database working!")
EOF
```

**3. Test API**
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Should return:
# {"status":"healthy","timestamp":"..."}
```

---

## Getting Help

### Debug Checklist

Before asking for help, try:

- [ ] Check this troubleshooting guide
- [ ] Look at terminal for error messages
- [ ] Check browser console (F12) for JavaScript errors
- [ ] Verify all credentials in `.env` are correct
- [ ] Try logging out and back in
- [ ] Clear browser cache
- [ ] Restart the application

### Where to Get Help

1. **Auth0 Issues**: [Auth0 Community](https://community.auth0.com/)
2. **Streamlit Issues**: [Streamlit Forums](https://discuss.streamlit.io/)
3. **General Questions**: Check the detailed guides:
   - [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md)
   - [AUTH0_FLOW_DIAGRAM.md](AUTH0_FLOW_DIAGRAM.md)

### Logging

Enable detailed logging for debugging:

**Streamlit:**
```bash
streamlit run app.py --logger.level=debug
```

**Flask:**
```python
# Edit api_endpoint.py, change last line:
app.run(host='0.0.0.0', port=port, debug=True)
```

---

## Still Stuck?

Create an issue with:
1. **Error message** (full text)
2. **Steps to reproduce**
3. **What you've tried**
4. **Screenshots** (if applicable)
5. **Environment**: OS, Python version

```bash
# Get your environment info
python3 --version
pip list | grep -E "(streamlit|authlib|flask)"
```

Good luck! 🚀
