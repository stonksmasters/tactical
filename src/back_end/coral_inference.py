# src/back_end/coral_inference.py
import numpy as np
import tensorflow as tf

MODEL_PATH = "models/signal_classifier.tflite"

# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def classify_signal(raw_data):
    """
    Expects raw_data as a space-separated string of floats (e.g., "0.1 0.2 ...").
    Adjust preprocessing as needed.
    """
    try:
        values = [float(x) for x in raw_data.split()]
    except Exception as e:
        print("Error processing raw_data:", e)
        input_size = input_details[0]['shape'][1]
        values = [0.0] * input_size
    input_data = np.array([values], dtype=np.float32)
    expected_shape = input_details[0]['shape']
    if input_data.shape != tuple(expected_shape):
        input_data = np.resize(input_data, expected_shape)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    label_index = int(np.argmax(output_data))
    labels = ["Car Key Fob", "NFC Tag", "IR Remote", "Wi-Fi Beacon", "Drone Controller"]
    if label_index < len(labels):
        return labels[label_index]
    else:
        return "Unknown"
