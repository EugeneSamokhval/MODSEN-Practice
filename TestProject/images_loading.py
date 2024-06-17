import os
import cv2


def load_images(PATH):
    file_paths = []

    for root, dirs, files in os.walk(PATH):
        for file in files:
            file_path = os.path.join(root, file)
            for expansion in ['.jpg', '.png', '.jpeg', '.bmp', '.gif']:
                if expansion in file_path:
                    file_paths.append(file_path)
                    break
    images_container = [cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
                        for img_path in file_paths]
    return images_container
