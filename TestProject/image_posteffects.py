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
    stddev = noise_scale
    noise = np.random.normal(mean, stddev, image.shape).astype(np.uint8)
    return cv2.add(image, noise)


def contrast(image: np.array, change_scale: int):
    """Changes brightness of an image

    Args:
        image (np.array): _description_
        change_scale (int): _description_

    Returns:
        np.array: image after processing
    """
    adjusted_image = cv2.convertScaleAbs(image, alpha=change_scale)
    return adjusted_image


# Functions positioning is needed to be with the same lineup as in self.switches variable of interface
funct_list = [brightness, contrast, noise, saturation]
