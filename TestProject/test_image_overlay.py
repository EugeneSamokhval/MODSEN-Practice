import unittest
import images_overlay
import numpy as np


class TestImageOverlay(unittest.TestCase):
    def check_image_overlay(self):
        """Image overlay test.
        Check input type.
        """
        image_1 = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        image_2 = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
        result = images_overlay.overlay_images(image_1, image_2, 10, 10, 1)
        self.assertEqual(type(result), np.array)

    def check_text_overlay(self):
        """Text overlay test.
        Check input type.
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        result = images_overlay.overlay_text(
            image, 1, 10, 'Hello world', font_path='./fonts/new-standard-font-collection/ageo-32909/AgeoTrialBold-3zPA3.ttf')
        self.assertEqual(type(result), np.array)

    def check_load_fonts(self):
        """Fonts loading test.
        Check input type.
        """
        try:
            font_list = images_overlay.load_fonts()
            self.assertEqual(type(font_list), list)
        except:
            self.assertTrue(False, "Error during finding fonts")

    def check_load_font_names(self):
        """Font names loading test.
        Check input type.
        """
        try:
            names_list = images_overlay.load_fonts_names()
            self.assertEqual(type(names_list), list)
        except:
            self.assertTrue(False, 'Error during finding fonts')


if __name__ == "__main__":
    unittest.main()
