# MODSEN-Practice

My applications written during my practice at MODSEN

# Image Augmentation

## Overview

Image Augmentation is a Python-based application that allows users to choose a directory with images and apply various transformations to them. The app supports transformations such as resizing, reflecting, rotating, changing saturation, brightness, contrast, and adding noise. Additionally, users can generate images using prompts. Unit tests are covering all of the image augmentation functions.

## Features

- Resize images
- Reflect images
- Rotate images
- Random crops
- Adjust saturation, brightness, and contrast
- Add noise to images
- Generate images based on user prompts

## Installation

To get started with Image Augmentation, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/EugeneSamokhval/MODSEN-Practice.git
   cd MODSEN-Practice/TestProject
   ```
2. Install the required dependencies:

```
    pip install kivymd opencv-python numpy requests
```

## Usage

To launch the application, simply run:

```
python main.py
```

## Tests

To check tests coverage run:
'''
python tests_main.py
'''

## Dependencies

KivyMD
OpenCV (cv2)
NumPy
Requests

## Example

### Transform Images

1. Launch the application by running `python main.py`.
2. Select a directory containing the images you want to transform.
3. Choose from the available transformations (resize, reflect, rotate, change saturation, brightness, contrast, add noise) using the transformations checklist.
4. Click the "Launch" button located below the transformations checklist.
5. Wait for a pop-up message indicating that the images were successfully transformed.
6. You can find the transformed images in the specified save directory.

### Generate Images

1. Launch the application by running `python main.py`.
2. Select the "Generate" tab at the bottom right of the screen.
3. Enter your prompt in the prompt text field.
4. Specify the dimensions of the image you want to generate.
5. Choose a save directory for the generated image.
6. Wait for a pop-up message indicating that the image was successfully generated and saved in the chosen directory.

## Contributing

If you find bugs, leave information about them in issues on Github.
You can also send suggestions for improving the project there.

## Team

Samokhval Eugene - python developer

## Sources

[KivyMD documentation](https://kivymd.readthedocs.io/en/1.1.1/)
[OpenCV documentation](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
[FusionBrain api documentation](https://fusionbrain.ai/docs/)
