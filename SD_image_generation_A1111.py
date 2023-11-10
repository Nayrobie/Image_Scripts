"""
This script provides a simple GUI for users to choose between different image generation methods:
* Text to image: generate images with a prompt as input
* Image to image: generate images with a prompt and an image as input
* ControlNet: adds extra conditions to control the image generated, it allows users to give
an image as input in addition to the prompt. Users can choose between lineart, scribble, canny and depth models.

It allows users to quickly experiment with different generation methods and prompts without the need
to run the automatic1111 webui manually and it greatly reduces the amount of parameters needed.
"""

import io
import cv2
import base64
import requests
from PIL import Image
import json
import tkinter as tk
from tkinter import simpledialog

# User configurations
input_image_path = r"D:\GIT\house_gray.jpg"
user_choice = "txt2img"
prompt = "An old, weathered lighthouse standing tall on a desolate, rocky coastline"
negative_prompt = "low-quality, watermark, deformed, distorted anatomy, poor artistry, NSFW, Cleavage, Nudity, Naked, explicit content, mutated features, extra limbs, extra fingers, ugly, missing body parts, disconnected elements, malformed, abnormal proportions, aberrant hands, aberrant feet, aberrant  legs, aberrant  fingers"
model_checkpoint = "juggernautXL_version45.safetensors [ca4802bc3f]"
controlnet_module = [
    "lineart",
    #"scribble_pidinet",
    #"canny",
    #"depth_midas"
    ]
denoising_strengh = 0.3
styles = [
    "3D Rendering",
    #"Cinematic",
    #"Portrait",
    "Digital Drawing",
    #"Sketchbook",
    #"Manga",
    #"Indie Game",
    #"Craft Clay",
    "Isometric",
    "Low Poly",
    "Origami",
    #"Biomechanical",
    "Steampunk",
    #"Pirate Punk",
    "Neon Punk" 
]

# A1111 URL
url = "http://127.0.0.1:7860"

def encode_image_to_base64(input_path):
    """
    Encode an image from the specified local path to base64 so it can be sent to the API.
    """
    try:
        # Read the image from the specified path
        img = cv2.imread(input_path)

        if img is None:
            raise Exception("Unable to read the image from the provided path.")

        # Encode into PNG
        retval, bytes = cv2.imencode('.png', img)
        encoded_image = base64.b64encode(bytes).decode('utf-8')

        return encoded_image

    except Exception as e:
        return str(e)

# Create a tkinter window
root = tk.Tk()

# Function to set user choice
def set_user_choice(choice):
    global user_choice
    user_choice = choice
    root.destroy()

# Create buttons for user choice
controlnet_button = tk.Button(root, text="Controlnet", command=lambda: set_user_choice("3"))
img2img_button = tk.Button(root, text="Img2img", command=lambda: set_user_choice("2"))
txt2img_button = tk.Button(root, text="Txt2img", command=lambda: set_user_choice("1"))

# Pack buttons
controlnet_button.pack()
img2img_button.pack()
txt2img_button.pack()

# Wait for the user to click a button
root.mainloop()

def get_user_prompt():
    return simpledialog.askstring("User Prompt", "Enter your prompt:")

prompt = get_user_prompt()

def txt2img_controlnet(prompt, negative_prompt, model_checkpoint, controlnet_module):
    """
    Text to image generation using ControlNets 
    (a neural network structure to control diffusion models by adding extra conditions).
    """
    if controlnet_module not in controlnet_mapping:
        raise ValueError(f"Unsupported controlnet module: {controlnet_module}")

    controlnet_model = controlnet_mapping[controlnet_module]

    controlnet_payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "batch_size": 1,
        "steps": 30,
        "cfg_scale": 7,
        "save_images": True,
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "input_image": encoded_image,
                        "module": controlnet_module,
                        "model": controlnet_model,
                        "weight": 2,
                        "width": 512,
                        "height": 512,
                        "resize_mode": "Scale to Fit (Inner Fit)",
                        "control_mode": "Balanced",
                        "pixel_perfect": True
                    }
                ]
            }
        }
    }

    # For the script to override the model chosen on A1111    
    override_settings = {
        "sd_model_checkpoint": model_checkpoint
    }
    override_payload = {
        "override_settings": override_settings
    }
    controlnet_payload.update(override_payload)

    # Trigger Generation
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=controlnet_payload)
    r = response.json()
    print(f"Generated image for controlnet_module: {controlnet_module}")

def img2img(prompt, negative_prompt, model_checkpoint, input_img, denoising_strengh):
    """
    Running Stable Diffusion by providing both a prompt and an initial image. 
    The denoising strengh is the pourcentage of noise added to the initial image,
    a value of 1 will completely replace your input image with noise.
    """
    # Generation parameters
    img2img_payload = {
        "init_images": [input_img],
        "resize_mode": 0,
        "image_cfg_scale": 0,
        "mask_blur": 0,
        "save_images": True,

        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "denoising_strength": denoising_strengh,
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

    #result = r['images'][0]
    #image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))

def txt2img(prompt, negative_prompt, model_checkpoint, styles):
    txt2img_payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": -1,
        "width": 1024,
        "height": 1024,
        "sampler_name": "Euler a",
        "cfg_scale": 7.0, 
        "steps": 30, 
        "restore_faces": False, 
        "denoising_strength": 0, 
        "extra_generation_params": {},
        "styles": styles,
        "save_images": True
    }

    # For the script to override the model chosen on A1111    
    override_settings = {
        "sd_model_checkpoint": model_checkpoint
    }
    override_payload = {
        "override_settings": override_settings
    }
    txt2img_payload.update(override_payload)

    txt2img_response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=txt2img_payload)
    r = txt2img_response.json()

# Controlnet module-to-model mapping
controlnet_mapping = {
    "lineart": "control_v11p_sd15_lineart [43d4be0d]",
    "scribble_pidinet": "control_v11p_sd15_scribble [d4ba51ff]",
    "canny": "control_v11p_sd15_canny [d14c016b]",
    "depth_midas": "control_v11f1p_sd15_depth [cfd03158]",
    "openpose_full": "control_v11p_sd15_openpose [cab727d4]",
}

# Documentation:
# Controlnet API doc https://github.com/Mikubill/sd-webui-controlnet/wiki/API
# API get info http://127.0.0.1:7860/docs#/default

encoded_image = encode_image_to_base64(input_image_path)

# User's choice between the different payloads
if user_choice == "3":
    if isinstance(controlnet_module, list):
        # Generate images for each controlnet module
        for module in controlnet_module:
            txt2img_controlnet(prompt, negative_prompt, model_checkpoint, module)
    else:
        # Send the ControlNet request for a single module
        txt2img_controlnet(prompt, negative_prompt, model_checkpoint, controlnet_module)
elif user_choice == "2":
    # Send the img2img request
    img2img(prompt, negative_prompt, encoded_image)
elif user_choice == "1":
    # Generate images for each style in the 'styles' list
    for style in styles:
        txt2img(prompt, negative_prompt, model_checkpoint, [style])
else:
    print("Invalid user choice. Please specify '1', '2', or '3'.")