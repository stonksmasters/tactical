# src/back_end/flipper_comm.py

def get_signal_data():
    global ser
    if ser is None and not config.get("simulate_serial", False):
        init_serial()
    if config.get("simulate_serial", False):
        # Return simulated data (should not be used when verifying real data)
        import random
        bearing = random.choice([90, 120, 240, 300])
        distance = random.uniform(5, 20)
        rssi = random.uniform(-80, -40)
        frequency = random.choice(["433 MHz", "13.56 MHz", "2.4 GHz"])
        raw_data = " ".join(str(random.uniform(0, 1)) for _ in range(10))
        print("Simulated data:", bearing, distance, rssi, frequency, raw_data)
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
            print("Raw data from serial:", line)  # Log the raw serial line
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
        return None  # No data available this cycle
    except Exception as e:
        print("Error reading from Flipper Zero:", e)
        return None
