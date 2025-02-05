# src/back_end/signal_processor.py
from .flipper_comm import get_signal_data
from .coral_inference import classify_signal

def process_signal():
    data = get_signal_data()
    if data is None:
        return None
    classification = classify_signal(data["raw_data"])
    # Simple threat estimation: stronger (less negative) RSSI means Low threat.
    threat = "Low" if data["rssi"] > -60 else "High"
    return {
        "bearing": data["bearing"],
        "distance": data["distance"],
        "rssi": data["rssi"],
        "frequency": data["frequency"],
        "classification": classification,
        "threat": threat
    }
