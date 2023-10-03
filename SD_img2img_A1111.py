import json
import requests
import io
import base64
import re
from PIL import Image
import os

url = "http://127.0.0.1:7860"

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

input_image_path = r"C:\Users\svc_ac-eko-ia\Downloads\image1.png"
input_img = encode_image_as_data_uri(input_image_path)
img2img(prompt, negative_prompt, input_img)