import json
import requests
import io
import base64
import re
from PIL import Image
import os
import json

# Load the configuration from the JSON file
with open('config.json') as config_file:
    config = json.load(config_file)
# Access the input_image_path from the configuration
output_directory_path = config["output_directory_path"]

url = "http://127.0.0.1:7860"

existing_images = [f for f in os.listdir(output_directory_path) if f.endswith(".jpg")]

info_txt = os.path.join(output_directory_path, "generated_info.txt")

highest_image_number = -1
for existing_image in existing_images:
    image_number = int(existing_image.split(".")[0].replace("image_", ""))
    highest_image_number = max(highest_image_number, image_number)

# API get info http://127.0.0.1:7860/docs#/default

# Define X and Y of the matrix
x_options = ["cat", "axolotl", "horse", "elephant"]
y_options = ["giraffe", "octopus", "dolphin", "chameleon"]

prompts = []
for x in x_options:
    for y in y_options:
        # Construct the prompt dynamically
        prompt = f"Realistic photography of a ({x}:0.5) ({y}:0.5)"
        prompts.append(prompt)

model_checkpoints = [
    "rundiffusionXL_beta.safetensors [f3efadbbaf]"
    ]

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