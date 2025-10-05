# What's Hardcoded vs Dynamic

## ✅ DYNAMIC (From Supabase - Updates Every 2 Seconds)

### Dashboard Page

| Element | Source | Updates |
|---------|--------|---------|
| **Driver Cards** | `drivers` table | Every 2s |
| **Driver Names** | `drivers.name` | Every 2s |
| **Driver Emails** | `drivers.email` | Every 2s |
| **Arduino IDs** | `drivers.arduino_id` | Every 2s |
| **Connection Status** | `drivers.connection_status` | Every 2s |
| **Green Checkmark ✓** | `connection_status === 'online'` | Every 2s |
| **"Live Connected" text** | `connection_status === 'online'` | Every 2s |
| **Gray "Offline" icon** | `connection_status === 'offline'` | Every 2s |
| **Safety Scores** | `drivers.safety_score` | Every 2s |
| **Last Active Time** | `drivers.last_active` | Every 2s |
| **Trips Today Count** | `driving_sessions` (today's sessions) | Every 2s |
| **"Live Drivers" Count** | Count of `connection_status = 'online'` | Every 2s |
| **Total Drivers Count** | Count of all drivers | Every 2s |

### Driver Detail Page

| Element | Source | Updates |
|---------|--------|---------|
| **Driver Info** | `drivers` table | Every 2s |
| **Connection Status** | `drivers.connection_status` | Every 2s |
| **Safety Score** | `drivers.safety_score` | Every 2s |
| **Current Session** | `driving_sessions` (status='active') | Every 2s |
| **Session Duration** | Calculated from `started_at` | Every 2s |
| **Sharp Turns Count** | `driving_sessions.total_swerving` | Every 2s |
| **Hard Brakes Count** | `driving_sessions.total_harsh_brake` | Every 2s |
| **Aggressive Count** | `driving_sessions.total_aggressive` | Every 2s |
| **Recent Events List** | `events` table | Every 2s |
| **Event Timestamps** | `events.timestamp` | Every 2s |
| **Event Severity** | `events.severity` | Every 2s |
| **Sensor Values (X,Y,Z)** | `events.x, y, z` | Every 2s |

## 🔧 HARDCODED (Not from Database)

### Dashboard Page

| Element | Value | Location |
|---------|-------|----------|
| **Supervisor Name** | "Sarah Johnson" | `Dashboard.jsx` line 27 |
| **Supervisor Email** | "sarah.johnson@company.com" | `Dashboard.jsx` line 28 |
| **Supervisor Role** | "Fleet Supervisor" | `Dashboard.jsx` line 30 |
| **Supervisor Avatar** | "SJ" | `Dashboard.jsx` line 31 |

### UI Text & Labels

All these are hardcoded in the components:
- "Fleet Dashboard" header
- "Monitor your drivers in real-time" subtitle
- "Your Drivers" section title
- Button labels ("View Details", etc.)
- Stat card labels ("Arduino ID", "Trips Today", "Safety Score")
- "Live Connected" / "Offline" text

### Colors & Styling

All hardcoded in Tailwind classes:
- Green for online status
- Gray for offline status
- Color gradients
- Card layouts
- Icons

## 🔄 How Polling Works

### Dashboard.jsx
```javascript
useEffect(() => {
  fetchDrivers()  // Fetch immediately

  const interval = setInterval(() => {
    fetchDrivers()  // Fetch every 2 seconds
  }, 2000)

  return () => clearInterval(interval)
}, [])
```

**What `fetchDrivers()` does:**
1. Fetches ALL drivers from `drivers` table
2. Fetches TODAY'S sessions from `driving_sessions` table
3. Processes data to match drivers with their sessions
4. Updates `drivers` state
5. React re-renders the UI

### DriverDetail.jsx
```javascript
useEffect(() => {
  fetchDriverDetails()  // Fetch immediately

  const interval = setInterval(() => {
    fetchDriverDetails()  // Fetch every 2 seconds
  }, 2000)

  return () => clearInterval(interval)
}, [driverId])
```

**What `fetchDriverDetails()` does:**
1. Fetches driver from `drivers` table
2. Fetches active session from `driving_sessions` table
3. Fetches all events for that session from `events` table
4. Updates state
5. React re-renders the UI

## 🎯 Why Polling Instead of Real-time?

**You said:**
> "Rather than trying to do a live connection just make it such that our frontend fetches from supabase every 2 seconds because that was an issue that I ran into last week and this is the fix that worked."

**Benefits of 2-second polling:**
- ✅ More reliable (no WebSocket connection issues)
- ✅ Simpler code (no subscription management)
- ✅ Easier to debug
- ✅ Works better with Supabase's free tier
- ✅ Still feels real-time to users

**Trade-offs:**
- Slightly more database queries (but minimal with 2s interval)
- Not "instant" but close enough (2s max delay)

## 📊 Data Flow

```
Arduino → ble_supabase.py → Supabase Database
                                    ↓
                          (Updates every 2 seconds)
                                    ↓
                              React Dashboard
```

### When Script Starts:
```sql
-- ble_supabase.py updates:
UPDATE drivers SET
  connection_status = 'online',
  last_heartbeat = NOW()
WHERE arduino_id = 'ARD-001'

-- Dashboard fetches (every 2s):
SELECT * FROM drivers
-- Sees connection_status = 'online'
-- Shows green checkmark ✓
```

### When Event Occurs:
```sql
-- ble_supabase.py inserts:
INSERT INTO events (event_type, severity, ...)
VALUES ('SWERVING', 'medium', ...)

-- Trigger auto-updates:
UPDATE driving_sessions SET
  total_swerving = total_swerving + 1

-- Dashboard fetches (every 2s):
SELECT * FROM driving_sessions WHERE status = 'active'
-- Sees updated count
-- UI updates to show new count
```

### When Script Stops:
```sql
-- ble_supabase.py updates:
UPDATE drivers SET
  connection_status = 'offline'
WHERE arduino_id = 'ARD-001'

-- Dashboard fetches (every 2s):
SELECT * FROM drivers
-- Sees connection_status = 'offline'
-- Shows gray offline icon
```

## 🔑 Key Points

1. **Everything updates every 2 seconds** - No need to refresh browser
2. **Connection status is 100% accurate** - Based on actual database value
3. **Only ARD-001 will show online** - When `ble_supabase.py` is running
4. **All other drivers show offline** - Until their Arduino connects
5. **Supervisor info is hardcoded** - Will be replaced when you add auth

## 🚀 To See It Working

### Terminal 1:
```bash
python ble_supabase.py
# Enter: ARD-001
```
**Result in database:**
```sql
connection_status = 'online' for ARD-001
connection_status = 'offline' for ARD-002, ARD-003, etc.
```

### Browser:
```
http://localhost:5173/dashboard
```
**You'll see:**
- ARD-001: ✓ Live Connected (green)
- ARD-002: Offline (gray)
- ARD-003: Offline (gray)
- ARD-004: Offline (gray)
- ARD-005: Offline (gray)
- ARD-006: Offline (gray)
- Live Drivers: 1

### Press Ctrl+C in Terminal:
**Result in database:**
```sql
connection_status = 'offline' for ARD-001
```

**Dashboard updates within 2 seconds:**
- ARD-001: Offline (gray)
- Live Drivers: 0

## ✅ Summary

| What | How Often | Source |
|------|-----------|--------|
| Driver data | Every 2s | Supabase `drivers` table |
| Connection status | Every 2s | Supabase `connection_status` field |
| Session data | Every 2s | Supabase `driving_sessions` table |
| Events | Every 2s | Supabase `events` table |
| Supervisor info | Never (hardcoded) | Dashboard.jsx |
| UI text/colors | Never (hardcoded) | React components |

**Everything that matters is dynamic and updates automatically!** 🎉
