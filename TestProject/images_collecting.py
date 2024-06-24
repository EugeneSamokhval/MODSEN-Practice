import os
import cv2
from PIL import Image


def get_images_by_dir(PATH):
    file_paths = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            file_path = os.path.join(root, file)
            for expansion in [".jpg", ".png", ".jpeg", ".bmp"]:
                if expansion in file_path:
                    file_paths.append(file_path)
                    break
    return file_paths


def read_images_attributes(PATH):
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
            data_container.append((str(counter), name, "Unknown", "Unknown", str(0)))
        counter += 1
    return data_container


def save_images(images_list: list, PATH: str):
    for image in images_list:
        cv2.imwrite(PATH + "\\" + image[1], image[0])


def load_images(PATH):
    file_paths = get_images_by_dir(PATH)
    images_container = [
        [cv2.imread(img_path, cv2.IMREAD_ANYCOLOR), img_path] for img_path in file_paths
    ]
    return [image for image in images_container if image]
