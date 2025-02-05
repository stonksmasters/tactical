# src/front_end/screens/history_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        title = Label(text="History Log", font_size=24, size_hint=(1, 0.2))
        layout.add_widget(title)
        # Placeholder history data
        history_data = [
            "Car Key Fob - 12:34:56 - ~15m",
            "NFC Tag - 12:36:10 - ~5m"
        ]
        for item in history_data:
            layout.add_widget(Label(text=item, font_size=18))
        back_button = Button(text="Back", size_hint=(1, 0.2), on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "radar"
