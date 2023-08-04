import re # a regex pattern to remove all non-alphanumeric characters and multiple spaces
from PIL import Image
import os

# Define the path to the image folder
image_folder = r"E:\GIT_ROOT\AC-EKO-IA\AUTOMATIC1111\outputs\txt2img-images\2023-07-25"

for filename in os.listdir(image_folder):
    if filename.endswith(".jpg"):
        # Get the full path to the image
        image_path = os.path.join(image_folder, filename)

        # Open the image using Pillow
        image = Image.open(image_path)

        # Extract the text info from the image's metadata
        image_info = None
        if hasattr(image, '_getexif'):
            exif_data = image._getexif()
            if exif_data is not None:
                # Search for a custom comment tag (you may need to adjust the tag value)
                for tag, value in exif_data.items():
                    if tag == 37510:  # Custom comment tag (adjust as needed)
                        image_info = value.strip().decode("utf-8")
                        break

        print(f"Image File: {filename}")

        # Process and print the text info
        if image_info:
            formatted_info = re.sub(r'[^\w\s]+', '', image_info)
            formatted_info = re.sub(r'\s+', ' ', formatted_info).strip()
            # Remove "UNICODE" from the beginning of the image info
            formatted_info = formatted_info.replace("UNICODE", "").strip()
            print(f"Image Info: {formatted_info}")

        print("======================================")
