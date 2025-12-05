#.\.venv\Scripts\Activate.ps1
#python teensy.py

import time
import random

USE_FAKE_DATA = True

def get_teensy_reading():
    """Generates mock high-speed data common for Teensy projects."""
    analog_val = random.randint(0, 1023)
    voltage = round((analog_val * 3.3) / 1023, 3)
    return analog_val, voltage

def main():
    print("Starting Teensy Simulation...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            if USE_FAKE_DATA:
                raw_val, volts = get_teensy_reading()
                print(f"Teensy Output -> Raw: {raw_val} | Voltage: {volts}V")
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    main()