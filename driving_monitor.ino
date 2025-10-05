#include <Arduino_LSM9DS1.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include <ArduinoBLE.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// BLE Service and Characteristic
BLEService drivingService("12345678-1234-1234-1234-123456789abc");
BLEStringCharacteristic drivingData("87654321-4321-4321-4321-cba987654321", BLERead | BLENotify, 100);

const float HARSH_BRAKE_THRESHOLD = 0.5;
const float HARSH_ACCEL_THRESHOLD = 0.4;
const float SWERVE_THRESHOLD = 0.6;
const int TIME_WINDOW = 60000;
const int AGGRESSIVE_EVENT_LIMIT = 3;
const int EVENT_COOLDOWN = 3000;

int aggressiveEventCount = 0;
unsigned long windowStartTime = 0;
unsigned long lastEventTime = 0;

void setup() {
  Serial.begin(115200);
  
  // Initialize OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println("OLED failed!");
    while (1);
  }
  
  // Initialize IMU
  if (!IMU.begin()) {
    Serial.println("IMU failed!");
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("IMU FAILED!");
    display.display();
    while (1);
  }
  
  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("BLE failed!");
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("BLE FAILED!");
    display.display();
    while (1);
  }
  
  // Set BLE device name and service
  BLE.setLocalName("Driving Monitor");
  BLE.setAdvertisedService(drivingService);
  drivingService.addCharacteristic(drivingData);
  BLE.addService(drivingService);
  
  // Start advertising
  BLE.advertise();
  
  windowStartTime = millis();
  
  // Show startup message
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Driving Monitor");
  display.println("BLE: Advertising");
  display.println("Events: 0");
  display.println("Status: Ready");
  display.display();
  
  Serial.println("Driving Monitor with BLE Started");
  Serial.println("Look for 'Driving Monitor' in BLE devices");
}

void updateDisplay(String eventType, int eventCount, String status) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  display.setCursor(0, 0);
  display.println("Driving Monitor");
  display.println("BLE: Connected");
  display.println("---------------");
  
  if (eventType != "") {
    display.println("Event: " + eventType);
  } else {
    display.println("Event: None");
  }
  
  display.println("Count: " + String(eventCount));
  display.println("Status: " + status);
  
  display.display();
}

void sendBLEData(String data) {
  if (BLE.connected()) {
    drivingData.writeValue(data);
    Serial.println("BLE Sent: " + data);
  }
}

void loop() {
  // Listen for BLE connections
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.println("Connected to: " + central.address());
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("BLE Connected!");
    display.display();
    
    while (central.connected()) {
      float ax, ay, az;
      
      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(ax, ay, az);
        
        bool aggressiveEvent = false;
        String eventType = "";
        
        if (ax < -HARSH_BRAKE_THRESHOLD) {
          eventType = "HARSH_BRAKE";
          aggressiveEvent = true;
        }
        
        if (ax > HARSH_ACCEL_THRESHOLD) {
          eventType = "AGGRESSIVE";
          aggressiveEvent = true;
        }
        
        if (abs(ay) > SWERVE_THRESHOLD) {
          eventType = "SWERVING";
          aggressiveEvent = true;
        }
        
        // Send data via BLE
        String dataString = String(ax) + "," + String(ay) + "," + String(az) + "," + eventType + "," + String(aggressiveEventCount);
        sendBLEData(dataString);
        
        // Only count events once per cooldown period
        if (aggressiveEvent && (millis() - lastEventTime > EVENT_COOLDOWN)) {
          Serial.println(eventType);
          aggressiveEventCount++;
          lastEventTime = millis();
          
          // Send event notification
          sendBLEData("EVENT:" + eventType + ":" + String(aggressiveEventCount));
          updateDisplay(eventType, aggressiveEventCount, "Event Detected");
        }
        
        if (millis() - windowStartTime > TIME_WINDOW) {
          String status;
          if (aggressiveEventCount >= AGGRESSIVE_EVENT_LIMIT) {
            status = "AGGRESSIVE";
            sendBLEData("STATUS:AGGRESSIVE:" + String(aggressiveEventCount));
          } else {
            status = "SAFE";
            sendBLEData("STATUS:SAFE:" + String(aggressiveEventCount));
          }
          
          updateDisplay("", aggressiveEventCount, status);
          aggressiveEventCount = 0;
          windowStartTime = millis();
        }
        
        // Update display every 5 seconds
        static unsigned long lastDisplayUpdate = 0;
        if (millis() - lastDisplayUpdate > 5000) {
          updateDisplay("", aggressiveEventCount, "Monitoring");
          lastDisplayUpdate = millis();
        }
      }
      
      delay(20);
    }
    
    Serial.println("Disconnected");
  }
}
