import json
import requests
import io
import base64
import re
from PIL import Image
import os

url = "http://127.0.0.1:7860"

output_directory = "E:\GIT_ROOT\AC-EKO-IA\AUTOMATIC1111\outputs\sd_api\script_test"
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
    "SPYBGToolkit_v50-official.ckpt [5d6cf7c225]",
    "sd_xl_base_1.0.safetensors [31e35c80fc]",
    "rpg_V4.safetensors [e04b020012]"
    ]
prompt1 = [
    "A developers conf poster, Samurai warrior standing in a flower field, Japan, official fanart behance, extra realistic, shot with cinematic camera, remarkable colours, A developers conf poster, Samurai warrior standing in a flower field, Japan, official fanart behance, extra realistic"
    ]
prompt2 = "((text)), cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed iris, pupils, semi-realistic, text, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, canvas frame, bad art, weird colors, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, tiling, poorly drawn feet, mutated, cross-eye, body out of frame, nude, naked, watermark, blurred"

for model_checkpoint in model_checkpoints:
    for p in prompt1:
        # Default generation parameters
        payload = {
            "prompt": p,
            "negative_prompt": prompt2,
            "seed": 755961913,
            "width": 512,
            "height": 512,
            "sampler_name": "Euler",
            "cfg_scale": 7.0, 
            "steps": 20, 
            "restore_faces": False, 
            "denoising_strength": 0, 
            "extra_generation_params": {},                                                                                                                                                                                                                                                                                         "styles": [], 
        }
        # Custom best parameters for specific models
        # /!\ For SDXL base 1.0 when setting 1080x1080 you'll get a torch.cuda.OutOfMemoryError 
        # that can be fixed if you delete --no-half from the webui-user.bat
        if model_checkpoint == "sd_xl_base_1.0.safetensors [31e35c80fc]":
            payload["width"] = 1080
            payload["height"] = 1080
        if model_checkpoint == "SPYBGToolkit_v50-official.ckpt [5d6cf7c225]":
            payload["width"] = 768
            payload["height"] = 768

        # For the script to override the model chosen on A1111    
        override_settings = {
            "sd_model_checkpoint": model_checkpoint
        }
        override_payload = {
            "override_settings": override_settings
        }
        payload.update(override_payload)

        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        r = response.json()

        # Print all the generated image info
        print(r.get("info"))
        info_json = json.loads(r.get("info"))  # Parse the "info" JSON string

        # Extract the infotexts value
        infotexts = info_json.get("infotexts")[0]  # Assuming there's only one infotext
        filename = re.sub(r'[:,\s]+', '_', infotexts)
        filename = filename.replace("__", "_")  # Replace double underscores with a single underscore

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