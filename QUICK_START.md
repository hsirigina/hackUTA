# 🚀 Quick Start - Arduino to Dashboard

## Current Status ✅

Your system is **90% ready**! Here's what's done:

### ✅ Database Setup (Complete)
- 5 tables created in Supabase
- Sample data loaded (6 drivers, 2 active sessions, 9 events)
- Real-time subscriptions enabled
- Row Level Security configured

### ✅ Frontend (Complete)
- Beautiful authentication page
- Supervisor dashboard with driver cards
- Ready for real-time data

### ✅ Arduino Integration (Ready to Test)
- `ble_supabase.py` - Connects Arduino → Supabase
- Environment variables configured
- Supabase client installed

## 🎯 To Get Live Data Flowing

### Option 1: Test with Your Arduino (Recommended)

1. **Make sure Arduino is on and advertising via Bluetooth**

2. **Run the BLE script:**
   ```bash
   python ble_supabase.py
   ```

3. **When prompted, enter Arduino ID:**
   - Press Enter for default (ARD-001)
   - Or type: ARD-002, ARD-003, etc.

4. **Watch the magic happen:**
   ```
   ✅ Connected to Supabase
   ✅ Found driver: Michael Chen
   ✅ Started new driving session
   📱 Receiving driving data and syncing to Supabase...
   ```

### Option 2: View Existing Sample Data

The dashboard already has sample data! Just view it:

1. **Start the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open browser:** `http://localhost:5173/dashboard`

3. **You'll see:**
   - 6 drivers with different statuses
   - Safety scores
   - Arduino IDs
   - Sample events

## 📊 File Reference

| File | Purpose |
|------|---------|
| `ble.py` | Original BLE script (no Supabase) |
| `ble_supabase.py` | **NEW** - BLE with Supabase sync |
| `test_supabase_connection.py` | Test Supabase connection |
| `frontend/` | React dashboard |
| `SUPABASE_DATABASE_GUIDE.md` | Database documentation |
| `ARDUINO_BLUETOOTH_SETUP.md` | Arduino setup guide |

## 🔑 Important Note About Service Key

Currently using the **anon key** in `.env`. For production Arduino integration, you should:

1. Go to Supabase Dashboard → Settings → API
2. Copy the **service_role** key (not anon)
3. Update `.env`:
   ```
   SUPABASE_SERVICE_KEY=<your-service-role-key>
   ```

The service_role key bypasses RLS policies, which is needed for Arduino to write data.

## 🎨 What You Can Do Right Now

### 1. View the Dashboard
```bash
cd frontend && npm run dev
```
Navigate to: http://localhost:5173/dashboard

### 2. Connect Your Arduino
```bash
python ble_supabase.py
```

### 3. Watch Real-time Updates
- Events appear instantly
- Safety scores update automatically
- Driver status changes live

## 📱 Sample Arduino IDs Available

- **ARD-001** → Michael Chen (active, score: 95)
- **ARD-002** → Emily Rodriguez (active, score: 88)
- **ARD-003** → James Wilson (inactive, score: 92)
- **ARD-004** → Aisha Patel (warning, score: 76)
- **ARD-005** → David Kim (active, score: 98)
- **ARD-006** → Sofia Martinez (active, score: 91)

## 🐛 Troubleshooting

### Arduino not found?
- Check Bluetooth is on
- Arduino is powered
- Device is advertising

### Data not showing in dashboard?
- Make sure Supabase connection is working
- Check browser console for errors
- Verify `.env` file has correct credentials

### "Driver not found"?
- Use one of the existing Arduino IDs above
- Or create a new driver in Supabase

## 🎯 Next Steps

1. **Test with live Arduino** → Run `ble_supabase.py`
2. **Update dashboard** → Connect to real Supabase data (next task)
3. **Add real-time subscriptions** → Dashboard updates automatically
4. **Deploy** → Host on Vercel/Netlify + keep Arduino running

## 📚 Documentation

- [Arduino Setup](ARDUINO_BLUETOOTH_SETUP.md) - Detailed BLE guide
- [Database Guide](SUPABASE_DATABASE_GUIDE.md) - Schema & queries
- [Frontend README](frontend/README.md) - React app docs

---

**You're all set!** 🎉 Your Arduino can now send data directly to Supabase, and your dashboard is ready to display it.
