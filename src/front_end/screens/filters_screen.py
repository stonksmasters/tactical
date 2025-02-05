# src/front_end/screens/filters_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

class FiltersScreen(Screen):
    def __init__(self, **kwargs):
        super(FiltersScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        title = Label(text="Filters", font_size=24, size_hint=(1, 0.2))
        layout.add_widget(title)
        # Toggle buttons for different signal types
        self.rf_toggle = ToggleButton(text="RF", state="down", size_hint=(1, 0.2))
        self.nfc_toggle = ToggleButton(text="NFC", state="down", size_hint=(1, 0.2))
        self.ir_toggle = ToggleButton(text="IR", state="down", size_hint=(1, 0.2))
        layout.add_widget(self.rf_toggle)
        layout.add_widget(self.nfc_toggle)
        layout.add_widget(self.ir_toggle)
        back_button = Button(text="Back", size_hint=(1, 0.2), on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "radar"
