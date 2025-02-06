# test_serial.py
import serial
import time

port = "/dev/ttyACM0"  # or "COM3" on Windows
baudrate = 115200

try:
    ser = serial.Serial(port, baudrate=baudrate, timeout=1)
    time.sleep(2)
    print("Serial connection established on", port)
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print("Received:", line)
except Exception as e:
    print("Error:", e)
