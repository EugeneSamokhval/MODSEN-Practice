import image_posteffects
import numpy as np
import unittest
import cv2


def is_image_inside(image, template, threshold=0.8):
    """
    Checks if the template image is inside the base image.

    Args:
        image (str): base image.
        template_path (str): template image.
        threshold (float, optional): Matching threshold (default is 0.8).

    Returns:
        bool: True if the template is inside the base, False otherwise.
    """
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    return len(loc[0]) > 0


class TestImagePosteffects(unittest.TestCase):
    def basic_test(self, test_image, modified_image):
        """Basics test to check if the image is edited and if it has same dimension as before
        Args:
            test_image (np.array): image before processing.
            modified_image (np.array): image after processing.
        """
        self.assertEqual(True, np.array_equal(
            modified_image.shape, test_image.shape), "Wrong image shape")
        self.assertNotEqual(True, np.array_equal(
            modified_image, test_image), "Image didn't changed")

    def test_saturation(self):
        """Tests for saturation change
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        for sat_factor in range(1, 100, 10):
            modified_image = image_posteffects.saturation(image, sat_factor)
            self.basic_test(image, modified_image)

    def test_brightness(self):
        """Tests for brightness change
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        for brightness_factor in range(1, 100, 10):
            modified_image = image_posteffects.brightness(
                image, brightness_factor)
            self.basic_test(image, modified_image)

    def test_noise(self):
        """Tests for function which adds noise"""
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        for noise_scale in [1, 2, 3]:
            modified_image = image_posteffects.noise(
                image, noise_scale
            )
            self.basic_test(image, modified_image)

    def test_contrast(self):
        """Tests for function which changes contrast"""
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        for contrast_factor in range(1, 100, 10):
            modified_image = image_posteffects.contrast(image, contrast_factor)
            self.basic_test(image, modified_image)

    def test_rand_crops(self):
        """Test for random croping
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        rand_crop = image_posteffects.random_crops(image, 25, 25)
        self.assertTrue(is_image_inside(image, rand_crop),
                        "Crop doesn't belong to the image")
        self.assertEqual(rand_crop.shape, (25, 25, 3),
                         "Crop's shape doesn't match input shape input")


if __name__ == "__main__":
    unittest.main()
