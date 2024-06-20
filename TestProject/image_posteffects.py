import cv2
import numpy as np


def saturation(image, change_scale):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 1] = hsv_image[:, :, 1] * change_scale
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1], 0, 255)
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return bgr_image


def brightness(image, change_scale):
    brightness_matrix = np.ones(image.shape, dtype='uint8') * change_scale
    bright_image = cv2.add(image, brightness_matrix)
    return bright_image


def noise(image, noise_scale):
    mean = 0
    stddev = noise_scale
    noise = np.random.normal(mean, stddev, image.shape).astype(np.uint8)
    return cv2.add(image, noise)


def contrast(image, change_scale):
    adjusted_image = cv2.convertScaleAbs(image, alpha=change_scale)
    return adjusted_image


# Funtions postioning is needed to be with the same lineup as in self.switches variable of interface
funct_list = [brightness, contrast, noise, saturation]
