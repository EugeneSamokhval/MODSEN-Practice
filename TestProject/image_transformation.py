import cv2
import numpy as np


def resize(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)


def cutout(image, top_left: list, down_right: list):
    return image[top_left[0]: down_right[0], top_left[1]: down_right[1]]


def flip(image, is_horisontal):
    return cv2.flip(image, is_horisontal)


def rotate(image, center_of_rotation=None, angle=None):
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


def tilt(image, angle=None):
    if not angle:
        angle = 90
    (h, w) = image.shape[:2]

    center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    tilted = cv2.warpAffine(image, M, (w, h))
    return tilted


def shift(image, x_shift, y_shift):
    M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted


image = cv2.imread('TestProject\\test_art.png', cv2.IMREAD_ANYCOLOR)
if image is None:
    print(f"Failed to load image")
else:
    new_img = tilt(image, 50)
    cv2.imshow('Edited Image', new_img)
    cv2.waitKey(0)


fuct_list = (resize, cutout, flip, rotate)
