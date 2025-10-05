# Arduino Bluetooth to Supabase Integration Guide

## What This Does

Your Arduino is now connected to Supabase! When you run the new script, it will:
1. ✅ Connect to your Arduino via Bluetooth
2. ✅ Receive real-time sensor data (X, Y, Z accelerometer values)
3. ✅ Detect driving events (SWERVING, HARSH_BRAKE, AGGRESSIVE)
4. ✅ Store everything in Supabase
5. ✅ Update your dashboard in real-time
6. ✅ Calculate safety scores automatically

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the Supabase Python client.

### 2. Verify Your Arduino ID

Your script needs to know which Arduino is sending data. The default is **ARD-001**.

**To check which drivers exist in Supabase:**
- ARD-001 → Michael Chen
- ARD-002 → Emily Rodriguez
- ARD-003 → James Wilson
- ARD-004 → Aisha Patel
- ARD-005 → David Kim
- ARD-006 → Sofia Martinez

If you want to use a different Arduino ID, you can specify it when running the script.

### 3. Make Sure Arduino is On

- Power on your Arduino Nano 33 BLE
- Ensure it's advertising (should be discoverable via Bluetooth)
- Device name should be "Driving Monitor" or contain "Arduino"

### 4. Run the Script

```bash
python ble_supabase.py
```

You'll be prompted to enter an Arduino ID. Press Enter to use the default (ARD-001) or type a different one.

## What Happens When You Run It

### Step 1: Connection
```
Enter Arduino ID (default: ARD-001):
✅ Connected to Supabase
✅ Found driver: Michael Chen (mchen@company.com)
✅ Started new driving session: <session-id>
🔍 Looking for 'Driving Monitor' device...
```

### Step 2: Scanning
```
Scanning for devices...
✅ Found Driving Monitor at: XX:XX:XX:XX:XX:XX
✅ Connected to Driving Monitor!
📱 Receiving driving data and syncing to Supabase...
```

### Step 3: Real-time Data Streaming
```
Sensors: X=0.19, Y=0.74, Z=1.22 | Event: SWERVING | Count: 1
🚨 EVENT: SWERVING (Total: 1)
💾 Saved SWERVING event to Supabase (Severity: medium)

Sensors: X=-0.67, Y=-0.33, Z=1.91 | Event: HARSH_BRAKE | Count: 1
🚨 EVENT: HARSH_BRAKE (Total: 1)
💾 Saved HARSH_BRAKE event to Supabase (Severity: high)
```

### Step 4: Dashboard Updates
Your frontend dashboard will automatically show:
- ✅ Driver status changing to "active"
- ✅ Real-time event counts
- ✅ Updated safety scores
- ✅ Last active timestamp

## How Data Flows

```
Arduino (BLE)
    ↓
ble_supabase.py (Your Laptop)
    ↓
Supabase Database
    ↓
React Dashboard (Real-time updates)
```

## Data Storage

### What Gets Saved

1. **Sensor Readings** (every 5 seconds or when event occurs)
   - X, Y, Z accelerometer values
   - Timestamp
   - Event type (if any)

2. **Events** (only when detected)
   - Event type: SWERVING, HARSH_BRAKE, AGGRESSIVE
   - Sensor values at event time
   - Severity: low, medium, high
   - Timestamp

3. **Session Data** (updated continuously)
   - Total swerving events
   - Total harsh brake events
   - Total aggressive events
   - Safety score (calculated automatically)
   - Session start/end times

4. **Driver Status** (updated in real-time)
   - Status: active/inactive/warning
   - Last active time
   - Current safety score

## Safety Score Calculation

Your safety score starts at 100 and decreases based on events:
- **Swerving**: -2 points each
- **Harsh Brake**: -5 points each
- **Aggressive**: -10 points each

Minimum score: 0

## To Stop the Script

Press `Ctrl+C` to disconnect. This will:
1. ✅ End the driving session
2. ✅ Update driver status to "inactive"
3. ✅ Show session summary
4. ✅ Disconnect from Arduino

## Viewing Data in Your Dashboard

Once the script is running:

1. **Open your React dashboard:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Navigate to:** `http://localhost:5173/dashboard`

3. **You'll see:**
   - Driver status: "active" (green dot)
   - Real-time safety score updates
   - Event counts increasing
   - Last active: "just now"

## Troubleshooting

### "Driver not found for Arduino ID"
**Solution:** Make sure you're using one of the existing Arduino IDs (ARD-001 to ARD-006) or create a new driver in Supabase first.

### "Driving Monitor not found"
**Solution:**
- Check Arduino is powered on
- Verify BLE code is uploaded
- Make sure device is advertising
- Try restarting Arduino

### "Missing SUPABASE_URL or SUPABASE_SERVICE_KEY"
**Solution:** Make sure your `.env` file has both:
```
SUPABASE_URL=https://mlztlnewoxxazrquimkk.supabase.co
SUPABASE_SERVICE_KEY=<your-key>
```

### Data not showing in dashboard
**Solution:**
- Make sure you're logged in as the supervisor
- Check that the driver's supervisor_id matches
- Verify Row Level Security policies

## Next Steps

1. **Test the connection** with your Arduino
2. **Monitor the dashboard** for real-time updates
3. **Drive around** (or simulate events) to see data flow
4. **Check Supabase** tables to verify data is being saved

## Advanced: Multiple Arduinos

If you have multiple Arduinos:
1. Run multiple instances of the script
2. Each with a different Arduino ID
3. They'll all update the same Supabase database
4. Dashboard shows all drivers simultaneously

## Files Created

- `ble_supabase.py` - Main script for BLE to Supabase sync
- Updated `.env` - Contains Supabase credentials
- Updated `requirements.txt` - Added Supabase client

## Your Old Script

Your original `ble.py` is still there and unchanged. Use `ble_supabase.py` for production with Supabase integration.
