import image_generation
import image_posteffects
import image_transformation
import images_collecting
import images_overlay
from typing import Union
import os
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabs
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivymd.uix.button import (
    MDRectangleFlatButton,
    MDFloatingActionButton,
)
from threading import Thread
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDColorPicker


def open_dialog_error(error_text: str) -> None:
    """function which creates and opens dialog window

    Args:
        error_text (str): Text which will be seen on the dialog window

    Returns:
        None: Opens pop up window without returning anything
    """
    dialog_window = MDDialog()
    dialog_window.title = "Error"
    dialog_window.md_bg_color = "#2e0000"
    dialog_window.text = error_text
    return dialog_window.open()


def open_dialog_message(message_text: str) -> None:
    """function which creates and opens dialog window

    Args:
        message_text (str): Text which will be seen on the dialog window

    Returns:
        None: Opens pop up window without returning anything
    """
    dialog_window = MDDialog()
    dialog_window.title = "Message"
    dialog_window.text = message_text
    return dialog_window.open()


class App(MDApp):
    def build(self, **kwargs):
        # app atributes
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        Window.size = (1920, 1080)
        Window.fullscreen = "auto"
        # Screens layout
        self.bottom_navigation_layout = MDBottomNavigation(
            selected_color_background="orange", text_color_active="lightgrey"
        )
        # main window bottom navigation tab description
        self.main_window_container = MDBottomNavigationItem()
        self.main_window_container.text = "Editing"
        self.main_window_container.name = "Editing"
        self.main_window_container.icon = "image-edit-outline"
        self.main_window_container.md_bg_color = "#3F3F3F"
        # generation window bottom navigation tab description
        self.image_generation_container = MDBottomNavigationItem()
        self.image_generation_container.name = "Generation"
        self.image_generation_container.icon = "image-auto-adjust"
        self.image_generation_container.text = "Generation"
        # overlay window bottom navigation tab description
        self.image_overlay_container = MDBottomNavigationItem()
        self.image_overlay_container.name = "Overlay"
        self.image_overlay_container.icon = 'image-multiple-outline'
        self.image_overlay_container.text = 'Overlay'
        # assighning widgets to their's parents
        self.main_window_container.add_widget(MainScreen())
        self.image_generation_container.add_widget(ImageGenerationScreen())
        self.image_overlay_container.add_widget(ImageOverlayScreen())
        self.bottom_navigation_layout.add_widget(self.main_window_container)
        self.bottom_navigation_layout.add_widget(
            self.image_generation_container)
        self.bottom_navigation_layout.add_widget(self.image_overlay_container)
        self.bottom_navigation_layout.on_switch_tabs = self.switch_screens
        return self.bottom_navigation_layout

    def switch_screens(self, next_item: MDTabs, name: str):
        """An dunction to switch between tabs using bottom navigation bar

        Args:
            next_item (MDTabs): link to the clicked tab
            name (str): name of the tab
        """
        self.bottom_navigation_layout.switch_tab(name)


def transform_items_constructor(widgets: list, columns=3):
    """Function for creation of similar transform checkbox included items

    Args:
        widgets (list): all the widgets for transfom item
        columns (int, optional): number of widgets in transform item. Defaults to 3.

    Returns:
        MDGridLayout: an transform item widget
    """
    result = MDGridLayout(cols=columns)
    result.size_hint = (None, None)
    result.size = (350, 65)
    result.spacing = 10
    result.line_color = "#7B7B7B"
    result.radius = 15
    result.md_bg_color = "#1E1E1E"
    for widget in widgets:
        result.add_widget(widget)
    return result


class ImageOverlayScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Buffer variables
        self.images_load_path = ""
        self.overlay_image = ""
        self.images_save_path = ""
        self.current_font_path = ""
        self.current_index = 0
        self.image_paths_list = []
        self.font_color = list()
        # Image overlay windows layout
        overlay_layout = MDGridLayout()
        overlay_layout.cols = 2
        overlay_layout.rows = 2
        overlay_layout.size_hint = (1, 1)
        overlay_layout.md_bg_color = "#1E1E1E"
        overlay_layout.spacing = 50
        # Image wrapper
        image_wrapper = MDGridLayout(cols=1, rows=1)
        image_wrapper.spacing = 20
        image_wrapper.line_color = "#7B7B7B"
        image_wrapper.line_width = 2
        image_wrapper.radius = 30
        image_wrapper.padding = 10
        image_wrapper.size_hint = (0.5, 0.5)
        image_wrapper.size = image_wrapper.minimum_size
        # Current image widget
        self.current_image = AsyncImage()
        self.current_image.size = (800, 800)
        self.current_image.source = "placeholder.png"
        self.current_image.allow_stretch = True
        self.current_image.keep_ratio = False
        # Navigation buttons layout
        navigation_buttons_layout = MDGridLayout()
        navigation_buttons_layout.cols = 2
        navigation_buttons_layout.rows = 1
        navigation_buttons_layout.size = (120, 70)
        navigation_buttons_layout.size_hint = (None, None)
        navigation_buttons_layout.spacing = 10
        # Navigation left button
        self.left_nav_button = MDFloatingActionButton()
        self.left_nav_button.size = (50, 50)
        self.left_nav_button.line_color = "#7B7B7B"
        self.left_nav_button.line_width = 2
        self.left_nav_button.md_bg_color = '#1E1E1E'
        self.left_nav_button.text_color = "#7B7B7B"
        self.left_nav_button.icon = 'arrow-left-bold-outline'
        self.left_nav_button.on_press = self.next_image_left
        # Navigation right button
        self.right_nav_button = MDFloatingActionButton()
        self.right_nav_button.size = (50, 50)
        self.right_nav_button.line_color = "#7B7B7B"
        self.right_nav_button.line_width = 2
        self.right_nav_button.md_bg_color = '#1E1E1E'
        self.right_nav_button.text_color = "#7B7B7B"
        self.right_nav_button.icon = 'arrow-right-bold-outline'
        self.right_nav_button.on_press = self.next_image_right
        # User input layout
        user_input_layout = MDGridLayout(cols=1, rows=5)
        user_input_layout.size_hint = (0.4, 1)
        user_input_layout.spacing = 50
        # Image overlay check box
        self.is_image_overlay = MDCheckbox()
        self.is_image_overlay.size = (50, 60)
        self.is_image_overlay.size_hint = (None, None)
        # Image overlay x position text field
        self.image_x_pos = MDTextField(
            hint_text="x position", size_hint=(0.35, 0.1))
        # Image overlay y position text field
        self.image_y_pos = MDTextField(
            hint_text="y position", size_hint=(0.35, 0.1))
        # Image overlay path opening button
        self.overlay_input_button = MDRectangleFlatButton()
        self.overlay_input_button.padding = 20
        self.overlay_input_button.size_hint = (0.1, 0.05)
        self.overlay_input_button.text = "Choose image to overlay"
        self.overlay_input_button.on_press = lambda: self.file_manager_opener(
            'Over')
        # Image overlay item
        image_overlay_item = transform_items_constructor([self.is_image_overlay, MDLabel(
            text="Image overlay", size_hint=(0.2, 0.1)), self.overlay_input_button, self.image_x_pos, self.image_y_pos], columns=5)
        image_overlay_item.size_hint = (1, None)
        # Text overlay check box
        self.is_text_overlay = MDCheckbox()
        self.is_text_overlay.size = (50, 60)
        self.is_text_overlay.size_hint = (None, None)
        # Text overlay x position text field
        self.text_x_pos = MDTextField(size=(200, 70), padding=25,
                                      hint_text="x position", size_hint=(None, None))
        # Text overlay x position text field
        self.text_y_pos = MDTextField(size=(200, 70), padding=25,
                                      hint_text="y position", size_hint=(None, None))
        # Text overlay font choise button
        self.font_choise_button = MDRectangleFlatButton()
        self.font_choise_button.padding = 20
        self.font_choise_button.size_hint = (None, None)
        self.font_choise_button.size = (200, 70)
        self.font_choise_button.font_style = 'Button'
        self.font_choise_button.text = "Choose overlay font"
        self.font_choise_button.on_press = lambda: self.fonts_dropdown_menu.open()
        # Font size input field
        self.font_size_input_box = MDTextField(
            size=(200, 70), padding=25,
            hint_text="font size", size_hint=(None, None))
        # Font colorpicker
        self.font_colorpicker = MDColorPicker(
            size_hint=(0.45, 0.85)
        )
        self.font_colorpicker.on_release = self.on_colorpicker_press
        # Open font colorpicker button
        self.font_colorpicker_button = MDFloatingActionButton(
            size=(50, 50), size_hint=(None, None), line_color="#7B7B7B", line_width=2, md_bg_color='#1E1E1E', text_color="#7B7B7B"
        )
        self.font_colorpicker_button.icon = 'palette-outline'
        self.font_colorpicker_button.text_color = '#7B7B7B'
        self.font_colorpicker_button.on_press = self.font_colorpicker.open
        # Text overlay item decription
        text_overlay_item = MDStackLayout(orientation='lr-tb')
        for widget in [self.is_text_overlay, MDLabel(
                text="Text overlay", size=(100, 70), size_hint=(None, None)),  self.text_x_pos, self.text_y_pos,  self.font_size_input_box, self.font_colorpicker_button, self.font_choise_button]:
            text_overlay_item.add_widget(widget)
        text_overlay_item.size_hint = (1, None)
        text_overlay_item.line_color = '#7B7B7B'
        text_overlay_item.line_width = 2
        text_overlay_item.spacing = 25
        text_overlay_item.size = (800, 180)
        text_overlay_item.radius = 15
        # Text overlay input box
        self.prompt_field = MDTextField()
        self.prompt_field.mode = "rectangle"
        self.prompt_field.hint_text = "Text for overlay"
        self.prompt_field.size_hint = (0.45, 0.15)
        self.prompt_field.multiline = True
        self.prompt_field.helper_text_mode = "on_error"
        self.prompt_field.required = True
        # Dropdown menu description
        self.fonts_dropdown_menu = MDDropdownMenu()
        self.fill_dropdown_menu()
        self.fonts_dropdown_menu.caller = self.font_choise_button
        # process all images layout
        all_selected_layout = MDGridLayout()
        all_selected_layout.size_hint = (None, None)
        all_selected_layout.cols = 2
        all_selected_layout.rows = 1
        # Process all images checkbox
        self.all_selected_checkbox = MDCheckbox()
        self.all_selected_checkbox.size = (50, 50)
        self.all_selected_checkbox.size_hint = (None, None)
        # Process all images label
        all_selected_label = MDLabel()
        all_selected_label.size_hint = (None, None)
        all_selected_label.size = (350, 40)
        all_selected_label.text = "Save changes for all images?"
        # Path choise layout description
        paths_layout = MDGridLayout()
        paths_layout.size_hint = (0.5, 0.05)
        paths_layout.spacing = 50
        paths_layout.cols = 2
        paths_layout.rows = 1
        # Open Path to Input button
        self.input_button = MDRectangleFlatButton()
        self.input_button.padding = 20
        self.input_button.size_hint = (0.1, 0.05)
        self.input_button.text = "Choose input path"
        self.input_button.on_press = lambda: self.file_manager_opener('Inp')
        # Open path to output button
        self.output_button = MDRectangleFlatButton()
        self.output_button.padding = 20
        self.output_button.size_hint = (0.1, 0.05)
        self.output_button.text = "Choose output path"
        self.output_button.on_press = lambda: self.file_manager_opener('Out')
        # File manager definition and attributes
        self.manager_open = False
        self.manager_mode = ''
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[],
            preview=True,
        )
        # Start processing button
        self.start_button = MDFloatingActionButton()
        self.start_button.icon = "send-variant-outline"
        self.start_button.size = (25, 25)
        self.start_button.font_size = 24
        self.start_button.text_color = "#FFFFFF"
        self.start_button.md_bg_color = "#000000"
        self.start_button.padding = 10
        self.start_button.pos_hint = {"x": 0.8, "y": 0.5}
        self.start_button.on_press = self.start_processing
        # Add widgtets to their's parents
        all_selected_layout.add_widget(self.all_selected_checkbox)
        all_selected_layout.add_widget(all_selected_label)
        paths_layout.add_widget(self.input_button)
        paths_layout.add_widget(self.output_button)
        user_input_layout.add_widget(image_overlay_item)
        user_input_layout.add_widget(text_overlay_item)
        user_input_layout.add_widget(self.prompt_field)
        user_input_layout.add_widget(all_selected_layout)
        user_input_layout.add_widget(self.start_button)
        navigation_buttons_layout.add_widget(self.left_nav_button)
        navigation_buttons_layout.add_widget(self.right_nav_button)
        image_wrapper.add_widget(self.current_image)
        overlay_layout.add_widget(image_wrapper)
        overlay_layout.add_widget(user_input_layout)
        overlay_layout.add_widget(navigation_buttons_layout)
        overlay_layout.add_widget(paths_layout)
        self.add_widget(overlay_layout)

    def on_colorpicker_press(self, color_type: str,
                             selected_color: Union[list, str], *args) -> None:
        """Sets current font colour for text overlaying

        Args:
            color_type (str): returns color format as string
            selected_color (Union[list, str]): Color selected by user in formats RGB, RGBA, HEX
        """
        self.font_color = [
            int(255*selected_color[index]) for index in range(len(selected_color))]
        if len(self.font_color) < 4:
            self.font_color.append(1)
        self.font_colorpicker_button.md_bg_color = selected_color
        self.font_colorpicker.dismiss()
        print(selected_color)

    def next_image_left(self) -> None:
        """Navgation function which switches current displayed image to the left
        """
        if self.current_index > 0:
            self.current_index -= 1
            self.current_image.source = self.image_paths_list[self.current_index]

    def next_image_right(self) -> None:
        """Navgation function which switches current displayed image to the right
        """
        if self.current_index < len(self.image_paths_list)-2:
            self.current_index += 1
            self.current_image.source = self.image_paths_list[self.current_index]

    def text_input_checks(self) -> bool:
        """Checks correctness of user input for text generation fields

        Returns:
            bool: Returns True when all the needed data inputed correctly. In any other case returns False.
        """
        try:
            if int(self.text_x_pos.text) and int(self.text_y_pos.text) and int(self.font_size_input_box.text):
                if self.font_color:
                    if self.current_font_path:
                        if self.prompt_field.text:
                            return True
                        else:
                            open_dialog_error(
                                'You need to write text you want to overlay')
                            return False
                    else:
                        open_dialog_error('You need to choose a font')
                        return False
                else:
                    open_dialog_error('You need to choose a colour')
                return False
            else:
                open_dialog_error(
                    'X position, Y position, and font size needs to be filled')
                return False
        except:
            open_dialog_error(
                'X position, Y position, and font size needs to be an integer')
            return False

    def image_input_checks(self) -> bool:
        """Checks correctness of user input for image generation fields

        Returns:
            bool: Returns True when all the needed data inputed correctly. In any other case returns False.
        """
        try:
            if int(self.image_x_pos.text) and int(self.image_y_pos.text):
                if self.overlay_image:
                    return True
                else:
                    open_dialog_error(
                        'You need to choose image to overlay')
                    return False
            else:
                open_dialog_error(
                    'X position and Y posisition fields weren\'t filled')
                return False
        except:
            open_dialog_error(
                'X position and Y posisition should be integer')
            return False

    def start_processing(self) -> None:
        """Checks correctness of user input.
           Disables start button.
        """
        checks_completed = True
        if self.images_load_path and self.image_paths_list:
            pass
        else:
            checks_completed = False
            open_dialog_error(
                'You need to choose input and output dirrectories')
        if self.is_image_overlay.active:
            checks_completed = self.image_input_checks()
        if self.is_text_overlay.active:
            checks_completed = self.text_input_checks()
        if checks_completed:
            self.start_button.disabled = True
            process = Thread(target=self.add_image_or_text)
            process.start()

    def add_image_or_text(self):
        """Editing imput images to have text and image overlay
        """
        try:
            resulting_images = list()
            if self.all_selected_checkbox.active:
                loaded_images = images_collecting.load_images(
                    self.images_load_path)
            else:
                loaded_images = [[images_collecting.load_exact_image(
                    self.current_image.source), self.current_image.source]]
            for image in loaded_images:
                if self.is_image_overlay.active:
                    image[0] = images_overlay.overlay_images(image[0], images_collecting.load_exact_image(
                        self.overlay_image), int(self.image_x_pos.text), int(self.image_y_pos.text))
                if self.is_text_overlay.active:
                    image[0] = images_overlay.overlay_text(image[0], int(self.text_x_pos.text), int(self.text_y_pos.text),
                                                           self.prompt_field.text,
                                                           self.current_font_path,
                                                           int(self.font_size_input_box.text),
                                                           tuple(
                                                               self.font_color),
                                                           self.font_color[-1]
                                                           )
                resulting_images.append(image)
            named_images_list = [[image[0], image[1].split(
                '\\')[-1]] for image in resulting_images]
            images_collecting.save_images(
                named_images_list, self.images_save_path)
            Clock.schedule_once(self.on_processing_finish)
        except:
            Clock.schedule_once(self.on_processing_finish_error)

    def on_processing_finish(self, *arg):
        """Executed when the function add_image_or_text completes successfully.
            Enables start button.
            Shows dialog message.
        """
        self.start_button.disabled = False
        open_dialog_message('Image overlaying was finished!')

    def on_processing_finish_error(self, *arg):
        """Executed when the function add_image_or_text completes with error.
            Enables start button.
            Shows error message.
        """
        self.start_button.disabled = False
        open_dialog_message(
            'Image overlaying was finished with error please check correctness of input data')

    def fill_dropdown_menu(self):
        """Fills dropown menu with fonts
        """
        self.fonts_dropdown_menu.items = [
            {"text": name, "on_release": lambda name=name: self.set_current_font(name)} for name in images_overlay.load_fonts_names()]

    def set_current_font(self, name: str):
        """When user choses a font from dropdown menu, saves chosen font
        Args:
            name (str): name of chosen font
        """
        try:
            all_paths = images_overlay.load_fonts()
            self.current_font_path = list(filter(
                lambda string: name in string, all_paths))[0]
            self.font_choise_button.text = name
            self.fonts_dropdown_menu.dismiss()
        except:
            open_dialog_error(
                "This font is no longer presented in fonts dirrectory")

    def file_manager_opener(self, mode: str):
        """Opens file manager
        Args:
            mode (str): shows where to write result of manager work
        """
        self.manager_mode = mode
        self.manager_open = True
        path = os.path.expanduser("C:\\")
        self.file_manager.show(path)

    def select_path(self, path: str):
        """Saves chosen path into a buffer

        Args:
            path (str): Chosen path
        """
        self.exit_manager()
        if self.manager_mode == 'Inp':
            self.load_images(path)
            self.input_button.text = path
            self.images_load_path = path
        elif self.manager_mode == 'Out':
            self.images_save_path = path
            self.output_button.text = path
        elif self.manager_mode == 'Over':
            is_image = False
            for defintion in ['.png', '.jpg', '.jpeg', '.bmp']:
                if defintion in path:
                    self.overlay_input_button.text = path.split('\\')[-1]
                    self.overlay_image = path
                    is_image = True
                    break
            if not is_image:
                open_dialog_error('You need to chose image')
        toast(path)

    def exit_manager(self, *args):
        """Closes file manager when called"""
        self.manager_open = False
        self.file_manager.close()

    def load_images(self, path: str):
        """loads data about images into a buffer
        Args:
            path (str): images import path
        """
        new_images = images_collecting.get_images_by_dir(path)
        if new_images:
            self.image_paths_list = new_images
            self.current_image.source = new_images[0]
        else:
            open_dialog_error("No images inside of the choosen dirrectory")


class ImageGenerationScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Buffer variables
        self.images_unload_path = ""
        # image generation window layout
        generation_layout = MDGridLayout()
        generation_layout.md_bg_color = "#1E1E1E"
        generation_layout.cols = 2
        generation_layout.rows = 1
        generation_layout.size_hint = (1, 1)
        generation_layout.spacing = 50
        # Images Layout attributes
        images_layout = MDGridLayout()
        images_layout.spacing = 15
        images_layout.cols = 1
        images_layout.rows = 2
        images_layout.size_hint = (0.5, 1)
        # Image generation input parameters layout
        input_grid = MDGridLayout()
        input_grid.cols = 1
        input_grid.spacing = 40
        input_grid.size_hint = (0.5, 0.8)
        # Prompt input text field
        self.prompt_field = MDTextField()
        self.prompt_field.mode = "rectangle"
        self.prompt_field.hint_text = "Positive prompt"
        self.prompt_field.size_hint = (0.45, 0.15)
        self.prompt_field.multiline = True
        self.prompt_field.max_text_length = 1000
        self.prompt_field.helper_text_mode = "on_error"
        self.prompt_field.required = True
        self.prompt_field.helper_text = "Maximal size of a prompt = 1000"
        # Negative prompt input text field
        self.negative_prompt = MDTextField()
        self.negative_prompt.mode = "rectangle"
        self.negative_prompt.multiline = True
        self.negative_prompt.hint_text = "Negative prompt"
        self.negative_prompt.size_hint = (0.45, 0.15)
        self.negative_prompt.max_text_length = 1000
        self.negative_prompt.helper_text = "Maximal size of a prompt = 1000"
        self.negative_prompt.helper_text_mode = "on_error"
        # Image wrapper
        image_wrapper = MDGridLayout(cols=1, rows=1)
        image_wrapper.spacing = 20
        image_wrapper.line_color = "#7B7B7B"
        image_wrapper.line_width = 2
        image_wrapper.radius = 30
        image_wrapper.padding = 10
        image_wrapper.size = image_wrapper.minimum_size
        # Image placeholder
        self.current_downloaded_image = AsyncImage(source="placeholder.png")
        self.current_downloaded_image.size_hint = (1, 1)
        self.current_downloaded_image.allow_stretch = True
        self.current_downloaded_image.keep_ratio = False
        # Open Path to output button
        self.output_button = MDRectangleFlatButton()
        self.output_button.padding = 20
        self.output_button.size_hint_max = (0.4, 0.05)
        self.output_button.text = "Choose output path"
        self.output_button.on_press = lambda: self.file_manager_opener()
        # Send request button
        self.start_button = MDFloatingActionButton()
        self.start_button.size = (65, 65)
        self.start_button.icon = "send-variant-outline"
        self.start_button.md_bg_color = "#000000"
        self.start_button.radius = 20
        self.start_button.text_color = "#FFFFFF"
        self.start_button.on_press = self.generate_image_checks
        # Width input field
        self.width_textfield = MDTextField()
        self.width_textfield.hint_text = "Width 1-1024"
        self.width_textfield.size_hint = (1, None)
        self.width_textfield.required = True
        self.width_textfield.helper_text_mode = "on_error"
        self.width_textfield.helper_text = "You need to input image's height"
        self.width_textfield.mode = "round"
        self.width_textfield.height = 30
        # Height unput field
        self.height_textfield = MDTextField()
        self.height_textfield.hint_text = "Height 1-1024"
        self.height_textfield.size_hint = (1, None)
        self.height_textfield.required = True
        self.height_textfield.helper_text = "You need to input image's height"
        self.height_textfield.helper_text_mode = "on_error"
        self.height_textfield.mode = "round"
        self.height_textfield.height = 30
        # File manager definition and attributes
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[],
            preview=True,
        )
        # assighning widgets to their's parents
        image_wrapper.add_widget(self.current_downloaded_image)
        images_layout.add_widget(image_wrapper)
        images_layout.add_widget(self.output_button)
        input_grid.add_widget(self.prompt_field)
        input_grid.add_widget(self.negative_prompt)
        input_grid.add_widget(self.width_textfield)
        input_grid.add_widget(self.height_textfield)
        input_grid.add_widget(self.start_button)
        generation_layout.add_widget(images_layout)
        generation_layout.add_widget(input_grid)
        self.add_widget(generation_layout)

    def generate_image_checks(self):
        """Checks for correct input at generatin screen"""
        if self.prompt_field.text:
            if self.images_unload_path:
                try:
                    width_check = int(self.width_textfield.text)
                    height_check = int(self.width_textfield.text)
                    if (width_check > 1024) or (height_check > 1024):
                        open_dialog_error(
                            "Image dimension must be lower than 1024")
                        return None
                    elif (width_check < 0) or (height_check < 0):
                        open_dialog_error(
                            "Image dimension must be higher than 0")
                        return None
                    self.start_button.disabled = True
                    process = Thread(target=self.generate_image)
                    process.start()
                except:
                    open_dialog_error("Width and height need to be numbers")
            else:
                open_dialog_error("Choose download dirrectory")
        else:
            open_dialog_error("Please input prompt")

    def generate_image(self) -> None:
        """
        Function which calls an image generating api and scheldues image update after download
        """
        try:
            images_in_dir = [
                f
                for f in os.listdir(self.images_unload_path)
                if os.path.isfile(os.path.join(self.images_unload_path, f))
            ]
            current_index = 0
            while "ai_img_" + str(current_index) + ".png" in images_in_dir:
                current_index += 1
            self.image_path = (
                self.images_unload_path + "\\ai_img_" +
                str(current_index) + ".png"
            )
            if self.width_textfield and self.height_textfield:
                image = image_generation.get_generated_image(
                    prompt=self.prompt_field.text,
                    negative_prompt=self.negative_prompt.text,
                    width=int(self.width_textfield.text),
                    height=int(self.height_textfield.text),
                )
            else:
                image = image_generation.get_generated_image(
                    prompt=self.prompt_field.text,
                    negative_prompt=self.negative_prompt.text,
                )
            images_collecting.save_images(
                images_list=[(image, "ai_img_" + str(current_index) + ".png")],
                PATH=self.images_unload_path,
            )
            Clock.schedule_once(self.update_image)
        except:
            Clock.schedule_once(self.update_image)

    def update_image(self, *args):
        """updates image on the screen after generation"""
        self.current_downloaded_image.source = self.image_path
        open_dialog_message("Image has been generated!")
        self.start_button.disabled = False

    def error_during_generation(self, *args):
        """Show error pop up and unlock the button
        """
        open_dialog_error(
            "There is an error during generation, check your internet connection.")
        self.start_button.disabled = False

    def file_manager_opener(self):
        """opens file manager"""
        self.manager_open = True
        path = os.path.expanduser("C:\\")
        self.file_manager.show(path)

    def select_path(self, path: str):
        """When user selects exact path this function will save them
        in buffer variable
        Args:
            path (str): chosen path
        """
        self.exit_manager()
        self.images_unload_path = path
        self.output_button.text = path

    def exit_manager(self, *args):
        """Closes file manager when called"""
        self.manager_open = False
        self.file_manager.close()


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load-Uload buffer variables
        self.my_selections = []
        self.is_input = None
        self.images_load_path = ""
        self.images_unload_path = ""
        # Main screen attributes
        Window.bind(on_keyboard=self.events)
        self.md_bg_color = "#1E1E1E"
        # Agumnetation tab attributes
        main_window_layout = MDStackLayout()
        main_window_layout.orientation = "lr-tb"
        main_window_layout.size_hint = (1, 1)
        main_window_layout.md_bg_color = "#1E1E1E"
        main_window_layout.spacing = 35
        # Transformations list layout
        transform_layout = MDGridLayout(cols=1, size_hint=(0.2, 1), padding=20)
        transform_layout.md_bg_color = "#1E1E1E"
        transform_layout.spacing = 10
        # Checkboxes container
        self.checkboxes = dict()
        check_list = [MDCheckbox(size_hint=(0.1, 0.1)) for i in range(10)]
        # Resize item
        self.checkboxes[check_list[0]] = [
            MDTextField(hint_text="width", size_hint=(0.35, 0.08)),
            MDTextField(hint_text="height", size_hint=(0.35, 0.1)),
        ]
        resize_widget = transform_items_constructor(
            [
                check_list[0],
                MDLabel(text="Resize", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[0])[0],
                self.checkboxes.get(check_list[0])[1],
            ],
            columns=4,
        )
        # cutout item
        self.checkboxes[check_list[1]] = [
            MDTextField(
                hint_text="top left point [x, y]", size_hint=(0.35, 0.1)),
            MDTextField(
                hint_text="bottom right point [x, y]", size_hint=(0.35, 0.1)),
        ]
        cutout_widget = transform_items_constructor(
            [
                check_list[1],
                MDLabel(text="Cut", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[1])[0],
                self.checkboxes.get(check_list[1])[1],
            ],
            columns=4,
        )
        # flip item
        self.checkboxes[check_list[2]] = [
            MDTextField(hint_text="Is flip horisontal?", size_hint=(0.7, 0.1))
        ]
        flip_widget = transform_items_constructor(
            [
                check_list[2],
                MDLabel(text="Flip", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[2])[0],
            ]
        )
        # rotate item
        self.checkboxes[check_list[3]] = [
            MDTextField(hint_text="center [x, y]", size_hint=(0.35, 0.1)),
            MDTextField(hint_text="angle of rotation", size_hint=(0.35, 0.1)),
        ]
        rotate_widget = transform_items_constructor(
            [
                check_list[3],
                MDLabel(text="Rotate", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[3])[0],
                self.checkboxes.get(check_list[3])[1],
            ],
            columns=4,
        )
        # shift image
        self.checkboxes[check_list[4]] = [
            MDTextField(hint_text="shift horizontal", size_hint=(0.35, 0.1)),
            MDTextField(hint_text="shift vertical", size_hint=(0.35, 0.1)),
        ]
        shift_widget = transform_items_constructor(
            [
                check_list[4],
                MDLabel(text="Shift", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[4])[0],
                self.checkboxes.get(check_list[4])[1],
            ],
            columns=4,
        )
        # change brightness
        self.checkboxes[check_list[5]] = [
            MDTextField(hint_text="scale of changes", size_hint=(0.70, 0.1)),
        ]
        brightness_widget = transform_items_constructor(
            [
                check_list[5],
                MDLabel(text="Brightness", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[5])[0],
            ]
        )
        # change contrast
        self.checkboxes[check_list[6]] = [
            MDTextField(hint_text="scale of changes", size_hint=(0.70, 0.1)),
        ]
        contrast_widget = transform_items_constructor(
            [
                check_list[6],
                MDLabel(text="Contrast", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[6])[0],
            ]
        )
        # add noise
        self.checkboxes[check_list[7]] = [
            MDTextField(hint_text="scale of changes", size_hint=(0.70, 0.1)),
        ]
        noise_widget = transform_items_constructor(
            [
                check_list[7],
                MDLabel(text="Noise", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[7])[0],
            ]
        )
        # change saturation
        self.checkboxes[check_list[8]] = [
            MDTextField(hint_text="scale of changes", size_hint=(0.70, 0.1)),
        ]
        saturation_widget = transform_items_constructor(
            [
                check_list[8],
                MDLabel(text="Saturation", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[8])[0],
            ]
        )
        # random cropping
        self.checkboxes[check_list[9]] = [
            MDTextField(hint_text="crop width", size_hint=(0.35, 0.1)),
            MDTextField(hint_text="crop height", size_hint=(0.35, 0.1)),
        ]
        crop_widget = transform_items_constructor(
            [
                check_list[9],
                MDLabel(text="Rand Crop", size_hint=(0.15, 0.1)),
                self.checkboxes.get(check_list[9])[0],
                self.checkboxes.get(check_list[9])[1],
            ],
            columns=4,
        )
        # Table of images and their's attributes
        self.image_table = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("№", dp(30)),
                ("Title", dp(120)),
                ("Resolution", dp(50)),
                ("Format", dp(30)),
                ("intact", dp(30)),
            ],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
            size_hint=(0.8, 1),
            pos_hint=(1, 1),
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
        self.input_button.text = "Choose input path"
        self.input_button.on_press = lambda: self.file_manager_opener(True)
        # Open path to output button
        self.output_button = MDRectangleFlatButton()
        self.output_button.padding = 20
        self.output_button.size_hint = (0.1, 0.05)
        self.output_button.text = "Choose output path"
        self.output_button.on_press = lambda: self.file_manager_opener(False)
        # Start transformations
        self.start_button = MDFloatingActionButton()
        self.start_button.icon = "send-variant-outline"
        self.start_button.size = (25, 25)
        self.start_button.font_size = 24
        self.start_button.text_color = "#FFFFFF"
        self.start_button.md_bg_color = "#000000"
        self.start_button.padding = 10
        self.start_button.pos_hint = {"x": 0.8, "y": 0.5}
        self.start_button.on_press = self.start_processing
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
        transform_layout.add_widget(crop_widget)
        main_window_layout.add_widget(self.image_table)
        main_window_layout.add_widget(transform_layout)
        transform_layout.add_widget(self.input_button)
        transform_layout.add_widget(self.output_button)
        transform_layout.add_widget(self.start_button)
        self.add_widget(main_window_layout)

    def open_dialog(self, *args):
        """
        calls an open dialog function inside of a main thread
        """
        self.start_button.disabled = False
        message_text = (
            "Image editing is finished. Images are saved at " + self.images_unload_path
        )
        return open_dialog_message(message_text)

    def open_error(self, *args):
        self.start_button.disabled = False
        open_dialog_error(
            'Error during image processing please check the input.')

    def on_checkbox_active(self, cb: MDCheckbox):
        """
            Changes checkbox state to "unchecked" at custom checkbox container
        Args:
            cb (MDCheckbox): choosen checbox at the data table
        """
        if cb.state == "normal":
            Clock.schedule_once(self.update_checks, 0)

    def on_check(self, instance, row_data):
        """
            Changes checkbox state to "checked" at custom checkbox container
        Args:
            cb (MDCheckbox): choosen checbox at the data table
        """
        Clock.schedule_once(self.update_checks, 0)

    def update_checks(self, _):
        """Upadates buffer in which all of the checked rows of datatables are stored"""
        self.my_selections = []
        table_data = self.image_table.table_data
        for page, selected_cells in table_data.current_selection_check.items():
            for column_index in selected_cells:
                data_index = int(
                    page * table_data.rows_num
                    + column_index / table_data.total_col_headings
                )
                self.my_selections.append(table_data.row_data[data_index][0])

    def calcute_to_do(self):
        """Collects all the needed functions and their's parameters

        Returns:
            list: returns list of pairs where first ia function and second is parameters
        """
        to_do_list = []
        all_functions = image_transformation.funct_list + image_posteffects.funct_list
        for func, key in zip(all_functions, self.checkboxes.keys()):
            if key.active:
                func_inputs = []
                for textfield in self.checkboxes.get(key):
                    if "]" in textfield.text:
                        func_inputs.append(
                            [
                                int(entry)
                                for entry in textfield.text.strip("]")
                                .strip("[")
                                .split(", ")
                            ]
                        )
                    else:
                        func_inputs.append(int(textfield.text))
                to_do_list.append([func, func_inputs])
        return to_do_list

    def process_images(self):
        """Processing images and saving them
        Raises:
            ValueError: raises when there is an error in any of the input fields
        """
        try:
            to_do_list = self.calcute_to_do()
            images = images_collecting.load_images(self.images_load_path)
            needed_images = []
            checked_names = [
                self.image_table.row_data[int(i)][1] for i in self.my_selections
            ]
            for image in images:
                for name in checked_names:
                    if name == image[1].split("\\")[-1]:
                        needed_images.append(image)
                        break
            result = []
            for image in needed_images:
                temp_image = image[0]
                for func in to_do_list:
                    temp_image = func[0](temp_image, *func[1])
                result.append([temp_image, image[1].split("\\")[-1]])
            images_collecting.save_images(result, PATH=self.images_unload_path)
            Clock.schedule_once(self.open_dialog)
        except:
            Clock.schedule_once()
            open_dialog_error(
                "Error while converting images. Check the entered data for correctness."
            )

    def start_processing(self):
        """Check upload and import paths and calls processing function thread. Also catches value errors"""
        if self.images_load_path and self.images_unload_path:
            try:
                self.start_button.disabled = True
                process = Thread(target=self.process_images)
                process.start()
            except:
                open_dialog_error(
                    "Error while converting images. Check the entered data for correctness."
                )
        else:
            open_dialog_error("You need to choose upload and import paths")

    def load_images(self, path: str):
        """loads data about images into a datatable
        Args:
            path (str): images import path
        """
        new_images = images_collecting.read_images_attributes(path)
        if new_images:
            self.image_table.row_data = new_images
        else:
            open_dialog_error("No images inside of the choosen dirrectory")

    def file_manager_opener(self, is_input: bool):
        """
            Opens file mangager
        Args:
            is_input (bool): shows which path is being chosen input path or output path
        """
        self.manager_open = True
        self.is_input = is_input
        path = os.path.expanduser("C:\\")
        self.file_manager.show(path)

    def select_path(self, path: str):
        """Saves chosen path into a buffer

        Args:
            path (str): Chosen path
        """
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
        """Keyboard events handler

        Args:
            keyboard (int): index of pressed key
        """
        if keyboard in (1001, 27) and self.manager_open:
            self.file_manager.back()
        elif keyboard == 27:
            quit()

    def exit_manager(self, *args):
        """Closes file manager"""
        self.manager_open = False
        self.file_manager.close()
