import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os


def overlay_images(image_1: np.array, image_2: np.array, x: int, y: int, alpha: int = 1):
    """
    Overlay image_2 onto image_1 at position (x, y).

    Args:
        image_1: The base image.
        image_2: The image to overlay.
        x (int): The x-coordinate for the top-left corner of the overlay.
        y (int): The y-coordinate for the top-left corner of the overlay.
        alpha (int): Overlay image transparancy

    Returns:
        The resulting image after overlaying image_2 onto image_1.
    """
    size_container = image_1.shape
    # Convert the images to PIL Image objects
    image_1 = Image.fromarray(image_1)
    image_2 = Image.fromarray(image_2)

    # Ensure both images have an alpha channel
    image_1 = image_1.convert("RGBA")
    image_2 = image_2.convert("RGBA")

    overlay_with_transparency = image_2.copy()
    overlay_with_transparency.putalpha(int(255 * alpha))

    empty_image = Image.new(
        'RGBA', (size_container[0], size_container[1]))
    empty_image.paste(image_1, (0, 0))
    empty_image.paste(overlay_with_transparency,
                      (x, y), overlay_with_transparency)

    return np.array(empty_image)


def overlay_text(image: np.array, x: int, y: int, text: str, font_path: str, font_size: int, color=(0, 0, 0, 255)):
    """Draws text over the input image

    Args:
        image (np.array): background image
        x (int): x position of starting point for writing text
        y (int): y position of starting point for writing text
        text (str): text to draw
        font_path (str): path to font for text overlay
        font_size (int): size of output text
        color (tuple, optional): Color of output text. Defaults to (0, 0, 0, 255).

    Returns:
        np.array: output image
    """

    font = ImageFont.truetype(font_path, font_size)
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    draw.multiline_text((x, y), text, color, font=font)
    open_cv_image = np.array(image)
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
