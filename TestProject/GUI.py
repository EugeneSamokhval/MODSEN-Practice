from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.tab import MDTabs
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatIconButton
import os


class App(MDApp):
    def build(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        Window.size = (1920, 1080)
        Window.fullscreen = "auto"
        return MainScreen()


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Main screen attributes
        Window.bind(on_keyboard=self.events)
        self.md_bg_color = "#1C1C1C"
        # Agumnetation tab attributes
        main_window_layout = MDStackLayout()
        main_window_layout.orientation = "lr-tb"
        main_window_layout.size_hint = (1, 1)
        main_window_layout.md_bg_color = "#3F3F3F"
        # Transformations list layout
        transformations_layout = MDGridLayout(
            cols=1, size_hint=(0.2, 0.6), padding=20)
        transformations_layout.md_bg_color = "#1C1C1C"
        # Table of images and their's attributes
        image_table = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ('№', dp(30)),
                ('Title', dp(60)),
                ('Resolution', dp(50)),
                ('Format', dp(30)),
                ('intact', dp(30))
            ],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
            size_hint=(0.8, 0.6),
            pos_hint=(1, 1)
        )
        image_table.padding = 60
        # File manager definition and attributes
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[],
            preview=True,
        )
        # Open Path to Input button
        input_button = MDRectangleFlatButton()
        input_button.padding = 20
        input_button.size_hint = (0.1, 0.05)
        input_button.text = 'Choose input path'
        input_button.on_press = lambda: self.file_manager_opener(True)
        # Open path to output button
        output_button = MDRectangleFlatButton()
        output_button.padding = 20
        output_button.size_hint = (0.1, 0.05)
        output_button.text = 'Choose output path'
        output_button.on_press = lambda: self.file_manager_opener(False)
        # Start transformations
        start_button = MDFillRoundFlatIconButton()

        # Add widgets to their's parents
        main_window_layout.add_widget(image_table)
        main_window_layout.add_widget(transformations_layout)
        main_window_layout.add_widget(input_button)
        main_window_layout.add_widget(output_button)
        main_window_layout.add_widget(start_button)
        self.add_widget(main_window_layout)

    def file_manager_opener(self, is_input: bool):
        self.manager_open = True
        path = os.path.expanduser("~")

        self.file_manager.show(path)

    def select_path(self, path):
        self.exit_manager()
        toast(path)

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27) and self.manager_open:
            self.file_manager.back()
        elif keyboard == 27:
            quit()
        return True

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
