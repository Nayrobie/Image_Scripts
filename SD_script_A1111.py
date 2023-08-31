import json
import requests
import io
import base64
import re
from PIL import Image
import os

url = "http://127.0.0.1:7860"

output_directory = "D:\GIT\stable-diffusion-webui\outputs\sd_api\models_and_prompt"
existing_images = [f for f in os.listdir(output_directory) if f.endswith(".jpg")]

info_txt = os.path.join(output_directory, "generated_info.txt")

highest_image_number = -1
for existing_image in existing_images:
    image_number = int(existing_image.split(".")[0].replace("image_", ""))
    highest_image_number = max(highest_image_number, image_number)

# How to get model hash:
# go to http://127.0.0.1:7860/docs#/default/get_sd_models_sdapi_v1_sd_models_get
# and execute the code at: /sdapi/v1/sd-models

model_checkpoints = [
    "sd_xl_base_1.0.safetensors [31e35c80fc]",
    "dreamshaperXL10_alpha2Xl10.safetensors",
    "rundiffusionXL_beta.safetensors",
    "samaritan3dCartoon_v40SDXL.safetensors [1b8fca3fee]"
    ]
prompts = [
    "Digital artwork of Ezio from Assins' Creed franchise, depicted in full from head to toe",
    "Digital artwork of Bayek from Assins' Creed Origins, depicted in full from head to toe",
    "Digital artwork of Eivor from Assins' Creed Valhalla, depicted in full from head to toe"
    ]
for m in model_checkpoints:
    for p in prompts:
        # Default generation parameters
        payload = {
            "prompt": p,
            #"negative_prompt": ,
            "seed": 1476951986,
            "width": 1024,
            "height": 1024,
            "sampler_name": "Euler a",
            "cfg_scale": 7.0, 
            "steps": 100, 
            "restore_faces": False, 
            "denoising_strength": 0, 
            "extra_generation_params": {},                                                                                                                                                                                                                                                                                         "styles": [], 
        }
        # Custom best parameters for specific models
        # /!\ For SDXL base 1.0 when setting 1080x1080 you'll get a torch.cuda.OutOfMemoryError 
        # that can be fixed if you delete --no-half from the webui-user.bat
        
        #if m == "sd_xl_base_1.0.safetensors [31e35c80fc]":
            #payload["width"] = 1344
            #payload["height"] = 768

        # For the script to override the model chosen on A1111    
        override_settings = {
            "sd_model_checkpoint": m
        }
        override_payload = {
            "override_settings": override_settings
        }
        payload.update(override_payload)

        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        r = response.json()

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