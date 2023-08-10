import copy
import random
import sys
import traceback
import shlex

import modules.scripts as scripts
import gradio as gr

from modules import sd_samplers
from modules.processing import Processed, process_images
from modules.shared import state


def process_string_tag(tag):
    return tag

def process_int_tag(tag):
    return int(tag)

def process_float_tag(tag):
    return float(tag)

def process_boolean_tag(tag):
    return True if (tag == "true") else False


prompt_tags = {
    "sd_model": None,
    "outpath_samples": process_string_tag,
    "outpath_grids": process_string_tag,
    "prompt_for_display": process_string_tag,
    "prompt": process_string_tag,
    "negative_prompt": process_string_tag,
    "styles": process_string_tag,
    "seed": process_int_tag,
    "subseed_strength": process_float_tag,
    "subseed": process_int_tag,
    "seed_resize_from_h": process_int_tag,
    "seed_resize_from_w": process_int_tag,
    "sampler_index": process_int_tag,
    "sampler_name": process_string_tag,
    "batch_size": process_int_tag,
    "n_iter": process_int_tag,
    "steps": process_int_tag,
    "cfg_scale": process_float_tag,
    "width": process_int_tag,
    "height": process_int_tag,
    "restore_faces": process_boolean_tag,
    "tiling": process_boolean_tag,
    "do_not_save_samples": process_boolean_tag,
    "do_not_save_grid": process_boolean_tag
}


class Script(scripts.Script):
    def title(self):
        return "Batch testing"

    def ui(self):
            return []
    
    def run(self, p):
        # What's always true
        p.seed = 1500269447
        p.do_not_save_grid = True
        state.job_count = 1

        # List of prompts
        prompts = ["dog", "horse"]

        # Process images for each prompt
        processed_images = []
        for prompt in prompts:
            copy_p = copy.copy(p)
            copy_p.prompt = prompt
            proc = process_images(copy_p)
            images = proc.images
            all_prompts = proc.all_prompts
            infotexts = proc.infotexts
            processed_images.append(Processed(p, images, p.seed, "", all_prompts=all_prompts, infotexts=infotexts))

        # Return the list of processed images
        return processed_images