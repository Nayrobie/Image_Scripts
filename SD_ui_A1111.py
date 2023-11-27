# 1. Installing Python 3.10.6
# Link to local install: https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe
# check the box that says "Add Python to PATH."
# 2. Create virtual environment in the Terminal:
# cd "C:\Users\ybole\Desktop\A1111_artist_ ui"
# python -m venv myenv
# .\myenv\Scripts\Activate
# 3. Lib installation:
# pip install gradio
# 4. Run the script:
# python image_generator.py


import gradio as gr
 
def generate_image(prompt, artist, style, format, perspective, booster, vibe, negative_constraints, parameters):
    # Votre logique de génération d'image vient ici.
    return f"Generated image with: {prompt}, {artist}, {style}, {format}, {perspective}, {booster}, {vibe}, {negative_constraints}, {parameters}"
 
# Créer les entrées Gradio en utilisant la nouvelle syntaxe de Gradio 4.7.1
prompt_input = gr.components.Textbox(lines=2, placeholder="Enter your prompt here", label="Prompt")
artist_input = gr.components.Dropdown(choices=["Artist 1", "Artist 2"], label="Artist")
style_input = gr.components.Dropdown(choices=["Style 1", "Style 2"], label="Style")
format_input = gr.components.Radio(choices=["Format 1", "Format 2"], label="Format")
perspective_input = gr.components.Radio(choices=["Perspective 1", "Perspective 2"], label="Perspective")
booster_input = gr.components.Slider(minimum=0, maximum=100, label="Booster")
vibe_input = gr.components.Dropdown(choices=["Vibe 1", "Vibe 2"], label="Vibe")
negative_constraints_input = gr.components.Textbox(lines=2, placeholder="Negative constraints", label="Negative Constraints")
parameters_input = gr.components.Textbox(lines=2, placeholder="Parameters", label="Parameters")
 
# Créer l'interface Gradio
iface = gr.Interface(
    fn=generate_image,
    inputs=[
        prompt_input, artist_input, style_input, format_input,
        perspective_input, booster_input, vibe_input,
        negative_constraints_input, parameters_input
    ],
    outputs=gr.components.Text(label="Generated Image Details"),
    title="Stable Diffusion Image Generator",
    description="Fill out the fields below to generate an image."
)
 
# Lancer l'interface
iface.launch()