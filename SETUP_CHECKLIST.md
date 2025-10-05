# ✅ Auth0 Setup Checklist

Use this checklist to track your setup progress. Follow along with [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md) for detailed instructions.

## 📋 Setup Progress

### Phase 1: Auth0 Account Setup
- [ ] Create Auth0 account at https://auth0.com/signup
- [ ] Choose tenant name (e.g., `yourname-hackuta`)
- [ ] Verify account via email

### Phase 2: Create Application
- [ ] Go to Applications → Applications
- [ ] Click "Create Application"
- [ ] Name: `Driving Tracker`
- [ ] Type: `Regular Web Applications`
- [ ] Click "Create"

### Phase 3: Configure Application
- [ ] Copy **Domain** → Write here: `_______________________`
- [ ] Copy **Client ID** → Write here: `_______________________`
- [ ] Copy **Client Secret** (click show first)
- [ ] Add Allowed Callback URLs: `http://localhost:8501/callback`
- [ ] Add Allowed Logout URLs: `http://localhost:8501`
- [ ] Add Allowed Web Origins: `http://localhost:8501`
- [ ] Add Allowed Origins (CORS): `http://localhost:8501`
- [ ] Click "Save Changes"

### Phase 4: Create Roles
- [ ] Go to User Management → Roles
- [ ] Create role: `supervisor`
- [ ] Create role: `driver`

### Phase 5: Set Up Actions
**Note:** You'll see either "Flows" OR "Triggers" - both work the same!
- [ ] Go to Actions → **Flows** (or **Triggers** if you don't see Flows)
- [ ] Click "Login" flow (or "Login / Post Login" trigger)
- [ ] Create custom action: "Add User Metadata"
- [ ] Copy/paste the JavaScript code from guide
- [ ] Click "Deploy"
- [ ] Drag action into Login flow (look for "Custom" tab on right)
- [ ] Click "Apply"

### Phase 6: Create Test Users

#### Supervisor User
- [ ] Go to User Management → Users
- [ ] Create user: `supervisor@test.com` / `Test1234!`
- [ ] Click on user
- [ ] Add to app_metadata: `{"role": "supervisor", "supervised_users": []}`
- [ ] Copy supervisor's user_id: `_______________________`

#### Driver User
- [ ] Create user: `driver@test.com` / `Test1234!`
- [ ] Click on user
- [ ] Copy driver's user_id: `_______________________`
- [ ] Add to app_metadata: `{"role": "driver", "supervisor_id": "SUPERVISOR_USER_ID"}`
- [ ] Go back to supervisor user
- [ ] Update app_metadata with driver's user_id in supervised_users array

### Phase 7: Local Application Setup
- [ ] Copy `.env.example` to `.env`: `cp .env.example .env`
- [ ] Update `AUTH0_DOMAIN` in `.env`
- [ ] Update `AUTH0_CLIENT_ID` in `.env`
- [ ] Update `AUTH0_CLIENT_SECRET` in `.env`
- [ ] Generate `SECRET_KEY`: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Generate `ARDUINO_API_KEY`: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

### Phase 8: Install & Run
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start Streamlit: `streamlit run app.py`
- [ ] (Optional) Start API: `python api_endpoint.py`

### Phase 9: Test Authentication
- [ ] Open `http://localhost:8501`
- [ ] Click "Login with Auth0"
- [ ] Login as supervisor (`supervisor@test.com`)
- [ ] Verify supervisor dashboard shows
- [ ] Logout
- [ ] Login as driver (`driver@test.com`)
- [ ] Verify driver dashboard shows
- [ ] Verify driver sees "monitored by supervisor" message

## 🎯 Quick Reference

### Auth0 Dashboard URLs
- **Main Dashboard**: https://manage.auth0.com/
- **Applications**: https://manage.auth0.com/dashboard/us/YOUR-TENANT/applications
- **Users**: https://manage.auth0.com/dashboard/us/YOUR-TENANT/users
- **Roles**: https://manage.auth0.com/dashboard/us/YOUR-TENANT/roles
- **Actions**: https://manage.auth0.com/dashboard/us/YOUR-TENANT/actions/flows

### Your Credentials (fill these in)
```
Tenant Domain: _________________________________.us.auth0.com
Client ID: _________________________________________
Client Secret: _____________________________________

Supervisor User ID: auth0|_________________________
Driver User ID: auth0|_____________________________
```

### Test Credentials
```
Supervisor:
  Email: supervisor@test.com
  Password: Test1234!

Driver:
  Email: driver@test.com
  Password: Test1234!
```

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| Can't login | Check Callback URLs in Auth0 match `.env` |
| Role not showing | Verify Action is deployed and in Login flow |
| Supervisor sees no drivers | Check `supervised_users` array in supervisor's metadata |
| Driver not linked | Verify `supervisor_id` in driver's metadata |

## ✅ Success Criteria

You'll know everything works when:
1. ✅ You can login with both test accounts
2. ✅ Supervisor sees driver in their dashboard
3. ✅ Driver sees "monitored by supervisor" message
4. ✅ Each role sees different dashboard views

---

**Need help?** Check [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md) for detailed step-by-step instructions!
