import os.path

import modules.scripts as scripts
import gradio as gr

from modules import shared, sd_samplers_common
from modules.processing import Processed, process_images

class Script(scripts.Script):
    def title(self):
        return "Save steps of the sampling process to files"

    def ui(self, is_img2img):
        path = gr.Textbox(label="Save images to path", placeholder="Enter folder path here. Defaults to webui's root folder")
        return [path]

    def run(self, p, path):
        if not os.path.exists(path):
            os.makedirs(path)
        index = [0]

        def store_latent(x):
            image = shared.state.current_image = sd_samplers_common.sample_to_image(x)
            image.save(os.path.join(path, f"sample-{index[0]:05}.png"))
            index[0] += 1
            fun(x)

        fun = sd_samplers_common.store_latent
        sd_samplers_common.store_latent = store_latent

        try:
            proc = process_images(p)
        finally:
            sd_samplers_common.store_latent = fun

        return Processed(p, proc.images, p.seed, "")