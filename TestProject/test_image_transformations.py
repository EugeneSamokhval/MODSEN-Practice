import unittest
import numpy as np
import image_transformation
import test_image_posteffects


class TestImageTransformations(unittest.TestCase):
    def test_resize(self):
        """Test cases for image resizing
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        scale = 1000
        resized_image = image_transformation.resize(image, scale, scale)
        self.assertTrue(np.array_equal(
            resized_image.shape, (scale, scale, 3)), "Resized image doesn't have requested size")
        self.assertFalse(np.array_equal(resized_image, image),
                         "Image didn't changed after resizing")

    def test_cut(self):
        """Test cases for image cut
        """
        image = np.random.randint(0, 256, (250, 250, 3), dtype=np.uint8)
        scale = 100
        image_cut = image_transformation.cutout(image, [0, 0], [scale, scale])
        self.assertTrue(np.array_equal(
            image_cut.shape, (scale, scale, 3)), 'Image cut has wrong shape')
        self.assertTrue(
            test_image_posteffects.is_image_inside(image, image_cut), 'Image cut can\'t be find inside of the image')
        self.assertFalse(np.array_equal(image_cut, image),
                         "Image didn't changed after cutting")

    def test_flip(self):
        """Test cases for image flippings
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        flipped_image_h = image_transformation.flip(image, 1)
        flipped_image_v = image_transformation.flip(image, 1)
        vals_image = set(image.mean(axis=2).flatten())
        vals_flipped_h = set(flipped_image_h.mean(axis=2).flatten())
        vals_flipped_v = set(flipped_image_v.mean(axis=2).flatten())
        self.assertTrue(np.array_equal(vals_image, vals_flipped_h),
                        'Image colors changed. But they shouldn\'t.')
        self.assertTrue(np.array_equal(vals_image, vals_flipped_v),
                        'Image colors changed. But they shouldn\'t.')
        self.assertTrue(np.array_equal(
            flipped_image_v.shape, image.shape), "Flipped image\'s shape should be equal with shape of original image")
        self.assertTrue(np.array_equal(
            flipped_image_h.shape, image.shape), "Flipped image\'s shape should be equal with shape of original image")
        self.assertFalse(np.array_equal(flipped_image_v, image),
                         "Image didn't changed after flipping")
        self.assertFalse(np.array_equal(flipped_image_h, image),
                         "Image didn't changed after flipping")

    def test_rotate(self):
        """Test cases for image rotations
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        rotated = image_transformation.rotate(image, angle=90)
        self.assertEqual(True, np.array_equal(
            rotated.shape, image.shape), 'Image rotation has wrong shape')
        rotated_full = image_transformation.rotate(image, angle=360)
        self.assertTrue(np.array_equal(image, rotated_full),
                        'Image changed after 360 degrees rotation, but it sholdn\'t')
        self.assertFalse(np.array_equal(rotated, image),
                         "Image didn't changed after shifting")

    def test_shift(self):
        """Test cases for image shifting
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        shifted_image = image_transformation.shift(image, 50, 50)
        self.assertTrue(np.array_equal(
            shifted_image.shape, image.shape), "Shifted image\'s shape should be equal with shape of original image")
        self.assertFalse(np.array_equal(shifted_image, image),
                         "Image didn't changed after shifting")


if __name__ == "__main__":
    unittest.main()
