# This script saves every step of the denoising process during image generation.

import os.path
import modules.scripts as scripts
import gradio as gr
from modules import shared, sd_samplers_common
from modules.processing import Processed, process_images

class Script(scripts.Script):
    def title(self):
        return "Save steps of the sampling process to files"

    def ui(self, is_img2img):
        # User interface elements: a textbox to input the folder path
        path = gr.Textbox(label="Save images to path", placeholder="Enter folder path here. Defaults to webui's root folder")
        return [path]

    def run(self, p, path):
        # Create the specified folder if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)

        # Index to keep track of the step number
        index = [0]

        # Function to store latent images
        def store_latent(x):
            # Convert the latent sample to an image
            image = shared.state.current_image = sd_samplers_common.sample_to_image(x)
            
            # Save the image to the specified folder with a sequential filename
            image.save(os.path.join(path, f"sample-{index[0]:05}.png"))
            
            # Increment the index for the next step
            index[0] += 1
            
            # Call the original function
            fun(x)

        # Save the original store_latent function
        fun = sd_samplers_common.store_latent

        # Replace the store_latent function with the customized version
        sd_samplers_common.store_latent = store_latent

        try:
            # Process the images and store the denoising steps
            proc = process_images(p)
        finally:
            # Restore the original store_latent function
            sd_samplers_common.store_latent = fun

        # Return the processed images
        return Processed(p, proc.images, p.seed, "")
