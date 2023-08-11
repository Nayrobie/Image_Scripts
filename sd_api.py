import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

# Access automatic1111: set up API url and payload
url = "http://127.0.0.1:7860"

payload = {
    "prompt": "magicien in the woods",
    "steps": 10
}

# See http://127.0.0.1:7860/docs#/default/text2imgapi_sdapi_v1_txt2img_post
response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()

# Process generated images
for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save('output.png', pnginfo=pnginfo)