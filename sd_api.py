import json
import requests
import io
import base64
from PIL import Image

url = "http://127.0.0.1:7860"

payload = {
    "prompt": "mountain",
    "steps": 10,
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()
# Print all the generated image info
print(r.get("info"))

info_json = json.loads(r.get("info"))  # Parse the "info" JSON string

# Extract the Seed value from the infotexts list
seed = None
for infotext in info_json.get("infotexts", []):
    if "Seed" in infotext:
        seed = infotext.split("Seed: ")[1].split(",")[0]
        break

for i in r['images']:
    image_data = base64.b64decode(i.split(",", 1)[0])
    image = Image.open(io.BytesIO(image_data))

    # Update the output directory path with the seed value in the filename
    output_path = f"E:\\GIT_ROOT\\AC-EKO-IA\\AUTOMATIC1111\\outputs\\sd_api\\{seed}.jpg"
    image.save(output_path, format='JPEG', quality=95)

    # Open the saved image and add the parameters info as a comment
    with Image.open(output_path) as saved_image:
        comment = r.get("info")  # Use the info from the main response
        saved_image.info["comment"] = comment
        saved_image.save(output_path)