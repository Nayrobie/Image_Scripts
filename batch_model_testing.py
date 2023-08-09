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


def cmdargs(line):
    args = shlex.split(line)
    pos = 0
    res = {}

    while pos < len(args):
        arg = args[pos]

        assert arg.startswith("--"), f'must start with "--": {arg}'
        assert pos+1 < len(args), f'missing argument for command line option {arg}'

        tag = arg[2:]

        if tag == "prompt" or tag == "negative_prompt":
            pos += 1
            prompt = args[pos]
            pos += 1
            while pos < len(args) and not args[pos].startswith("--"):
                prompt += " "
                prompt += args[pos]
                pos += 1
            res[tag] = prompt
            continue


        func = prompt_tags.get(tag, None)
        assert func, f'unknown commandline option: {arg}'

        val = args[pos+1]
        if tag == "sampler_name":
            val = sd_samplers.samplers_map.get(val.lower(), None)

        res[tag] = func(val)

        pos += 2

    return res


class Script(scripts.Script):
    def title(self):
        return "Batch testing"

    def ui(self):
            return []
    
    def run(self, p):
        # Set the seed value
        p.seed = 1500269447
        p.prompt="dog"
        p.do_not_save_grid = True

        state.job_count = 1

        copy_p = copy.copy(p)



        proc = process_images(copy_p)


        images = proc.images
        all_prompts = proc.all_prompts
        infotexts = proc.infotexts


        Processed(p, images, p.seed, "", all_prompts=all_prompts, infotexts=infotexts)

        p.prompt="cat"
        copy_p2 = copy.copy(p)
        copy_p2.prompt = "horse"
        proc2 = process_images(copy_p2)
        images2 = proc2.images
        all_prompts2 = proc2.all_prompts
        infotexts2 = proc2.infotexts

        Processed(p,images2, p.seed, "", all_prompts=all_prompts2, infotexts=infotexts2)

        return Processed(p,images2, p.seed, "", all_prompts=all_prompts2, infotexts=infotexts2)