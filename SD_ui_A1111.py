# python .\artist_ui.py

import gradio as gr

# Default inputs
default_extra_tags = ["highly detailed", "masterpiece", "8k", "uhd"]
default_negative_prompt = ["low-quality, watermark, deformed, distorted anatomy, poor artistry, NSFW, Cleavage, Nudity, Naked, explicit content, mutated features, extra limbs, extra fingers, ugly, missing body parts, disconnected elements, malformed, abnormal proportions, aberrant hands, aberrant feet, aberrant legs, aberrant fingers"]

def generate_image(prompt, styles, perspectives, media, extra_tags, extra_negative_prompt=default_negative_prompt):
    # Concatenate additional negative keywords provided by the user with default negative prompt
    all_negative_prompts = f"{extra_negative_prompt}" if extra_negative_prompt else default_negative_prompt
    
    # Generated image logic here, using extra_tags and negative_prompt
    return f"Generated image with: {prompt}, {styles}, {perspectives}, {media}, {default_extra_tags}, {all_negative_prompts}"

# Define prompt keywords list
style_list = ["hyper-realistic", "minimalist", "surreal", "abstract", "steampunk", "cyberpunk", "mystical", "moody", "intricate details", "hazy atmosphere", "handcrafted", "mysterious", "ethereal", "enigmatic", "otherworldly"]
perspective_list = ["depth of field", "fisheye lens", "low view camera angle", "close-up shot", "wide shot", "full body length", "bird’s-eye view", "panoramic", "fixed focal length", "macro", "anamorphic", "overhead", "aerial"]
media_list = ["sketchbook", "oil painting", "photography", "concept art", "portrait", "3d rendering", "octane render", "editorial cinematic", "cinemascope", "vector depiction", "digital schematics", "pbr material", "watercolour", "charcoal drawing", "graffiti"]

# Create the entries with Gradio
prompt_input = gr.components.Textbox(lines=2, placeholder="Enter your prompt here", label="Prompt")
style_input = gr.components.Dropdown(choices=style_list, label="Style")
perspective_input = gr.components.Dropdown(choices=perspective_list, label="Perspective")
media_input = gr.components.Dropdown(choices=media_list, label="Media")
extra_negative_prompt_input = gr.components.Textbox(lines=2, placeholder="Enter your negative prompt here", label="Negative prompt")

# Create the ui
iface = gr.Interface(
    fn=generate_image,
    inputs=[
        prompt_input, style_input, perspective_input, media_input, extra_negative_prompt_input
    ],
    outputs=gr.components.Text(label="Generated Image Details"),
    title="Stable Diffusion Image Generator",
    description="Fill out the fields below to generate an image."
)

# Run the ui
iface.launch()