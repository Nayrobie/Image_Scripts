"""
The utility of this script is to visualise the effect of blending different keywords when prompting.
It generates a matrix formed by blending X and Y options, and each combination of X and Y generates a prompt
Then the images are saved along with their information in a specified output directory.
"""

import json
import requests
import io
import base64
import re
from PIL import Image
import os

# A1111 API URL
url = "http://127.0.0.1:7860"

# Output directory for saving generated images
output_directory = "D:\\GIT\\stable-diffusion-webui\\outputs\\sd_api\\mix_animals_prompt"

# List existing images in the output directory
existing_images = [f for f in os.listdir(output_directory) if f.endswith(".jpg")]

# Info text file to store information about generated images
info_txt = os.path.join(output_directory, "generated_info.txt")

# Find the highest image number to continue numbering from there
highest_image_number = -1
for existing_image in existing_images:
    image_number = int(existing_image.split(".")[0].replace("image_", ""))
    highest_image_number = max(highest_image_number, image_number)

# Define X and Y options for the matrix
x_options = ["cat", "axolotl", "horse", "elephant"]
y_options = ["giraffe", "octopus", "dolphin", "chameleon"]

# Generate prompts for all combinations of X and Y options
prompts = []
for x in x_options:
    for y in y_options:
        # Construct the prompt dynamically
        prompt = f"Realistic photography of a ({x}:0.5) ({y}:0.5)"
        prompts.append(prompt)

# Model checkpoints to use for image generation
model_checkpoints = [
    "rundiffusionXL_beta.safetensors [f3efadbbaf]"
]

# Iterate over model checkpoints and prompts to generate images
for m in model_checkpoints:
    for p in prompts:
        # Default generation parameters
        txt2img_payload = {
            "prompt": p,
            "negative_prompt": "",
            "seed": -1,
            "width": 1024,
            "height": 1024,
            "sampler_name": "Euler a",
            "cfg_scale": 7.0,
            "steps": 50,
            "restore_faces": False,
            "denoising_strength": 0,
            "extra_generation_params": {},
            "styles": [],
            "save_images": True
        }

        # For the script to override the model chosen on A1111
        override_settings = {
            "sd_model_checkpoint": m
        }
        override_payload = {
            "override_settings": override_settings
        }
        txt2img_payload.update(override_payload)

        # Send the txt2img request to the A1111 API
        txt2img_response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=txt2img_payload)
        r = txt2img_response.json()

        # Print all the generated image info
        print(r.get("info"))
        info_json = json.loads(r.get("info"))

        # Extract the infotexts value
        infotexts = info_json.get("infotexts")[0]
        filename = re.sub(r'[:,\s]+', '_', infotexts)
        filename = filename.replace("__", "_")

        # Increment the highest image number to get the next unique number
        highest_image_number += 1
        image_number = str(highest_image_number).zfill(4)

        filename = f"image_{image_number}.jpg"

        # Select the first image from the images list
        image_data = base64.b64decode(r['images'][0].split(",", 1)[0])
        image = Image.open(io.BytesIO(image_data))

        # Update the output directory path with the generated filename
        output_path = os.path.join(output_directory, filename)
        image.save(output_path, format='JPEG', quality=95)

        # Append the image information to the combined info text file
        with open(info_txt, "a") as info_file:
            info_file.write(f"image_{image_number}\n")
            info_file.write(f"{infotexts}\n\n")

        print(infotexts)