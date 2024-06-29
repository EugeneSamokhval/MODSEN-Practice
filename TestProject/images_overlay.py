import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


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
    h, w, _ = image_2.shape
    image_1[y:y+h, x:x+w] = image_2
    return image_1


def text_to_image(text, font_path, font_size, color=(255, 255, 255)):
    """
    Generate an image of the given text.

    Args:
        text (str): The text to render.
        font_path (str): The path to the .ttf font file.
        font_size (int): The size of the font.
        color (tuple): The color of the text in RGB format.

    Returns:
        img: An Image object with the rendered text.
    """
    font = ImageFont.truetype(font_path, font_size)

    text_width, text_height = font.getsize(text)

    img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    draw.text((0, 0), text, font=font, fill=color)

    return img
