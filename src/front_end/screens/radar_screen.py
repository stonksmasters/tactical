# src/front_end/screens/radar_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
import math

# Import the backend signal processor
from back_end.signal_processor import process_signal

class RadarWidget(Widget):
    def __init__(self, **kwargs):
        super(RadarWidget, self).__init__(**kwargs)
        self.angle = 0
        self.signals = []  # List of (bearing, distance) tuples

    def update(self, dt):
        self.angle = (self.angle + 2) % 360
        self.canvas.clear()
        with self.canvas:
            # Draw radar circle
            Color(0, 0.5, 0, 1)  # Dark green
            radius = min(self.width, self.height) / 2 - 10
            Line(circle=(self.center_x, self.center_y, radius), width=2)
            # Draw sweep line
            Color(0, 1, 0, 0.5)
            x2 = self.center_x + math.cos(math.radians(self.angle)) * radius
            y2 = self.center_y + math.sin(math.radians(self.angle)) * radius
            Line(points=[self.center_x, self.center_y, x2, y2], width=2)
            # Draw signal blips
            for bearing, distance in self.signals:
                # Scale distance (1 unit = 10 pixels), capped by radar radius
                dist_pixels = min(distance * 10, radius)
                x = self.center_x + math.cos(math.radians(bearing)) * dist_pixels
                y = self.center_y + math.sin(math.radians(bearing)) * dist_pixels
                Color(0, 1, 0, 1)
                Ellipse(pos=(x - 5, y - 5), size=(10, 10))

class RadarScreen(Screen):
    def __init__(self, **kwargs):
        super(RadarScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        # Radar widget (60% height)
        self.radar_widget = RadarWidget(size_hint=(1, 0.6))
        layout.add_widget(self.radar_widget)

        # Signal information panel (30% height)
        self.intel_panel = BoxLayout(orientation="vertical", size_hint=(1, 0.3))
        self.signal_type = Label(text="No Signal Detected", font_size=24, halign="center")
        self.signal_freq = Label(text="Frequency: N/A", font_size=18, halign="center")
        self.signal_dist = Label(text="Distance: N/A", font_size=18, halign="center")
        self.signal_threat = Label(text="Threat: Low", font_size=18, halign="center", color=(0, 1, 0, 1))
        self.intel_panel.add_widget(self.signal_type)
        self.intel_panel.add_widget(self.signal_freq)
        self.intel_panel.add_widget(self.signal_dist)
        self.intel_panel.add_widget(self.signal_threat)
        layout.add_widget(self.intel_panel)

        # Bottom toolbar (10% height)
        toolbar = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        self.scan_button = Button(text="Scan", on_press=self.start_scan)
        self.filter_button = Button(text="Filters", on_press=self.show_filters)
        self.history_button = Button(text="History", on_press=self.show_history)
        toolbar.add_widget(self.scan_button)
        toolbar.add_widget(self.filter_button)
        toolbar.add_widget(self.history_button)
        layout.add_widget(toolbar)

        self.add_widget(layout)

        # Schedule updates: smooth radar animation and signal polling
        Clock.schedule_interval(self.radar_widget.update, 0.05)
        Clock.schedule_interval(self.update_signals, 1.0)

    def start_scan(self, instance):
        # Trigger a manual scan
        self.update_signals(0)

    def show_filters(self, instance):
        self.manager.current = "filters"

    def show_history(self, instance):
        self.manager.current = "history"

    def update_signals(self, dt):
        # Get new signal data from the backend
        signal_data = process_signal()
        if signal_data:
            self.radar_widget.signals = [(signal_data["bearing"], signal_data["distance"])]
            self.signal_type.text = signal_data["classification"]
            self.signal_freq.text = "Frequency: " + signal_data["frequency"]
            self.signal_dist.text = "Distance: ~{:.1f}m".format(signal_data["distance"])
            self.signal_threat.text = "Threat: " + signal_data["threat"]
            # Set threat color: green for Low, red for High
            if signal_data["threat"] == "Low":
                self.signal_threat.color = (0, 1, 0, 1)
            else:
                self.signal_threat.color = (1, 0, 0, 1)
