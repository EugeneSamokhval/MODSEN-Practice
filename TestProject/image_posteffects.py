import cv2
import numpy as np


def saturation(image: np.array, change_scale: int):
    """Changes saturation of an image

    Args:
        image (np.array): numpy array containing image data
        change_scale (int): saturation change scale

    Returns:
        np.array: image after processing
    """
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 1] = hsv_image[:, :, 1] * change_scale
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1], 0, 255)
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return bgr_image


def brightness(image: np.array, change_scale: int):
    """Changes brightness of an image

    Args:
        image ( np.array): numpy array containing image data
        change_scale (int): brightness change scale

    Returns:
        np.array: image after processing
    """
    brightness_matrix = np.ones(image.shape, dtype="uint8") * change_scale
    bright_image = cv2.add(image, brightness_matrix)
    return bright_image


def noise(image: np.array, noise_scale: int):
    """Adds noise to the image

    Args:
        image (np.array): numpy array containing image data
        noise_scale (int): brightness change scale

    Returns:
        np.array: image after adding a noise
    """
    mean = 0
    noise = np.random.normal(mean, noise_scale, image.shape).astype(np.uint8)
    return cv2.add(image, noise)


def contrast(image: np.array, change_scale: int):
    """Changes brightness of an image

    Args:
        image (np.array): numpy array containing image data
        change_scale (int): how much image contrast will change

    Returns:
        np.array: image after processing
    """
    adjusted_image = cv2.convertScaleAbs(image, alpha=1+(change_scale/256))
    return adjusted_image


def random_crops(image: np.array, crop_width: int, crop_height: int):
    """Cut random part of image out of it

    Args:
        image (np.array): cropable
        crop_width (int): width of resulting image
        crop_height (int): height of resulting image

    Returns:
        np.arrray: cropped image
    """
    image_height, image_width = image.shape[:2]
    start_x = np.random.randint(0, image_width - crop_width)
    start_y = np.random.randint(0, image_height - crop_height)
    cropped_image = image[
        start_y: start_y + crop_height, start_x: start_x + crop_width
    ]
    return cropped_image


# Functions positioning is needed to be with the same lineup as in self.switches variable of interface
funct_list = [brightness, contrast, noise, saturation, random_crops]
