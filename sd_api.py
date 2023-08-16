import json
import requests
import io
import base64
import re
from PIL import Image

url = "http://127.0.0.1:7860"

payload = {
    "prompt": "black dragon",
    "steps": 10,
    "negative_prompt": "purple",
    "seed": 475849700
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()
# Print all the generated image info
print(r.get("info"))

info_json = json.loads(r.get("info"))  # Parse the "info" JSON string

# Extract the infotexts value
infotexts = info_json.get("infotexts")[0]  # Assuming there's only one infotext

filename = re.sub(r'[:,\s]+', '_', infotexts)
filename = filename.replace("__", "_")  # Replace double underscores with a single underscore
filename = filename + ".jpg"

# Select the first image from the images list
image_data = base64.b64decode(r['images'][0].split(",", 1)[0])
image = Image.open(io.BytesIO(image_data))

# Update the output directory path with the generated filename
output_path = f"E:\\GIT_ROOT\\AC-EKO-IA\\AUTOMATIC1111\\outputs\\sd_api\\{filename}"
image.save(output_path, format='JPEG', quality=95)