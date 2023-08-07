
import math

import modules.scripts as scripts
import gradio as gr
from PIL import Image

from modules import processing, shared, sd_samplers, images, devices
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

import os
import glob

from modules import images
from modules import processing
from modules.processing import process_images, Processed
from modules.generation_parameters_copypaste import parse_generation_parameters
from modules.extras import run_pnginfo


# This script is made from the AUTO1111 script located at "E:\GIT_ROOT\AC-EKO-IA\AUTOMATIC1111\scripts\sd_upscale.py"
# with a few modification to allow for batch upscaling from an initial directory of images (of a lower resolution)
# to an output directory of images with a specific resolution (1024x1024 to work with SDXL 1.0)

# To activate the venv, open VsCode terminal (View/Open View/Terminal)
# cd E:\GIT_ROOT\pythonProject
# From remote work: "Get-ExecutionPolicy" is restricted,  run "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
# At work: .\venv\Scripts\Activate

# Set the input and output directories
input_directory = r'E:\GIT_ROOT\AC-EKO-IA\AUTOMATIC1111\outputs\txt2img-images\2023-08-02'
output_directory = r'C:\Users\svc_ac-eko-ia\Desktop\Stable_Diff_Yonah\rescaled_images\training_images'

# List image files in the input directory
image_files = glob.glob(os.path.join(input_directory, '*.jpg'))

class Script(scripts.Script):
    def title(self):
        return "Custon Png Info SD Upscale"

    def show(self, is_img2img):
        return is_img2img

    def ui(self, is_img2img):        
        info = gr.HTML("<p style=\"margin-bottom:0.75em\">Will upscale the image by the selected scale factor; use width and height sliders to set tile size</p>")
        overlap = gr.Slider(minimum=0, maximum=256, step=16, label='Tile overlap', value=64, elem_id=self.elem_id("overlap"))
        scale_factor = gr.Slider(minimum=1.0, maximum=4.0, step=0.05, label='Scale Factor', value=2.0, elem_id=self.elem_id("scale_factor"))
        upscaler_index = gr.Radio(label='Upscaler', choices=[x.name for x in shared.sd_upscalers], value=shared.sd_upscalers[0].name, type="index", elem_id=self.elem_id("upscaler_index"))
		
        wantPrompt = gr.Checkbox(False, label="Override Prompt")
        wantNegative= gr.Checkbox(False, label="Override Negative Prompt")
        wantSeed = gr.Checkbox(False, label="Override Seed")
        wantSteps = gr.Checkbox(False, label="Override Steps")
        wantCFGScale = gr.Checkbox(False, label="Override CFG scale")
        wantSize = gr.Checkbox(False, label="Override Width and Height")
        wantdenoise = gr.Checkbox(False, label="Override Denoising strength")		

        return [info, overlap, upscaler_index, scale_factor, wantPrompt, wantNegative, wantSeed,wantSteps,wantCFGScale,wantSize,wantdenoise]

    def run(self, p, _, overlap, upscaler_index, scale_factor, wantPrompt, wantNegative, wantSeed,wantSteps,wantCFGScale,wantSize,wantdenoise):
        if isinstance(upscaler_index, str):
            upscaler_index = [x.name.lower() for x in shared.sd_upscalers].index(upscaler_index.lower())

		
        mytext = run_pnginfo(p.init_images[0])[1]
        deets = parse_generation_parameters(mytext)
        if wantPrompt and 'Prompt' in deets:
            p.prompt = deets['Prompt']
        if wantNegative and 'Negative prompt' in deets:
            p.negative_prompt = deets['Negative prompt']
        if wantSeed and 'Seed' in deets:
            p.seed = float(deets['Seed'])
        if wantSteps and 'Steps' in deets:
            p.steps = int(deets['Steps'])
        if wantCFGScale  and 'Seed' in deets:
            p.cfg_scale = float(deets['CFG scale'])                        
        if wantSize and 'Size-1' in deets:
            p.width = int(deets['Size-1'])
        if wantSize and 'Size-2' in deets:
            p.height = int(deets['Size-2'])
        if wantdenoise and 'Denoising strength' in deets:
            p.denoising_strength = float(deets['Denoising strength'])
        
        processing.fix_seed(p)
		
		
		
		
        upscaler = shared.sd_upscalers[upscaler_index]

        p.extra_generation_params["SD upscale overlap"] = overlap
        p.extra_generation_params["SD upscale upscaler"] = upscaler.name

        initial_info = None
        seed = p.seed

        init_img = p.init_images[0]
        init_img = images.flatten(init_img, opts.img2img_background_color)

        if upscaler.name != "None":
            img = upscaler.scaler.upscale(init_img, scale_factor, upscaler.data_path)
        else:
            img = init_img

        devices.torch_gc()

        grid = images.split_grid(img, tile_w=p.width, tile_h=p.height, overlap=overlap)

        batch_size = p.batch_size
        upscale_count = p.n_iter
        p.n_iter = 1
        p.do_not_save_grid = True
        p.do_not_save_samples = True

        work = []

        for y, h, row in grid.tiles:
            for tiledata in row:
                work.append(tiledata[2])

        batch_count = math.ceil(len(work) / batch_size)
        state.job_count = batch_count * upscale_count

        print(f"SD upscaling will process a total of {len(work)} images tiled as {len(grid.tiles[0][2])}x{len(grid.tiles)} per upscale in a total of {state.job_count} batches.")

        result_images = []
        for n in range(upscale_count):
            start_seed = seed + n
            p.seed = start_seed

            work_results = []
            for i in range(batch_count):
                p.batch_size = batch_size
                p.init_images = work[i * batch_size:(i + 1) * batch_size]

                state.job = f"Batch {i + 1 + n * batch_count} out of {state.job_count}"
                processed = processing.process_images(p)

                if initial_info is None:
                    initial_info = processed.info

                p.seed = processed.seed + 1
                work_results += processed.images

            image_index = 0
            for y, h, row in grid.tiles:
                for tiledata in row:
                    tiledata[2] = work_results[image_index] if image_index < len(work_results) else Image.new("RGB", (p.width, p.height))
                    image_index += 1

            combined_image = images.combine_grid(grid)
            result_images.append(combined_image)

            if opts.samples_save:
                images.save_image(combined_image, p.outpath_samples, "", start_seed, p.prompt, opts.samples_format, info=initial_info, p=p)

        processed = Processed(p, result_images, seed, initial_info)

        return processed
    

# Function to upscale and save images
def upscale_and_save_image(image_file):
    # Load the image
    image = Image.open(image_file)

    # Define the upscale parameters (you can customize these values as needed)
    overlap = 64
    scale_factor = 2.0
    upscaler_index = 0  # Set the index for the desired upscaler, e.g., 0 for the first upscaler

    # Create an instance of the Script class
    upscale_script = Script()

    # Call the run function to upscale the image
    processed_image = upscale_script.run(image, _, overlap=overlap, upscaler_index=upscaler_index, scale_factor=scale_factor,
                                         wantPrompt=False, wantNegative=False, wantSeed=False, wantSteps=False,
                                         wantCFGScale=False, wantSize=False, wantdenoise=False)

    # Get the upscaled image from the processed_image object
    upscaled_image = processed_image.images[0]

    # Save the upscaled image to the output directory with the same filename
    output_filename = os.path.join(output_directory, os.path.basename(image_file))
    upscaled_image.save(output_filename)

# Loop through the image files and upscale them
for image_file in image_files:
    upscale_and_save_image(image_file)

print("Upscaling completed.")