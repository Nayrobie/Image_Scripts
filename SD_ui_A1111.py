import gradio as gr

def generate_image(prompt, styles, perspectives, media, extra_tags, negative_prompt):
    # Generated image logic here
    return f"Generated image with: {prompt}, {styles}, {perspectives}, {media}, {extra_tags}, {negative_prompt}"

# Define keyword lists
style_list = ["hyper-realistic", "minimalist", "surreal", "abstract", "steampunk", "cyberpunk", "mystical", "moody", "intricate details", "hazy atmosphere", "handcrafted", "mysterious", "ethereal", "enigmatic", "otherworldly"]
perspective_list = ["depth of field", "fisheye lens", "low view camera angle", "close-up shot", "wide shot", "full body length", "bird’s-eye view", "panoramic", "fixed focal length", "macro", "anamorphic", "overhead", "aerial"]
media_list = ["sketchbook", "oil painting", "photography", "concept art", "portrait", "3d rendering", "octane render", "editorial cinematic", "cinemascope", "vector depiction", "digital schematics", "pbr material", "watercolour", "charcoal drawing", "graffiti"]
extra_tag_list = ["highly detailed", "high budget", "epic", "masterpiece", "8k", "photoreal", "inspirational", "narrative-based visual", "uhd image", "dslr effect"]

# Create the input components with Gradio
prompt_input = gr.components.Textbox(lines=2, placeholder="Enter your prompt here", label="Prompt")
style_input = gr.components.CheckboxGroup(choices=style_list, label="Style")
perspective_input = gr.components.CheckboxGroup(choices=perspective_list, label="Perspective")
media_input = gr.components.CheckboxGroup(choices=media_list, label="Media")
extra_tag_input = gr.components.CheckboxGroup(choices=extra_tag_list, label="Extra tag")
extra_tag_input.set_properties(default=["highly detailed", "masterpiece", "8k"])  # Set default values
negative_prompt_input = gr.components.Textbox(lines=2, placeholder="Negative prompt", label="Negative prompt")

# Create the Gradio interface
iface = gr.Interface(
    fn=generate_image,
    inputs=[
        prompt_input, style_input, perspective_input, media_input,
        extra_tag_input, negative_prompt_input
    ],
    outputs=gr.components.Text(label="Generated Image Details"),
    title="Stable Diffusion Image Generator",
    description="Fill out the fields below to generate an image."
)

# Run the interface
iface.launch()