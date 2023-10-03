import io
import cv2
import base64
import requests
from PIL import Image

# A1111 URL
url = "http://127.0.0.1:7860"

# Encoding input image
def encode_image_to_base64(input_path):
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

# Specify the path to your input image
input_image_path = r"C:\Users\svc_ac-eko-ia\Downloads\house_gray.jpg"
encoded_image = encode_image_to_base64(input_image_path)

prompt = ""
negative_prompt = ""
model_checkpoint = "dreamshaper_8.safetensors [879db523c3]"

# A1111 payload
controlnet_payload = {
    "prompt": prompt,
    "negative_prompt": negative_prompt,
    "batch_size": 1,
    "steps": 20,
    "cfg_scale": 7,
    "save_images": True,
    "alwayson_scripts": {
        "controlnet": {
            "args": [
                {
                    "input_image": encoded_image,
                    "module": "depth_midas",
                    "model": "control_v11f1p_sd15_depth [cfd03158]",
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

# Read results
r = response.json()
result = r['images'][0]
image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))