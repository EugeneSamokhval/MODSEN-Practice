import unittest
import images_collecting
import os
import cv2
import numpy as np


def is_test_image_here(input_list: list, searchable_entry: list) -> bool:
    """Function which returns true if file name and image is inside of one of the list's entries

    Args:
        input_list (list): list of ists(place to search)
        file_name (list): what we trying to find

    Returns:
        bool: _description_
    """
    for entry in input_list:
        if entry[1] == searchable_entry[1]:
            if np.array_equal(entry[0], searchable_entry[0]):
                return True
    return False


class TestImageCollecting(unittest.TestCase):
    def test_get_images_by_dir(self):
        """Test cases for funtion which finds images paths
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        cv2.imwrite('test.png', image)
        images_paths = images_collecting.get_images_by_dir(os.path.curdir)
        self.assertEqual(
            images_paths[0].split('\\')[-1], './test.png', 'Can\'t find image inside of a dirrectory')
        os.remove('test.png')

    def test_read_images_attributes(self):
        """Test cases for function which finds images data
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        cv2.imwrite('test.png', image)
        images_data = images_collecting.read_images_attributes(os.path.curdir)
        is_the_same_type = True
        if type(images_data[0]) != tuple:
            is_the_same_type = False
        for entry in range(len(images_data[0])):
            if type(images_data[0][entry]):
                is_the_same_type = False
        self.assertTrue(is_the_same_type,
                        'Can\'t get data correctly from an image')
        os.remove('test.png')

    def test_save_iamges(self):
        """Test cases for funtion which saves list of images
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        images_collecting.save_images([(image, 'test.png')], os.path.curdir)
        self.assertTrue(open('test.png', 'r'), 'Image wasn\'t saved correctly')
        os.remove('test.png')

    def test_load_images(self):
        """Test cases for function which loads list of lists with images and their names
        """
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        cv2.imwrite('test.png', image)
        im_data = images_collecting.load_images(os.path.curdir)
        im_data_to_compare = [image, './test.png']
        self.assertTrue(is_test_image_here(im_data, im_data_to_compare),
                        "Function wasn't able to find needed data")
        os.remove('test.png')


if __name__ == "__main__":
    unittest.main()
