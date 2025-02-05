# src/back_end/flipper_comm.py
import serial
import time
import json
import os

ser = None

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "../../config/app_config.json")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config
    except Exception as e:
        print("Error loading config:", e)
        # Fallback defaults
        return {"serial_port": "/dev/ttyACM0", "baudrate": 115200, "simulate_serial": True}

config = load_config()

def init_serial():
    global ser
    if config.get("simulate_serial", False):
        print("Simulation mode enabled. Not opening a real serial connection.")
        ser = None
        return
    port = config.get("serial_port", "/dev/ttyACM0")
    baudrate = config.get("baudrate", 115200)
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1)
        time.sleep(2)  # Give the port time to initialize
        print("Serial connection established on", port)
    except Exception as e:
        print("Error initializing serial connection:", e)

def get_signal_data():
    global ser
    if ser is None and not config.get("simulate_serial", False):
        init_serial()
    if config.get("simulate_serial", False):
        # Return simulated data when in simulation mode
        import random
        bearing = random.choice([90, 120, 240, 300])
        distance = random.uniform(5, 20)
        rssi = random.uniform(-80, -40)
        frequency = random.choice(["433 MHz", "13.56 MHz", "2.4 GHz"])
        raw_data = " ".join(str(random.uniform(0, 1)) for _ in range(10))
        return {
            "bearing": bearing,
            "distance": distance,
            "rssi": rssi,
            "frequency": frequency,
            "raw_data": raw_data
        }
    try:
        if ser and ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) >= 5:
                    try:
                        bearing = float(parts[0])
                        distance = float(parts[1])
                        rssi = float(parts[2])
                        frequency = parts[3]
                        raw_data = parts[4]
                        return {
                            "bearing": bearing,
                            "distance": distance,
                            "rssi": rssi,
                            "frequency": frequency,
                            "raw_data": raw_data
                        }
                    except Exception as parse_err:
                        print("Error parsing signal data:", parse_err)
                        return None
                else:
                    print("Received incomplete data:", line)
                    return None
        return None
    except Exception as e:
        print("Error reading from Flipper Zero:", e)
        return None
