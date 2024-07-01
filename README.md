# MODSEN-Practice

My applications written during my practice at MODSEN

# Image Augmentation

## Overview

Image Augmentation is a Python-based application that allows users to choose a directory with images and apply various transformations to them. The app supports transformations such as resizing, reflecting, rotating, changing saturation, brightness, contrast, and adding noise. Additionally, users can generate images using prompts.You can also use the image overlay function. As well as the function of superimposing text on an image. Unit tests are covering all of the image augmentation functions.

## Features

- Resize images
- Reflect images
- Rotate images
- Random crops
- Adjust saturation, brightness, and contrast
- Add noise to images
- Generate images based on user prompts
- Overlay image with image
- Overlay text with image

## Installation

To get started with Image Augmentation, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/EugeneSamokhval/MODSEN-Practice.git
   cd MODSEN-Practice/TestProject
   ```
2. Install the required dependencies:

```
    pip install kivymd opencv-python numpy requests pillow
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
pillow

## Example

### Transform Images

1. Launch the application by running python main.py.
2. Select a directory containing the images you want to transform.
3. Choose from the available transformations (resize, reflect, rotate, change saturation, brightness, contrast, add noise) using the transformations checklist.
4. Click the "Launch" button located below the transformations checklist.
5. Wait for a pop-up message indicating that the images were successfully transformed.
6. Find the transformed images in the specified save directory.

### Generate Images

1. Launch the application by running python main.py.
2. Select the "Generate" tab at the bottom right of the screen.
3. Enter your prompt in the prompt text field.
4. Specify the dimensions of the image you want to generate.
5. Choose a save directory for the generated image.
6. Press the "Send" button.
7. Wait for a pop-up message indicating that the image was successfully generated and saved in the chosen directory.

## Overlay an Image on an Image

1. Launch the application by running python main.py.
2. Select the "Overlay" tab at the bottom right of the screen.
3. Select the checkbox next to the label "Image overlay."
4. Choose an image to overlay on the target image.
5. Enter x and y coordinates in the respective text fields.
6. If you want to edit all images from the load directory, activate the checkbox next to the label "Save changes for all images."
7. Choose the input directory by pressing the "Choose input path" button.
8. Choose the output directory by pressing the "Choose output path" button.
9. To select a specific image from the input directory, navigate between images by pressing the arrow buttons under the image.
10. To start processing, press the "Send" button.
11. Wait for a pop-up message indicating that the images were successfully edited.
12. Find the transformed images in the specified save directory.

## Overlay Text on an Image

1. Launch the application by running python main.py.
2. Select the "Overlay" tab at the bottom right of the screen.
3. Select the checkbox next to the label "Text overlay."
4. Choose the input directory by pressing the "Choose input path" button.
5. Choose the output directory by pressing the "Choose output path" button.
6. Enter the x, y coordinates and font size in the respective fields next to the label "Text overlay."
7. Choose a font color using the color picker accessed by pressing the palette button.
8. Select a font by pressing the "Choose font" button.
9. To select a specific image from the input directory, navigate between images by pressing the arrow buttons under the image.
10. Enter your text in the "Text for overlay" text field.
11. To start processing, press the "Send" button.
12. Wait for a pop-up message indicating that the images were successfully edited.
13. Find the transformed images in the specified save directory.

## Custom fonts

To add custom fonts, unpack your fonts into 'TestProject/fonts'. Ensure you read the fonts' licenses before using them in your projects.

## To Do

1. Add random transformations from albumentations library.
2. Add real-time overlay displaying.
3. Increase test coverage.
4. Improve quality of documentation.

## Contributing

If you find bugs, leave information about them in the issues section on GitHub.
You can also send suggestions for improving the project there.

## Team

Samokhval Eugene - python developer

## Sources

[KivyMD documentation](https://kivymd.readthedocs.io/en/1.1.1/)
[OpenCV documentation](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
[FusionBrain api documentation](https://fusionbrain.ai/docs/)
[Pillow documentation](https://pillow.readthedocs.io/en/stable/)
