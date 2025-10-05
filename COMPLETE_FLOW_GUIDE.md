# Complete Flow Guide - Arduino to Dashboard

## 🎯 Your System Flow

```
Arduino (BLE) → ble_supabase.py → Supabase → React Dashboard
```

## ✅ What's Been Built

### 1. **Backend (Python + Supabase)**
- ✅ Database schema with 5 tables (supervisors, drivers, sessions, events, sensor_readings)
- ✅ `ble_supabase.py` - Connects Arduino via Bluetooth and streams to Supabase
- ✅ Real-time heartbeat every 10 seconds
- ✅ Auto-timeout after 5 minutes of inactivity
- ✅ Connection status tracking (online/offline)
- ✅ Public access (all supervisors see all drivers)

### 2. **Frontend (React + Tailwind + Framer Motion)**
- ✅ Dashboard with live driver cards
- ✅ Green checkmark when Arduino is connected (online)
- ✅ "Live Drivers" count updates in real-time
- ✅ Driver Detail page with current session stats
- ✅ Real-time subscriptions (auto-updates)

## 🚀 How to Use It

### Step 1: Start Arduino
Make sure your Arduino Nano 33 BLE is:
- Powered on
- Running BLE code
- Advertising as "Driving Monitor"

### Step 2: Connect Arduino to Supabase
```bash
python ble_supabase.py
```

**What happens:**
1. Prompts for Arduino ID (press Enter for ARD-001)
2. Connects to Supabase
3. Finds driver (Michael Chen for ARD-001)
4. Creates new driving session
5. **Sets connection_status to 'online'** 🟢
6. Starts heartbeat loop (every 10 seconds)
7. Starts timeout monitor (auto-end after 5 minutes)
8. Begins streaming sensor data

**Output:**
```
✅ Connected to Supabase
✅ Found driver: Michael Chen (mchen@company.com)
✅ Started new driving session: <session-id>
🟢 Driver is now ONLINE
✅ Found Driving Monitor at: XX:XX:XX:XX:XX:XX
📱 Receiving driving data and syncing to Supabase...
```

### Step 3: View Dashboard
```bash
cd frontend
npm run dev
```

Navigate to: `http://localhost:5173/dashboard`

**What you'll see:**
- ARD-001 card with **green checkmark** ✓ and "Live Connected"
- "Live Drivers" count shows 1
- Real-time sensor data flowing
- Safety score updating automatically

### Step 4: Click on ARD-001 Card
Navigates to: `/driver/<driver-id>`

**Driver Detail Page shows:**
- Current session duration
- Sharp turns count (swerving events)
- Hard brakes count (harsh brake events)
- Aggressive driving count
- Safety score progress bar
- Recent events timeline with sensor values

### Step 5: Stop the Script
Press `Ctrl+C` in the terminal running `ble_supabase.py`

**What happens:**
1. Heartbeat stops
2. Timeout monitor stops
3. Session marked as 'completed'
4. **Sets connection_status to 'offline'** 🔴
5. Dashboard updates automatically
6. Green checkmark turns to gray "Offline"
7. "Live Drivers" count decreases

**Output:**
```
✅ Session ended: <session-id>
🔴 Driver is now OFFLINE
```

## 📊 Data Flow

### When Script Starts:
```sql
UPDATE drivers SET
  connection_status = 'online',
  status = 'active',
  last_heartbeat = NOW()
WHERE arduino_id = 'ARD-001'
```

### Every 10 Seconds (Heartbeat):
```sql
UPDATE drivers SET
  last_heartbeat = NOW()
WHERE id = <driver_id>
```

### When Event Occurs:
```sql
INSERT INTO events (event_type, x, y, z, severity, ...)
VALUES ('SWERVING', 0.19, 0.74, 1.22, 'medium', ...)
```

Triggers automatically update:
```sql
UPDATE driving_sessions SET
  total_swerving = total_swerving + 1,
  safety_score = <calculated>
```

### When Script Stops:
```sql
UPDATE drivers SET
  connection_status = 'offline',
  status = 'inactive'
WHERE id = <driver_id>

UPDATE driving_sessions SET
  status = 'completed',
  ended_at = NOW()
WHERE id = <session_id>
```

### Dashboard Subscribes:
```javascript
supabase.channel('driver-changes')
  .on('postgres_changes', { table: 'drivers' }, () => {
    // Auto-refresh when connection_status changes
  })
```

## 🎨 UI Elements

### Dashboard Card (ARD-001 when online):
```
┌────────────────────────────────┐
│ MC  Michael Chen               │
│     mchen@company.com          │
│                                │
│ Arduino ID: ARD-001            │
│ ✓ 📡 Live Connected (green)    │
│                                │
│ Trips Today: 5 | Score: 95%    │
│ Last active: Just now          │
│ [View Details →]               │
└────────────────────────────────┘
```

