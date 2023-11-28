import gradio as gr
import requests
import base64

# A1111 API
# url EKO 2 = "http://10.2.4.15:7860"
url = "http://10.2.5.35:7860"
# Doc http://10.2.4.15:7860/docs#/default

model_checkpoint = "dreamshaperXL10_alpha2Xl10.safetensors [0f1b80cfe8]"

def txt2img(prompt_input, model_checkpoint):
    txt2img_payload = {
        "prompt": prompt_input,
        "seed": -1,
        "width": 1024,
        "height": 1024,
        "sampler_name": "Euler a",
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

    # Save the image locally if it exists in the response
    image_data = r.get("images", [])
    if image_data and image_data[0].startswith("data:image"):
        image_base64 = image_data[0].split(",")[1]
        with open("generated_image.png", "wb") as img_file:
            img_file.write(base64.b64decode(image_base64))
        print("Image saved locally as generated_image.png")
    else:
        print("Saving image failed")
    
# Define prompt keywords list
style_list = ["hyper-realistic", "minimalist", "surreal", "abstract", "steampunk", "cyberpunk", "mystical", "moody", "intricate details", "hazy atmosphere", "handcrafted", "mysterious", "ethereal", "enigmatic", "otherworldly"]
perspective_list = ["depth of field", "fisheye lens", "low view camera angle", "close-up shot", "wide shot", "full body length", "bird’s-eye view", "panoramic", "fixed focal length", "macro", "anamorphic", "overhead", "aerial"]
media_list = ["sketchbook", "oil painting", "photography", "concept art", "portrait", "3d rendering", "octane render", "editorial cinematic", "cinemascope", "vector depiction", "digital schematics", "pbr material", "watercolour", "charcoal drawing", "graffiti"]

# Hidden entries
model_checkpoint_input = gr.components.Textbox(label=model_checkpoint)
# Visible entries
prompt_input = gr.components.Textbox(lines=2, placeholder="Enter your prompt here", label="Prompt")
style_input = gr.components.Dropdown(choices=style_list, label="Style")
perspective_input = gr.components.Dropdown(choices=perspective_list, label="Perspective")
media_input = gr.components.Dropdown(choices=media_list, label="Media")
negative_prompt_input = gr.components.Textbox(lines=2, placeholder="Enter your negative prompt here", label="Negative prompt")

# Create the ui
iface = gr.Interface(
    fn=lambda prompt_input: txt2img(prompt_input, model_checkpoint),
    inputs=[prompt_input],
    outputs=gr.components.Textbox(label="Generated Image Details"),
    title="Stable Diffusion Image Generator",
    description="Fill out the fields below to generate an image.",
)

# Run the ui
iface.launch()