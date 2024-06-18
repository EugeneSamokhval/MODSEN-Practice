import images_collecting
import os
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.tab import MDTabs
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton
import image_transformation


class App(MDApp):
    def build(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        Window.size = (1920, 1080)
        Window.fullscreen = "auto"
        return MainScreen()


def transform_items_constructor(widgets: list, columns=3):
    result = MDGridLayout(cols=columns)
    result.size_hint = (0.5, 0.05)
    result.radius = 15
    result.md_bg_color = '#3F3F3F'
    for widget in widgets:
        result.add_widget(widget)
    return result


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load-Uload buffer variables
        self.is_input = None
        self.images_load_path = ''
        self.images_unload_path = ''
        # Main screen attributes
        Window.bind(on_keyboard=self.events)
        self.md_bg_color = "#1C1C1C"
        # Agumnetation tab attributes
        main_window_layout = MDStackLayout()
        main_window_layout.orientation = "lr-tb"
        main_window_layout.size_hint = (1, 1)
        main_window_layout.md_bg_color = "#3F3F3F"
        main_window_layout.spacing = 50
        # Transformations list layout
        transform_layout = MDGridLayout(
            cols=1, size_hint=(0.2, 0.6), padding=20)
        transform_layout.md_bg_color = "#1C1C1C"
        # Checkboxes container
        self.checkboxes = dict()
        check_list = [MDCheckbox(size_hint=(0.1, 0.1)) for i in range(4)]
        # Resize item
        self.checkboxes[check_list[0]] = [MDTextFieldRect(hint_text='Input width', size_hint=(
            0.35, 0.1)), MDTextFieldRect(hint_text='Input height', size_hint=(0.35, 0.1))]
        resize_widget = transform_items_constructor([
            check_list[0],
            MDLabel(text="Resize", size_hint=(0.25, 0.1)),
            self.checkboxes.get(check_list[0])[0],
            self.checkboxes.get(check_list[0])[1],
        ], columns=4)
        # cutout item
        self.checkboxes[check_list[1]] = [MDTextFieldRect(
            hint_text='Input top left point [x, y]', size_hint=(0.35, 0.1)),
            MDTextFieldRect(
                hint_text='Input bottom right point [x, y]', size_hint=(0.35, 0.1))]
        cutout_widget = transform_items_constructor([
            check_list[1],
            MDLabel(text="Cut", size_hint=(0.25, 0.1)),
            self.checkboxes.get(check_list[1])[0],
            self.checkboxes.get(check_list[1])[1]
        ], columns=4)
        # flip item
        self.checkboxes[check_list[2]] = [MDTextFieldRect(hint_text='Is flip horisontal?',
                                                          size_hint=(0.7, 0.1))]
        flip_widget = transform_items_constructor([
            check_list[2],
            MDLabel(text="Flip", size_hint=(0.25, 0.1)),
            self.checkboxes.get(check_list[2])[0]
        ])
        # rotate item
        self.checkboxes[check_list[3]] = [MDTextFieldRect(
            hint_text='Input center [x, y]', size_hint=(0.35, 0.1)),
            MDTextFieldRect(
                hint_text='Input angle of rotation', size_hint=(0.35, 0.1)),]
        rotate_widget = transform_items_constructor([
            check_list[3],
            MDLabel(text="Rotate", size_hint=(0.25, 0.1)),
            self.checkboxes.get(check_list[3])[0],
            self.checkboxes.get(check_list[3])[1],
        ], columns=4)
        # Table of images and their's attributes
        self.image_table = MDDataTable(
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
        self.image_table.padding = 25
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
        start_button = MDFloatingActionButton()
        start_button.icon = 'send-variant-outline'
        start_button.size = (25, 25)
        start_button.font_size = 24
        start_button.text_color = '#FFFFFF'
        start_button.padding = 10
        start_button.pos_hint = {'x': 0.8, 'y': 0.5}
        start_button.on_press = self.start_processing
        # Add widgets to their's parents
        transform_layout.add_widget(resize_widget)
        transform_layout.add_widget(cutout_widget)
        transform_layout.add_widget(flip_widget)
        transform_layout.add_widget(rotate_widget)
        main_window_layout.add_widget(self.image_table)
        main_window_layout.add_widget(transform_layout)
        main_window_layout.add_widget(input_button)
        main_window_layout.add_widget(output_button)
        main_window_layout.add_widget(start_button)
        self.add_widget(main_window_layout)

    def start_processing(self):
        if self.images_load_path and self.images_unload_path:
            to_do_list = []
            for func, key in zip(image_transformation.fuct_list, self.checkboxes.keys()):
                if key.active:
                    func_inputs = []
                    for textfield in self.checkboxes.get(key):
                        if ']' in textfield.text:
                            func_inputs.append([int(entry) for entry in textfield.text.strip(
                                ']').strip('[').split(', ')])
                        else:
                            func_inputs.append(int(textfield.text))
                    to_do_list.append([func, func_inputs])
            images = images_collecting.load_images(self.images_load_path)
            needed_images = []
            checked_names = [i[1] for i in self.image_table.get_row_checks()]
            for image in images:
                for name in checked_names:
                    if name in image[1]:
                        needed_images.append(image)
                        break
            result = []
            for image in needed_images:
                temp_image = image[0]
                for func in to_do_list:
                    temp_image = func[0](temp_image, *func[1])
                result.append([temp_image, image[1].split('\\')[-1]])
            images_collecting.save_images(result, PATH=self.images_unload_path)
            toast('New images are saved at ', self.images_unload_path)
        else:
            toast('You need to choose upload and import paths')

    def load_images(self, path):
        new_images = images_collecting.read_images_attributes(path)
        if new_images:
            self.image_table.row_data = new_images
        else:
            toast("No images inside of the choosen dirrectory")

    def file_manager_opener(self, is_input: bool):
        self.manager_open = True
        self.is_input = is_input
        path = os.path.expanduser("~")
        self.file_manager.show(path)

    def select_path(self, path):
        self.exit_manager()
        self.load_images(path)
        if self.is_input:
            self.images_load_path = path
        else:
            self.images_unload_path = path
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