### Dashboard Card (ARD-001 when offline):
```
┌────────────────────────────────┐
│ MC  Michael Chen               │
│     mchen@company.com          │
│                                │
│ Arduino ID: ARD-001            │
│ 📡̸ Offline (gray)               │
│                                │
│ Trips Today: 5 | Score: 95%    │
│ Last active: 3 mins ago        │
│ [View Details →]               │
└────────────────────────────────┘
```

### Driver Detail Page (Current Session):
```
┌─────────────────────────────────────┐
│ ← Driver Details                    │
├─────────────────────────────────────┤
│ MC  Michael Chen                    │
│     mchen@company.com               │
│     ARD-001  ✓ 📡 Live              │
│                           95%       │
├─────────────────────────────────────┤
│ Current Session Active              │
│ Real-time monitoring    ⏱ 25m      │
├─────────────────────────────────────┤
│  Sharp Turns    Hard Brakes  Aggr  │
│      3              2          1    │
├─────────────────────────────────────┤
│ Safety Score: ████████░░ 88%       │
├─────────────────────────────────────┤
│ Recent Events:                      │
│ • SWERVING (medium) - Just now      │
│ • HARSH_BRAKE (high) - 2m ago       │
│ • SWERVING (low) - 5m ago           │
└─────────────────────────────────────┘
```

## 🔧 Auto-Timeout Feature

If the script crashes or Arduino disconnects:

**After 5 minutes:**
```
⏱️  No activity for 5 minutes, ending session...
✅ Session ended: <session-id>
🔴 Driver is now OFFLINE
```

The timeout monitor runs in the background and checks heartbeat every minute.

## 🗂️ File Structure

```
hackUTA/
├── ble_supabase.py          # Arduino → Supabase connector
├── .env                     # Supabase credentials
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx      # Main dashboard (UPDATED)
│   │   │   ├── DriverDetail.jsx   # Driver detail page (NEW)
│   │   │   └── AuthPage.jsx       # Login page
│   │   ├── lib/
│   │   │   └── supabase.js        # Supabase client
│   │   └── App.jsx                # Routes (UPDATED)
│   └── package.json
└── COMPLETE_FLOW_GUIDE.md   # This file
```

## 🎯 Testing the Complete Flow

### Test 1: Connection Detection
1. Start dashboard: `cd frontend && npm run dev`
2. Open `http://localhost:5173/dashboard`
3. Note: All drivers show "Offline"
4. Run: `python ble_supabase.py` (Enter for ARD-001)
5. **Verify**: ARD-001 card shows green checkmark ✓
6. **Verify**: "Live Drivers" count = 1

### Test 2: Event Detection
1. Keep script running
2. Shake/move Arduino to trigger events
3. **Verify**: Terminal shows: `🚨 EVENT: SWERVING (Total: 1)`
4. **Verify**: Dashboard safety score updates
5. Click "View Details" on ARD-001
6. **Verify**: Event counts increase in real-time

### Test 3: Disconnection
1. Press Ctrl+C in script terminal
2. **Verify**: Terminal shows "🔴 Driver is now OFFLINE"
3. **Verify**: Dashboard checkmark turns gray
4. **Verify**: "Live Drivers" count = 0
5. **Verify**: ARD-001 shows "Offline"

### Test 4: Auto-Timeout
1. Run script: `python ble_supabase.py`
2. Wait 5+ minutes without moving Arduino
3. **Verify**: Script auto-ends session
4. **Verify**: Dashboard shows offline

## 📝 Key Features Summary

| Feature | How It Works |
|---------|-------------|
| **Live Status** | Heartbeat every 10s updates `last_heartbeat` |
| **Green Checkmark** | Shows when `connection_status = 'online'` |
| **Auto-Timeout** | Ends session after 5 min no heartbeat |
| **Real-time Updates** | Supabase Realtime subscriptions |
| **Event Tracking** | All events saved with severity levels |
| **Safety Score** | Auto-calculated: 100 - (swerving×2 + brake×5 + aggressive×10) |
| **Public Access** | All supervisors see all drivers |

## 🚀 Production Checklist

- [ ] Get Supabase service role key (currently using anon key)
- [ ] Update `.env` with service role key
- [ ] Add user authentication
- [ ] Link supervisors to auth users
- [ ] Deploy frontend (Vercel/Netlify)
- [ ] Keep `ble_supabase.py` running on server/laptop

## 🎉 You're Ready!

Your complete flow is working:
1. Arduino sends data via BLE
2. Python script receives and uploads to Supabase
3. Dashboard shows live status with checkmarks
4. Click driver to see detailed session stats
5. Everything updates in real-time!

Start your Arduino and watch the magic happen! 🚗💨
