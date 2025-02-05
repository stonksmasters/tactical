# src/main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from front_end.screens.radar_screen import RadarScreen
from front_end.screens.history_screen import HistoryScreen
from front_end.screens.filters_screen import FiltersScreen

class TacticalSignalTrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(RadarScreen(name="radar"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(FiltersScreen(name="filters"))
        return sm

if __name__ == "__main__":
    TacticalSignalTrackerApp().run()
