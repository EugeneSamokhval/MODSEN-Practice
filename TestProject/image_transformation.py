import cv2
import numpy as np


def resize(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)


def cutout(image, top_left: list, down_right: list):
    return image[top_left[0] : down_right[0], top_left[1] : down_right[1]]


def flip(image, is_horisontal):
    return cv2.flip(image, is_horisontal)


def rotate(image, center_of_rotation=None, angle=None):
    if not center_of_rotation:
        center_of_rotation = [i / 2 for i in image.shape[:2]]
    (width, height) = image.shape[:2]
    # the rotation matrix
    M = cv2.getRotationMatrix2D(
        (center_of_rotation[0], center_of_rotation[1]), angle, 1
    )

    return cv2.warpAffine(image, M, (width, height))


image = cv2.imread("test_art.png", cv2.IMREAD_ANYCOLOR)
image = rotate(image, angle=90)

cv2.imshow("test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
