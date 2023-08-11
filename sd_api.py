import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://127.0.0.1:7860"

payload = {
    "prompt": "cute pink dog",
    "steps": 10,
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()
print(r.get("info"))

# Get the seed value
seed = r.get('seed')
print(seed)

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    
    # Update the output directory path
    output_path = r"E:\GIT_ROOT\AC-EKO-IA\AUTOMATIC1111\outputs\sd_api\output.png"
    image.save(output_path, pnginfo=pnginfo)