import albumentations
from image_posteffects import brightness, contrast, noise, saturation, random_crops
from image_transformation import resize, cutout, flip, rotate, shift
import numpy as np
import datetime


def apply_all_transformations(image: np.array, width: int, height: int,
                              top_left: list, down_right: list, is_horizontal: int,
                              center_of_rotation: list, angle: int, x_shift: int,
                              y_shift: int, change_scale_saturation: int,
                              change_scale_brightness: int, noise_scale: int,
                              change_scale_contrast: int, crop_width: int,
                              crop_height: int) -> np.array:
    """Apply all transformations one by one to the image

    Args:
        image (np.array): Original image
        width (int): Width for resizing
        height (int): Height for resizing
        top_left (list): Coordinates of top left point for cutout
        down_right (list): Coordinates of bottom right point for cutout
        is_horizontal (int): Flip orientation
        center_of_rotation (list): Center point for rotation
        angle (int): Angle for rotation
        x_shift (int): Horizontal shift value
        y_shift (int): Vertical shift value
        change_scale_saturation (int): Saturation change scale
        change_scale_brightness (int): Brightness change scale
        noise_scale (int): Noise scale
        change_scale_contrast (int): Contrast change scale
        crop_width (int): Width for random cropping
        crop_height (int): Height for random cropping

    Returns:
        np.array: Transformed image
    """

    # Apply cutout
    image = cutout(image, top_left, down_right)

    # Apply flipping
    image = flip(image, is_horizontal)

    # Apply rotation
    image = rotate(image, center_of_rotation, angle)

    # Apply shifting
    image = shift(image, x_shift, y_shift)

    # Apply saturation adjustment
    image = saturation(image, change_scale_saturation)

    # Apply brightness adjustment
    image = brightness(image, change_scale_brightness)

    # Apply noise addition
    image = noise(image, noise_scale)

    # Apply contrast enhancement
    image = contrast(image, change_scale_contrast)

    # Apply resizing
    image = resize(image, width, height)

    # Apply random cropping
    image = random_crops(image, crop_width, crop_height)

    return image


def main_comprehansion():
    transform = albumentations.Compose([
        albumentations.RandomBrightnessContrast(
            p=0.5),  # Adjust brightness and contrast
        albumentations.GaussNoise(p=0.3),  # Add Gaussian noise
        albumentations.HueSaturationValue(p=0.5),  # Adjust saturation
        albumentations.RandomCrop(width=100, height=100),  # Random cropping
        albumentations.Resize(width=256, height=256),  # Resize to a fixed size
        albumentations.Crop(0, 0, 100, 100),  # Cutout augmentation
        albumentations.HorizontalFlip(p=0.5),  # Random horizontal flipping
        albumentations.Rotate(limit=30, p=0.5),  # Random rotation
        albumentations.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=30, p=0.5)])

    for image_size in [200, 500, 1000, 2000]:
        image = np.random.randint(0, 255, size=(
            image_size, image_size, 3), dtype=np.uint8)
        before_my_operations = datetime.datetime.now()
        augmented_image_custom = apply_all_transformations(
            image=image,
            width=1000,
            height=1000,
            top_left=[0, 0],
            down_right=[100, 100],
            is_horizontal=1,
            center_of_rotation=None,
            angle=30,
            x_shift=10,
            y_shift=10,
            change_scale_saturation=5,
            change_scale_brightness=5,
            noise_scale=1,
            change_scale_contrast=1,
            crop_width=100,
            crop_height=100
        )
        my_operations_time = datetime.datetime.now().microsecond - \
            before_my_operations.microsecond
        before_albumentations_operations = datetime.datetime.now()
        augmented_image = transform(image=image)['image']
        albumentations_time = datetime.datetime.now().microsecond - \
            before_albumentations_operations.microsecond
        print('Size of an image:', image_size, 'X', image_size, '\n', 'My operations work time:',
              my_operations_time, '\n', 'Albumentations operations work time:', albumentations_time)
        if albumentations_time < my_operations_time:
            print('Albumentations faster')
        else:
            print('My operations are faster')


if __name__ == '__main__':
    main_comprehansion()
