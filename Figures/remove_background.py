from PIL import Image
import numpy as np
import os

def remove_background_with_text_preservation(image):
    # Convert the image to RGBA mode if not already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Get the image data as a numpy array
    img_data = np.array(image)

    # Define the RGB values for the white background
    white_color = [255, 255, 255]

    # Create a mask to identify white pixels
    mask = np.all(img_data[:, :, :3] == white_color, axis=-1)


    # Apply the mask to the image data
    result_data = img_data.copy()
    result_data[mask] = [0, 0, 0, 0]  # Set RGBA values to transparent for masked pixels

    # Create a new PIL Image from the result data
    result_image = Image.fromarray(result_data)

    return result_image



print('RAN')
images_to_clear = ['besoins.png', 'caractéristiques.png', 'fonctions.png']

for image_path in images_to_clear:
    print(image_path)
    with Image.open('Figures/' + image_path) as img:
        result = remove_background_with_text_preservation(img)
        result.save('Figures/' +f"processed_{image_path}")
