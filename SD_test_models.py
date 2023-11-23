"""
The utility of this script is to test models on a base of a few prompts and basic parameters
to compare the artistic directions and limitations of different checkpoint models
"""

import requests

# A1111 API URL
url = "http://127.0.0.1:7860"

# Output directory for saving generated images
output_directory = "D:\GIT\stable-diffusion-webui\outputs\sd_api\model_testing"

# Prompt input
prompts = [
    "Digital artwork of Ezio from Assassin's Creed, depicted in full from head to toe, (full body lenght:1.2), character sheet, detailed",
    "Hand-drawn rough sketch, mix of bold dark lines and loose lines, (concept art:1.2), demon assassin's creed character, demon horns, black fire magic, ancient runes, detailed, masterpiece",
    "(neutral background:1.5) Character concept art of a fiendly humanoid creature made of wood, tall, gentle, detailed",
    "Hyperrealistic art, intricate (colourful:1.1) beautiful lycanthropic phoenix, ethereal, cyborg, biomorph, skinless, glass skeleton, biomechanical, hdr, high contrast",
    "Minimalist, 3D rendering, heavy pistol, semi worn with handpainted details onto it, handcrafted, artwork",
    "concept art, a skeleton in an dusty orange astronaut suit, (sci-fi atmosphere:1.2), orange and black, hand painted texture, bright colors, smooth lighting, centered, masterpiece",
    "Fantasy 3D environnement, indie game art, a grass path surrounded by ruins, taken over by nature, colourful, detailed, narrative",
    "neutral background, centred (assassin's creed tactic glove:1.2), leather, metal, detailed, neutral colours, 4K",
    "A woman in a bazaar, marketplace scene, vendors, items, imagination, intricate, sharp focus, dynamic lighting, vivid colors, subject-background isolation, detailed, masterpiece",
    "Digital artwork, (close up:0.5), a dragon, friendly creature, blue eyes, white scales",
    "(neutral background:1.5),centred 3D render of a crown made of wood and intertwined green lush plants",
]

# Model checkpoints to use for image generation
model_checkpoints = [
    "rundiffusionXL_beta.safetensors [f3efadbbaf]",
]

# Iterate over model checkpoints and prompts to generate images
for m in model_checkpoints:
    for p in prompts:
        # Default generation parameters
        txt2img_payload = {
            "prompt": p,
            "negative_prompt": "",
            "seed": 285248595,
            "width": 1024,
            "height": 1024,
            "sampler_name": "Euler a",
            "cfg_scale": 7.0,
            "steps": 20,
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