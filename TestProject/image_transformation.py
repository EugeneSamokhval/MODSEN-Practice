import cv2
import numpy as np


def resize(image: np.array, width: int, height: int):
    """Resizes an image

    Args:
        image (np.array): resizable image
        width (int): width of transformed image
        height (int): height of transformed image

    Returns:
        np.array: transformed image
    """
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)


def cutout(image, top_left: list, down_right: list):
    """Cut part of an image

    Args:
        image (np.array): editable image
        top_left (list): coordinates of top left point of the image
        down_right (list): coorditates of bottom right point of the image

    Returns:
        np.array: cut of an image
    """
    return image[top_left[0]: down_right[0], top_left[1]: down_right[1]]


def flip(image: np.array, is_horisontal: bool):
    """Flip image

    Args:
        image (np.array): editable image
        is_horisontal (bool): flip orientation

    Returns:
        np.array: flipped image
    """
    return cv2.flip(image, is_horisontal)


def rotate(image: np.array, center_of_rotation: int = None, angle: int = None):
    """Rotate image 

    Args:
        image (np.array): rotatable image
        center_of_rotation (int, optional): point which represents a center of rotation. Defaults to None.
        angle (int, optional): angle of rotation. Defaults to None.

    Returns:
        np.array: rotated image 
    """
    if not center_of_rotation:
        center_of_rotation = [i / 2 for i in image.shape[:2]]
    if not angle:
        angle = 90
    (width, height) = image.shape[:2]
    # the rotation matrix
    M = cv2.getRotationMatrix2D(
        (center_of_rotation[0], center_of_rotation[1]), angle, 1
    )

    return cv2.warpAffine(image, M, (width, height))


def shift(image: np.array, x_shift: int, y_shift: int):
    """Shift image

    Args:
        image (np.array): shiftable image
        x_shift (int): shift horisontal
        y_shift (int): shift vertical

    Returns:
        np.array: shifted image
    """
    M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted


# Functions positioning is needed to be with the same lineup as in self.switches variable of interface
funct_list = [resize, cutout, flip, rotate, shift]
