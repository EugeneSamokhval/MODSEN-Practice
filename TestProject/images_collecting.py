import os
import cv2
from PIL import Image


def get_images_by_dir(PATH: str):
    """Get path to every image in dirrectory

    Args:
        PATH (str): path to the directory containing images

    Returns:
        str: all the paths to images situeted in the 'PATH' dirrectory
    """
    file_paths = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            file_path = os.path.join(root, file)
            for expansion in [".jpg", ".png", ".jpeg", ".bmp"]:
                if expansion in file_path:
                    file_paths.append(file_path)
                    break
    return file_paths


def read_images_attributes(PATH: str):
    """Read all the needed data about images in the PATH dirrectory

    Args:
        PATH (str): path to the directory containing images

    Returns:
        list(Tuple): contains all the images data in the format suitable for MDDataTable
    """
    file_paths = get_images_by_dir(PATH)
    data_container = []
    counter = 0
    for path in file_paths:
        name = path.split("\\")[-1]
        try:
            with Image.open(path) as img:
                resolution = img.size
                img_format = img.format
                data_container.append(
                    (
                        str(counter),
                        name,
                        str(resolution[0]) + "X" + str(resolution[1]),
                        img_format,
                        "1",
                    )
                )
        except IOError:
            data_container.append(
                (str(counter), name, "Unknown", "Unknown", str(0)))
        counter += 1
    return data_container


def save_images(images_list: list, PATH: str):
    """saves all the cv2 images at the PATH directory

    Args:
        images_list (list): list containing pairs image_data-image_name
        PATH (str): path to the save directory
    """
    for image in images_list:
        cv2.imwrite(PATH + "\\" + image[1], image[0])


def load_images(PATH: str):
    """Loads images from the PATH directory in cv2 image format

    Args:
        PATH (str):  path to the load directory

    Returns:
        list: Contains all of the loaded images with their path
    """
    file_paths = get_images_by_dir(PATH)
    images_container = [
        [cv2.imread(img_path, cv2.IMREAD_ANYCOLOR), img_path] for img_path in file_paths
    ]
    return [image for image in images_container if image]


def load_exact_image(PATH: str):
    """Loads exact image in cv2 format

    Args:
        PATH (str): full path to an image
    Returns:
        image in cv2 format
    """
    return cv2.imread(PATH)
