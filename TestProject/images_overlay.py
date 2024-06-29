import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


def overlay_images(image_1: np.array, image_2: np.array, x: int, y: int):
    """
    Overlay image_2 onto image_1 at position (x, y).

    Args:
        image_1: The base image.
        image_2: The image to overlay.
        x (int): The x-coordinate for the top-left corner of the overlay.
        y (int): The y-coordinate for the top-left corner of the overlay.

    Returns:
        The resulting image after overlaying image_2 onto image_1.
    """
    height, width, _ = image_2.shape
    image_1[y:y+height, x:x+width] = image_2
    return image_1


def text_to_image(text: str, font_path: str, font_size: int, color=(0, 0, 0)):
    """
    Generate an image of the given text.

    Args:
        text (str): The text to render.
        font_path (str): The path to the .ttf font file.
        font_size (int): The size of the font.
        color (tuple): The color of the text in RGB format.

    Returns:
        open_cv_image: An Image object with the rendered text.
    """
    font = ImageFont.truetype(font_path, font_size)

    text_width = font.getlength(text)
    text_height = font_size
    image = Image.new('RGBA', (int(text_width), text_height), (0, 0, 0, 0))

    draw = ImageDraw.Draw(image)

    draw.text((0, 0), text, font=font, fill=color)
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image


def load_fonts() -> list:
    """
    Load fonts from 'fonts' directory

    Returns:
        list: list of paths to font files
    """
    file_paths = []
    for root, dirs, files in os.walk('fonts'):
        for file in files:
            file_path = os.path.join(root, file)
            if '.ttf' in file_path:
                file_paths.append(file_path)
                break
    return file_paths


def load_fonts_names() -> list:
    """
        Return the list of font inside of a 'fonts' dirrectory
    Returns:
        list: Returns list of fonts names
    """
    paths_list = load_fonts()
    names_list = []
    for path in paths_list:
        path: str
        font_name = path.split('\\')[-1].removesuffix('.ttf')
        font_name = font_name.split('-')[0]
        names_list.append(font_name)
    return names_list
