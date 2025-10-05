# 🧪 Testing Guide - How to Test Your App

## Quick Testing Steps

### 1. **View the Home Page**
Open: **http://localhost:8501**

You should see:
- Beautiful welcome screen
- Login button on the right
- Features listed on the left
- Demo credentials in expandable section

---

### 2. **Test Login as Supervisor**

#### Step A: Login
1. Click **"🔐 Login / Sign Up with Auth0"** button
2. You'll be redirected to Auth0
3. Enter credentials:
   - Email: `supervisor@test.com`
   - Password: `Test1234!`
4. Click "Continue" or "Login"

#### Step B: View Dashboard
After login, you should see:
- ✅ **Sidebar appears** on the left
- ✅ User info box showing "supervisor@test.com" and "Role: Supervisor"
- ✅ Navigation options: Dashboard, Manage Drivers, Settings
- ✅ **🚪 Logout button** at the bottom (blue, prominent)
- ✅ Supervisor dashboard in main area

#### Step C: Logout
1. Look at the **left sidebar**
2. Scroll to bottom if needed
3. Click **"🚪 Logout"** button
4. You'll be logged out and returned to home page

---

### 3. **Test Login as Driver**

#### Step A: Login
1. From home page, click **"🔐 Login / Sign Up with Auth0"**
2. Enter credentials:
   - Email: `driver@test.com`
   - Password: `Test1234!`
3. Click "Continue"

#### Step B: View Dashboard
After login, you should see:
- ✅ Sidebar with user info (driver@test.com, Role: Driver)
- ✅ Navigation: My Dashboard, My Stats, Settings
- ✅ **🚪 Logout button** in sidebar
- ✅ Driver dashboard showing:
  - "Your driving is being monitored by your supervisor" message
  - Start/Stop session buttons
  - Personal statistics

#### Step C: Test Driving Session
1. Click **"🚗 Start Driving Session"** button
2. Status changes to "Currently Driving"
3. Click **"🛑 End Session"** to stop
4. Session is saved to database

#### Step D: Logout
1. Click **"🚪 Logout"** in sidebar
2. Return to home page

---

## 🔍 Where to Find the Logout Button

### When Logged In:
```
┌─────────────────────────┐
│ 🚗 Driving Tracker      │ ← Sidebar (left side)
├─────────────────────────┤
│ User Name               │
│ Role: Supervisor        │ ← Your info
├─────────────────────────┤
│ ○ 📊 Dashboard         │
│ ○ 👥 Manage Drivers    │ ← Navigation
│ ○ ⚙️ Settings          │
├─────────────────────────┤
│  [🚪 Logout]           │ ← LOGOUT BUTTON HERE!
│                         │
│ Click logout to test... │
└─────────────────────────┘
```

**The logout button is:**
- ✅ In the **left sidebar** (not main area)
- ✅ At the **bottom** below navigation
- ✅ **Blue** (primary button style)
- ✅ Full width with 🚪 icon

---

## 🎯 What to Test

### ✅ Home Page
- [ ] Page loads without errors
- [ ] Title shows "🚗 Driving Tracker"
- [ ] Features are displayed on left
- [ ] Login button works on right
- [ ] Demo credentials are visible (expandable)
- [ ] Footer shows use cases, security, about

### ✅ Auth0 Login
- [ ] Clicking login redirects to Auth0
- [ ] Auth0 page shows your app name
- [ ] Can login with supervisor credentials
- [ ] Can login with driver credentials
- [ ] Returns to app after successful login

### ✅ Supervisor Dashboard
- [ ] Sidebar shows user info
- [ ] Sidebar shows navigation options
- [ ] Can see supervised drivers (or message if none)
- [ ] Dashboard shows metrics
- [ ] Logout button is visible and works

### ✅ Driver Dashboard
- [ ] Sidebar shows driver info
- [ ] Shows "monitored by supervisor" message
- [ ] Can start/stop driving sessions
- [ ] Shows personal statistics
- [ ] Logout button works

### ✅ Logout Flow
- [ ] Click logout button in sidebar
- [ ] Redirected to Auth0 logout
- [ ] Returns to home page
- [ ] Session is cleared (can't access dashboard)
- [ ] Can login again with different account

---

## 🐛 Troubleshooting

### Can't See Logout Button?
**Solution**: The sidebar might be collapsed
- Look for **←** or **☰** icon in top-left corner
- Click it to expand the sidebar
- Logout button is at the bottom of sidebar

### Logout Not Working?
**Symptoms**: Click logout but nothing happens
**Solution**:
- Check browser console for errors (F12)
- Make sure you're clicking the button in the **sidebar** (not main area)
- Refresh page and try again

### Keep Getting Logged Out?
**Symptoms**: Login works but immediately logs out
**Solution**:
- Check `.env` has correct Auth0 credentials
- Verify Auth0 callback URLs are configured
- Check browser console for errors

### Sidebar Doesn't Appear?
**Solution**:
- Make sure you're actually logged in
- Check for **☰** menu icon in top-left
- Click it to show sidebar
- Refresh the page

---

## 🔄 Testing Different Accounts

### Quick Switch Between Accounts:

1. **Login as Supervisor**
   ```
   supervisor@test.com / Test1234!
   → See supervisor dashboard
   → Logout
   ```

2. **Login as Driver**
   ```
   driver@test.com / Test1234!
   → See driver dashboard
   → Logout
   ```

3. **Repeat** to verify both dashboards work

---

## 📝 What Each Role Should See

### Supervisor View:
```
Sidebar:
- User: supervisor@test.com
- Role: Supervisor
- Navigation: Dashboard, Manage Drivers, Settings
- Logout button

Main Area:
- "Supervisor Dashboard" title
- "Overview" with metrics
- List of monitored drivers
- Recent events across all drivers
```

### Driver View:
```
Sidebar:
- User: driver@test.com
- Role: Driver
- Navigation: My Dashboard, My Stats, Settings
- Logout button

Main Area:
- "My Driving Dashboard" title
- "Your driving is being monitored" message
- Start/Stop session buttons
- Personal statistics
- Recent trips
- Safety tips
```

---

## ✅ Success Criteria

You've successfully tested when:
- ✅ Can view home page
- ✅ Can login as supervisor
- ✅ Can see supervisor dashboard
- ✅ Can logout from supervisor account
- ✅ Can login as driver
- ✅ Can see driver dashboard
- ✅ Can start/stop driving sessions
- ✅ Can logout from driver account
- ✅ Can switch between accounts multiple times

---

## 🚀 Next Steps After Testing

Once testing is complete:
1. **Customize** the home page (colors, text, logo)
2. **Add users** in Auth0 dashboard
3. **Connect Arduino** to send real data
4. **Deploy** to production (Streamlit Cloud, etc.)

---

**Start testing at: http://localhost:8501** 🎉

The logout button is in the **left sidebar** at the **bottom**!
