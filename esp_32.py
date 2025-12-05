#.\.venv\Scripts\Activate.ps1
#python esp_32.py

import time
import random

USE_FAKE_DATA = True

def generate_sensor_data():
    """Generates mock sensor data."""
    temp = round(random.uniform(20.0, 30.0), 2)
    humidity = round(random.uniform(40.0, 60.0), 2)
    return temp, humidity

def main():
    print("Starting ESP32 Simulation...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            if USE_FAKE_DATA:
                temp, humidity = generate_sensor_data()
                
                data_packet = f"ESP32_DATA: Temp={temp}C, Humidity={humidity}%"
                
                print(data_packet)
            
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    main()