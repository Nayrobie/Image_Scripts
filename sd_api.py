import json
import requests
import io
import base64
import re
from PIL import Image
import os

url = "http://127.0.0.1:7860"

output_directory = "E:\GIT_ROOT\AC-EKO-IA\AUTOMATIC1111\outputs\sd_api\models_comparison"
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
    "level4_v50BakedVAEFp16.safetensors [c61df6130b]",
    "SPYBGToolkit_v50-official.ckpt [5d6cf7c225]",
    "v1-5-pruned-emaonly.safetensors [6ce0161689]",
    "rpg_V4.safetensors [e04b020012]",
    "dreamshaper_6BakedVae.safetensors [c249d7853b]",
    "realisticVisionV20_v20NoVAE.safetensors [c0d1994c73]",
    "revAnimated_v122.safetensors [4199bcdd14]"
    ]
prompt1 = [
    "a developers conf poster, A Mandalorian squad centered, space, desert, mountains, art gta 5 cover, official fanart behance hd artstation by jesper ejsing, by rhads, makoto shinkai alois van baarle, ilya kuvshinov, ossdraws, orange tones, man in ski outfit"
    ]
prompt2 = "cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed iris, pupils, semi-realistic, text, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, canvas frame, bad art, weird colors, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, tiling, poorly drawn feet, mutated, cross-eye, body out of frame, nude, naked, watermark, blurred"

for model_checkpoint in model_checkpoints:
    for p in prompt1:
        payload = {
            "prompt": p,
            "negative_prompt": prompt2,
            "seed": 1500269447,
            "width": 512,
            "height": 512,
            "sampler_name": "Euler",
            "cfg_scale": 7.0, 
            "steps": 20, 
            "restore_faces": False, 
            "denoising_strength": 0, 
            "extra_generation_params": {},                                                                                                                                                                                                                                                                                         "styles": [], 
        }
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