import images_collecting
import os
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton
import image_transformation
import image_posteffects


class App(MDApp):
    def build(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        Window.size = (1920, 1080)
        Window.fullscreen = "auto"
        bottom_navigation_layout = MDBottomNavigation(
            selected_color_background="orange", text_color_active="lightgrey")
        # bottom navigation tab description
        main_window_container = MDBottomNavigationItem()
        main_window_container.text = "Augmentation"
        main_window_container.icon = 'image-edit-outline'
        main_window_container.md_bg_color = '#3F3F3F'
        image_generation_container = ""
        main_window_container.add_widget(MainScreen())
        bottom_navigation_layout.add_widget(main_window_container)
        return bottom_navigation_layout


def transform_items_constructor(widgets: list, columns=3):
    result = MDGridLayout(cols=columns)
    result.size_hint = (None, None)
    result.size = (350, 65)
    result.spacing = 10
    result.radius = 15
    result.md_bg_color = '#3F3F3F'
    for widget in widgets:
        result.add_widget(widget)
    return result


class ImageGenerationScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load-Uload buffer variables
        self.my_selections = []
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
            cols=1, size_hint=(0.2, 0.7), padding=20)
        transform_layout.md_bg_color = "#1C1C1C"
        transform_layout.spacing = 10
        # Checkboxes container
        self.checkboxes = dict()
        check_list = [MDCheckbox(size_hint=(0.1, 0.1)) for i in range(9)]
        # Resize item
        self.checkboxes[check_list[0]] = [MDTextField(hint_text='width', size_hint=(
            0.35, 0.08)), MDTextField(hint_text='height', size_hint=(0.35, 0.1))]
        resize_widget = transform_items_constructor([
            check_list[0],
            MDLabel(text="Resize", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[0])[0],
            self.checkboxes.get(check_list[0])[1],
        ], columns=4)
        # cutout item
        self.checkboxes[check_list[1]] = [MDTextField(
            hint_text='top left point [x, y]', size_hint=(0.35, 0.1)),
            MDTextField(
                hint_text='bottom right point [x, y]', size_hint=(0.35, 0.1))]
        cutout_widget = transform_items_constructor([
            check_list[1],
            MDLabel(text="Cut", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[1])[0],
            self.checkboxes.get(check_list[1])[1]
        ], columns=4)
        # flip item
        self.checkboxes[check_list[2]] = [MDTextField(hint_text='Is flip horisontal?',
                                                      size_hint=(0.7, 0.1))]
        flip_widget = transform_items_constructor([
            check_list[2],
            MDLabel(text="Flip", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[2])[0]
        ])
        # rotate item
        self.checkboxes[check_list[3]] = [MDTextField(
            hint_text='center [x, y]', size_hint=(0.35, 0.1)),
            MDTextField(
                hint_text='angle of rotation', size_hint=(0.35, 0.1)),]
        rotate_widget = transform_items_constructor([
            check_list[3],
            MDLabel(text="Rotate", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[3])[0],
            self.checkboxes.get(check_list[3])[1],
        ], columns=4)
        # shift image
        self.checkboxes[check_list[4]] = [MDTextField(
            hint_text='shift horizontal', size_hint=(0.35, 0.1)),
            MDTextField(
            hint_text='shift vertical', size_hint=(0.35, 0.1)),
        ]
        shift_widget = transform_items_constructor([
            check_list[4],
            MDLabel(text="Shift", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[4])[0],
            self.checkboxes.get(check_list[4])[1]
        ], columns=4)
        # change brightness
        self.checkboxes[check_list[5]] = [MDTextField(
            hint_text='scale of changes', size_hint=(0.70, 0.1)),
        ]
        brightness_widget = transform_items_constructor([
            check_list[5],
            MDLabel(text="Brightness", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[5])[0],
        ])
        # change contrast
        self.checkboxes[check_list[6]] = [MDTextField(
            hint_text='scale of changes', size_hint=(0.70, 0.1)),
        ]
        contrast_widget = transform_items_constructor([
            check_list[6],
            MDLabel(text="Contrast", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[6])[0],
        ])
        # add noise
        self.checkboxes[check_list[7]] = [MDTextField(
            hint_text='scale of changes', size_hint=(0.70, 0.1)),
        ]
        noise_widget = transform_items_constructor([
            check_list[7],
            MDLabel(text="Noise", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[7])[0],
        ])
        # change saturation
        self.checkboxes[check_list[8]] = [MDTextField(
            hint_text='scale of changes', size_hint=(0.70, 0.1)),
        ]
        saturation_widget = transform_items_constructor([
            check_list[8],
            MDLabel(text="Saturation", size_hint=(0.15, 0.1)),
            self.checkboxes.get(check_list[8])[0],
        ])

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
        self.image_table.bind(on_check_press=self.on_check)
        self.image_table.header.ids.check.bind(
            on_release=self.on_checkbox_active)
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
        self.input_button = MDRectangleFlatButton()
        self.input_button.padding = 20
        self.input_button.size_hint = (0.1, 0.05)
        self.input_button.text = 'Choose input path'
        self.input_button.on_press = lambda: self.file_manager_opener(True)
        # Open path to output button
        self.output_button = MDRectangleFlatButton()
        self.output_button.padding = 20
        self.output_button.size_hint = (0.1, 0.05)
        self.output_button.text = 'Choose output path'
        self.output_button.on_press = lambda: self.file_manager_opener(False)
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
        transform_layout.add_widget(shift_widget)
        transform_layout.add_widget(brightness_widget)
        transform_layout.add_widget(contrast_widget)
        transform_layout.add_widget(noise_widget)
        transform_layout.add_widget(saturation_widget)
        main_window_layout.add_widget(self.image_table)
        main_window_layout.add_widget(transform_layout)
        main_window_layout.add_widget(self.input_button)
        main_window_layout.add_widget(self.output_button)
        main_window_layout.add_widget(start_button)
        self.add_widget(main_window_layout)

    def on_checkbox_active(self, cb):
        if cb.state == 'normal':
            Clock.schedule_once(self.update_checks, 0)

    def on_check(self, instance, row_data):
        Clock.schedule_once(self.update_checks, 0)

    def update_checks(self, _):
        self.my_selections = []
        table_data = self.image_table.table_data
        for page, selected_cells in table_data.current_selection_check.items():
            for column_index in selected_cells:
                data_index = int(page * table_data.rows_num +
                                 column_index / table_data.total_col_headings)
                self.my_selections.append(table_data.row_data[data_index][0])

    def calcute_to_do(self):
        to_do_list = []
        all_functions = image_transformation.funct_list + image_posteffects.funct_list
        for func, key in zip(all_functions, self.checkboxes.keys()):
            if key.active:
                func_inputs = []
                for textfield in self.checkboxes.get(key):
                    if ']' in textfield.text:
                        func_inputs.append([int(entry) for entry in textfield.text.strip(
                            ']').strip('[').split(', ')])
                    else:
                        func_inputs.append(int(textfield.text))
                to_do_list.append([func, func_inputs])
        return to_do_list

    def start_processing(self):
        try:
            if self.images_load_path and self.images_unload_path:
                to_do_list = self.calcute_to_do()
                images = images_collecting.load_images(self.images_load_path)
                needed_images = []
                checked_names = [self.image_table.row_data[int(i)][1]
                                 for i in self.my_selections]
                for image in images:
                    for name in checked_names:
                        if name == image[1].split('\\')[-1]:
                            needed_images.append(image)
                            break
                result = []
                for image in needed_images:
                    temp_image = image[0]
                    for func in to_do_list:
                        temp_image = func[0](temp_image, *func[1])
                    result.append([temp_image, image[1].split('\\')[-1]])
                images_collecting.save_images(
                    result, PATH=self.images_unload_path)
                toast('New images are saved at ' + self.images_unload_path)
            else:
                toast('You need to choose upload and import paths')
        except:
            toast(
                'Error while converting images. Check the entered data for correctness.')

    def load_images(self, path):
        new_images = images_collecting.read_images_attributes(path)
        if new_images:
            self.image_table.row_data = new_images
        else:
            toast("No images inside of the choosen dirrectory")

    def file_manager_opener(self, is_input: bool):
        self.manager_open = True
        self.is_input = is_input
        path = os.path.expanduser("C:\\")
        self.file_manager.show(path)

    def select_path(self, path):
        self.exit_manager()
        if self.is_input:
            self.load_images(path)
            self.input_button.text = path
            self.images_load_path = path
        else:
            self.images_unload_path = path
            self.output_button.text = path
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
