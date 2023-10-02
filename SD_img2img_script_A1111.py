import json
import requests
import io
import base64
import re
from PIL import Image
import os

url = "http://127.0.0.1:7860"

output_directory = "D:\GIT\stable-diffusion-webui\outputs\sd_api\img2img"
existing_images = [f for f in os.listdir(output_directory) if f.endswith(".jpg")]

info_txt = os.path.join(output_directory, "generated_info.txt")
highest_image_number = -1
for existing_image in existing_images:
    image_number = int(existing_image.split(".")[0].replace("image_", ""))
    highest_image_number = max(highest_image_number, image_number)

# API get info http://127.0.0.1:7860/docs#/default

# Function to encode an image as a data URI
def encode_image_as_data_uri(image_path):
    with open(image_path, 'rb') as f:
        image_uri = base64.b64encode(f.read()).decode('ascii')
    return str(image_uri)

prompt = "Portrait of a woman"
negative_prompt = ""
model_checkpoint = "dreamshaper_8.safetensors [879db523c3]"

def img2img(prompt,negative_prompt,input_img):
    # Generation parameters
    img2img_payload = {
        "init_images": [input_img],
        "resize_mode": 0,
        "image_cfg_scale": 0,
        "mask_blur": 0,
        "save_images": True,

        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "denoising_strength": 0.3,
        "width": 512,
        "height": 512,
        "cfg_scale": 7,
        "sampler_name": "Euler a",
        "steps": 20
    }

    # For the script to override the model chosen on A1111    
    override_settings = {
        "sd_model_checkpoint": model_checkpoint
    }
    override_payload = {
        "override_settings": override_settings
    }
    img2img_payload.update(override_payload)

    img2img_response = requests.post(url=f'{url}/sdapi/v1/img2img', json=img2img_payload)
    r = img2img_response.json()

input_image_path = "D:\GIT\stable-diffusion-webui\outputs\sd_api\img2img\image1.png"
input_img = encode_image_as_data_uri(input_image_path)
img2img(prompt, negative_prompt, input_img)