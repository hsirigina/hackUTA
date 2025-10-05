# Arduino Nano 33 BLE - Quick Start Guide

## 🚀 Running the BLE Monitor

Your Arduino Nano 33 BLE is already programmed with the driving monitor code!

### Quick Start (Easiest)
```bash
./run_ble.sh
```

### Alternative Methods

**With venv activation:**
```bash
source venv/bin/activate
python3 ble.py
```

**Scan for devices:**
```bash
source venv/bin/activate
python3 scan_ble.py
```

---

## 📊 What You'll See

The script connects to your Arduino via Bluetooth and displays:
- **Real-time accelerometer data** (X, Y, Z axes)
- **Driving events** (harsh braking, aggressive acceleration, swerving)
- **Event counts** and timestamps
- **Safety status** (SAFE/AGGRESSIVE)

---

## 🧪 Testing Events

Move/shake the Arduino to trigger events:

| Event Type | How to Trigger | Threshold |
|------------|----------------|-----------|
| **Harsh Brake** | Tilt backward quickly | X < -0.5g |
| **Aggressive Accel** | Tilt forward quickly | X > 0.4g |
| **Swerving** | Shake left/right | Y > 0.6g |

---

## 🔧 Arduino Code Details

**File:** `driving_monitor.ino`

**Features:**
- Uses LSM9DS1 IMU sensor (built-in)
- BLE advertising as "Driving Monitor"
- OLED display support (SSD1306)
- Real-time event detection
- 60-second monitoring windows

**BLE Configuration:**
- Service UUID: `12345678-1234-1234-1234-123456789abc`
- Characteristic UUID: `87654321-4321-4321-4321-cba987654321`
- Device Name: `Driving Monitor`

---

## 📝 Data Format

The Arduino sends data in two formats:

**1. Continuous sensor data:**
```
ax,ay,az,event_type,count
Example: -0.06,0.00,0.96,,0
```

**2. Event notifications:**
```
EVENT:HARSH_BRAKE:3
STATUS:AGGRESSIVE:5
```

---

## ⚙️ Modifying Thresholds

Edit these values in `driving_monitor.ino`:

```cpp
const float HARSH_BRAKE_THRESHOLD = 0.5;    // Braking sensitivity
const float HARSH_ACCEL_THRESHOLD = 0.4;    // Acceleration sensitivity
const float SWERVE_THRESHOLD = 0.6;         // Swerving sensitivity
const int AGGRESSIVE_EVENT_LIMIT = 3;       // Events to trigger alert
const int TIME_WINDOW = 60000;              // Monitoring window (ms)
```

---

## 🐛 Troubleshooting

**Arduino not found?**
- Check Bluetooth is ON on your Mac
- Ensure Arduino is powered and showing "Advertising"
- Run `python3 scan_ble.py` to check if it's visible

**Connection drops?**
- Keep Arduino close to your Mac (< 10 meters)
- Check USB power connection is stable
- Restart the Arduino if needed

**No bleak module?**
- Make sure you activated the venv: `source venv/bin/activate`
- Or use the helper script: `./run_ble.sh`

---

## 📦 Dependencies

The project uses:
- **bleak** - Bluetooth Low Energy library
- **asyncio** - Async I/O for Python
- **Arduino_LSM9DS1** - IMU sensor library
- **ArduinoBLE** - Bluetooth library
- **Adafruit_SSD1306** - OLED display library

---

## 🎯 Next Steps

1. **Test the system** - Move the Arduino and watch for events
2. **Adjust thresholds** - Fine-tune sensitivity for your use case
3. **Integrate with app** - Use the BLE data in your main application
4. **Add features** - Extend the monitoring logic as needed

Happy coding! 🚀
