# Supabase Database Guide - Driver Monitoring System

## Database Schema Overview

Your Supabase database is now set up with a hybrid real-time architecture for live driver monitoring.

### Tables Created

#### 1. **supervisors**
Stores supervisor/fleet manager information
```sql
- id (UUID, primary key)
- user_id (UUID, references auth.users)
- name (TEXT)
- email (TEXT, unique)
- role (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

#### 2. **drivers**
Stores driver information and Arduino associations
```sql
- id (UUID, primary key)
- supervisor_id (UUID, foreign key)
- name (TEXT)
- email (TEXT, unique)
- arduino_id (TEXT, unique) - Links to Arduino device
- status (TEXT: 'active', 'inactive', 'warning')
- safety_score (INTEGER, 0-100)
- total_trips (INTEGER)
- last_active (TIMESTAMP)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

#### 3. **driving_sessions**
Tracks individual driving trips/sessions
```sql
- id (UUID, primary key)
- driver_id (UUID, foreign key)
- arduino_id (TEXT)
- started_at (TIMESTAMP)
- ended_at (TIMESTAMP, nullable)
- status (TEXT: 'active', 'completed')
- total_swerving (INTEGER)
- total_harsh_brake (INTEGER)
- total_aggressive (INTEGER)
- total_events (INTEGER)
- safety_score (INTEGER)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

#### 4. **sensor_readings**
Raw sensor data from Arduino (for detailed analysis)
```sql
- id (UUID, primary key)
- session_id (UUID, foreign key)
- arduino_id (TEXT)
- timestamp (TIMESTAMP)
- x (FLOAT) - X-axis accelerometer
- y (FLOAT) - Y-axis accelerometer
- z (FLOAT) - Z-axis accelerometer
- event_type (TEXT: 'SWERVING', 'HARSH_BRAKE', 'AGGRESSIVE', 'NORMAL', null)
- count_at_time (INTEGER)
- created_at (TIMESTAMP)
```

#### 5. **events**
Aggregated safety events (optimized for dashboard)
```sql
- id (UUID, primary key)
- session_id (UUID, foreign key)
- driver_id (UUID, foreign key)
- arduino_id (TEXT)
- event_type (TEXT: 'SWERVING', 'HARSH_BRAKE', 'AGGRESSIVE')
- timestamp (TIMESTAMP)
- x, y, z (FLOAT)
- count_at_time (INTEGER)
- severity (TEXT: 'low', 'medium', 'high')
- created_at (TIMESTAMP)
```

## Database Functions

### 1. **get_supervisor_dashboard(supervisor_uuid)**
Returns real-time dashboard data for a supervisor
```sql
SELECT * FROM get_supervisor_dashboard('supervisor-uuid-here');
```

Returns:
- driver_id, driver_name, driver_email
- arduino_id, status, last_active
- trips_today, safety_score
- active_session_id

### 2. **calculate_safety_score(session_uuid)**
Calculates safety score based on events
```sql
SELECT calculate_safety_score('session-uuid-here');
```

## How to Use in Your Frontend

### 1. **Fetch Drivers for Dashboard**
```javascript
import { supabase } from './lib/supabase'

// Get all drivers for logged-in supervisor
const { data: drivers, error } = await supabase
  .from('drivers')
  .select('*')
  .order('last_active', { ascending: false })

// Get drivers with their active sessions
const { data: driversWithSessions } = await supabase
  .from('drivers')
  .select(`
    *,
    driving_sessions!inner(*)
  `)
  .eq('driving_sessions.status', 'active')
```

### 2. **Real-time Updates (Subscribe to Changes)**
```javascript
// Subscribe to driver status changes
const driverSubscription = supabase
  .channel('driver-changes')
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'drivers' },
    (payload) => {
      console.log('Driver updated:', payload.new)
      // Update your UI
    }
  )
  .subscribe()

// Subscribe to new events
const eventSubscription = supabase
  .channel('event-alerts')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'events' },
    (payload) => {
      console.log('New event:', payload.new)
      // Show alert notification
    }
  )
  .subscribe()
```

### 3. **Get Events for a Driver**
```javascript
const { data: events } = await supabase
  .from('events')
  .select('*')
  .eq('driver_id', driverId)
  .order('timestamp', { ascending: false })
  .limit(10)
```

### 4. **Get Active Sessions**
```javascript
const { data: activeSessions } = await supabase
  .from('driving_sessions')
  .select(`
    *,
    drivers(name, email, arduino_id)
  `)
  .eq('status', 'active')
```

## Arduino Integration

### Send Sensor Data to Supabase

Your Arduino should send data to a backend API that then stores it in Supabase:

**Example Payload:**
```json
{
  "arduino_id": "ARD-001",
  "x": 0.19,
  "y": 0.74,
  "z": 1.22,
  "event_type": "SWERVING",
  "count": 1
}
```

**Backend Processing:**
1. Find or create active session for Arduino
2. Insert sensor reading
3. If event detected, insert into events table
4. Triggers automatically update session stats

### Example Backend Endpoint (Python/FastAPI)
```python
@app.post("/sensor-data")
async def receive_sensor_data(data: SensorData):
    # Find active session or create new one
    session = await get_or_create_session(data.arduino_id)

    # Insert sensor reading
    await supabase.table('sensor_readings').insert({
        'session_id': session['id'],
        'arduino_id': data.arduino_id,
        'x': data.x,
        'y': data.y,
        'z': data.z,
        'event_type': data.event_type,
        'count_at_time': data.count
    }).execute()

    # If event detected, insert into events
    if data.event_type in ['SWERVING', 'HARSH_BRAKE', 'AGGRESSIVE']:
        await supabase.table('events').insert({
            'session_id': session['id'],
            'driver_id': session['driver_id'],
            'arduino_id': data.arduino_id,
            'event_type': data.event_type,
            'x': data.x,
            'y': data.y,
            'z': data.z,
            'count_at_time': data.count,
            'severity': calculate_severity(data)
        }).execute()

    return {"status": "success"}
```

## Sample Data Included

The database includes sample data:
- 1 Supervisor: Sarah Johnson
- 6 Drivers with different statuses
- Active driving sessions for 2 drivers
- Sample events (swerving, harsh braking, aggressive driving)

## Next Steps

1. **Update Dashboard** to fetch from Supabase instead of mock data
2. **Set up real-time subscriptions** for live updates
3. **Create Arduino API endpoint** to receive sensor data
4. **Link supervisor to auth user** after login
5. **Build event notification system**

## Security (RLS Enabled)

- Supervisors can only see their own drivers
- Arduino devices can insert sensor data (via service role)
- All sensitive data is protected with Row Level Security

## Environment Variables

Already configured in `/frontend/.env`:
```
VITE_SUPABASE_URL=https://mlztlnewoxxazrquimkk.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```
