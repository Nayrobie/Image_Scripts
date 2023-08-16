import json
import requests
import io
import base64
import re
from PIL import Image
import os

url = "http://127.0.0.1:7860"

output_directory = "E:\\GIT_ROOT\\AC-EKO-IA\\AUTOMATIC1111\\outputs\\sd_api"
existing_images = [f for f in os.listdir(output_directory) if f.endswith(".jpg")]

highest_image_number = 0
for existing_image in existing_images:
    image_number = int(existing_image.split("_")[0])
    highest_image_number = max(highest_image_number, image_number)

# How to get model hash:
# go to http://127.0.0.1:7860/docs#/default/get_sd_models_sdapi_v1_sd_models_get
# and execute the code at: /sdapi/v1/sd-models 
# models = ["c249d7853b", "c0d1994c73", "4199bcdd14"]
# Dreamshaper, realisticVision, revAnimated

model_checkpoints = ["dreamshaper_6BakedVae.safetensors [c249d7853b]"]

for model_checkpoint in model_checkpoints:
    payload = {
        "prompt": "dragon",
        "negative_prompt": "purple",
        "steps": 10,
        "seed": 2845804966,
        # Doesn't work:
        # "sd_model_hash": "c249d7853b",
        # "model_name": "dreamshaper_6BakedVae",
        # "sd_model_checkpoint": "dreamshaper_6BakedVae.safetensors [c249d7853b]" 
    }
    override_settings = {
        "sd_model_checkpoint": model_checkpoint
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    print(r.get("info")) # Print all the generated image info
    info_json = json.loads(r.get("info"))  # Parse the "info" JSON string

    # Extract the infotexts value
    infotexts = info_json.get("infotexts")[0]  # Assuming there's only one infotext

    filename = re.sub(r'[:,\s]+', '_', infotexts)
    filename = filename.replace("__", "_")  # Replace double underscores with a single underscore

    # Increment the highest image number to get the next unique number
    highest_image_number += 1
    image_number = str(highest_image_number).zfill(3)

    filename = f"{image_number}_{filename}.jpg"

    # Select the first image from the images list
    image_data = base64.b64decode(r['images'][0].split(",", 1)[0])
    image = Image.open(io.BytesIO(image_data))

    # Update the output directory path with the generated filename
    output_path = os.path.join(output_directory, filename)
    image.save(output_path, format='JPEG', quality=95)