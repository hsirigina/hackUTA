#!/usr/bin/env python3
"""
Master Monitoring Script
Runs both Arduino BLE monitoring and Attention monitoring simultaneously
"""
import asyncio
import subprocess
import sys
import signal
import os

class MonitoringManager:
    def __init__(self):
        self.ble_process = None
        self.attention_process = None
        self.running = True

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n🛑 Stopping all monitoring processes...")
        self.running = False

        if self.ble_process:
            print("   Stopping BLE monitoring...")
            self.ble_process.terminate()
            self.ble_process.wait()
            print("   ✓ BLE monitoring stopped")

        if self.attention_process:
            print("   Stopping attention monitoring...")
            self.attention_process.terminate()
            self.attention_process.wait()
            print("   ✓ Attention monitoring stopped")

        print("\n✅ All processes stopped successfully")
        sys.exit(0)

    def run(self):
        """Start both monitoring processes"""
        print("\n" + "="*60)
        print("🚗 DRIVER MONITORING SYSTEM")
        print("="*60)
        print("\nStarting monitoring processes...")
        print("Press Ctrl+C to stop all monitoring\n")

        # Set up signal handler for Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

        try:
            # Start BLE monitoring in background
            print("🔵 Starting Arduino BLE monitoring...")
            self.ble_process = subprocess.Popen(
                [sys.executable, 'ble_supabase.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            print("   ✓ BLE monitoring started (PID: {})".format(self.ble_process.pid))

            # Wait a bit for session to be created
            print("\n⏳ Waiting 3 seconds for session initialization...")
            import time
            time.sleep(3)

            # Start attention monitoring
            print("\n👁️ Starting attention monitoring...")
            self.attention_process = subprocess.Popen(
                [sys.executable, 'attention_supabase.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            print("   ✓ Attention monitoring started (PID: {})".format(self.attention_process.pid))

            print("\n" + "="*60)
            print("✅ ALL MONITORING ACTIVE")
            print("="*60)
            print("\n📊 Monitoring Output:")
            print("-"*60 + "\n")

            # Monitor both processes and display output
            while self.running:
                # Check if processes are still running
                if self.ble_process.poll() is not None:
                    print("\n⚠️  BLE monitoring process ended unexpectedly")
                    break

                if self.attention_process.poll() is not None:
                    print("\n⚠️  Attention monitoring process ended unexpectedly")
                    break

                # Read output from BLE process
                if self.ble_process.stdout:
                    ble_line = self.ble_process.stdout.readline()
                    if ble_line:
                        print(f"[BLE] {ble_line}", end='')

                # Read output from attention process
                if self.attention_process.stdout:
                    attention_line = self.attention_process.stdout.readline()
                    if attention_line:
                        print(f"[CAM] {attention_line}", end='')

                time.sleep(0.1)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            self.signal_handler(None, None)

def main():
    manager = MonitoringManager()
    manager.run()

if __name__ == "__main__":
    main()
