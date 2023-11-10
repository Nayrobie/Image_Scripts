# Stable Diffusion Image Generation Scripts

This repository contains a few scripts for image generation using the Stable Diffusion (SD) model and the automatic1111 webui API.

## SD_image_generation_A1111.py

<img src="https://res.craft.do/user/full/7a93547b-a2a3-6209-a5e3-1a49258c4f73/doc/4EDB58DA-8EE5-4FDC-801D-829937E8FF43/8420CE19-8F5F-4F2C-8169-7F43AD74A11F_2/HbHdD1nzlPcnJyMtOX4Pue7wIfL4x80X00NDVPUvkBsz/GAI%20-%20Frame%202.jpeg" width="500">

This script facilitates image generation using different methods:

- **Txt2img:** Generates images based on textual prompts.
- **Img2img:** Runs Stable Diffusion with a prompt and an initial image, allowing users to add an image as input.
- **ControlNet:** Utilises ControlNets for text-to-image generation with additional control conditions.

#### How to Run:

Execute the script and follow the interactive prompts to choose the method, input image, prompts, and other parameters.

## SD_prompt_matrix_A1111.py

<img src="https://res.craft.do/user/full/7a93547b-a2a3-6209-a5e3-1a49258c4f73/doc/4EDB58DA-8EE5-4FDC-801D-829937E8FF43/314F4E36-4BF7-4955-BA37-FB625A988364_2/2mTwhNFZFF0WeFgLJigihPtRUTL3MuOgya2hRNEqRcsz/GAI%20-%20Frame%201.jpeg" width="500">

This script generates a matrix of images, experimenting with blending keywords for diverse image outputs. It is useful for exploring the impact of different prompts on image generation.

#### How to Run:

Execute the script and follow the prompts to choose keywords for the X and Y axes of the matrix.

## SD_saving_steps_A1111.py

![image](https://res.craft.do/user/full/7a93547b-a2a3-6209-a5e3-1a49258c4f73/doc/4EDB58DA-8EE5-4FDC-801D-829937E8FF43/A8476885-A8DA-419F-A907-4AB51D38AB7A_2/y9aqvy83R0S0EjMMszQr8OD6OZLXN9bHa92yCRVhZlMz/GAI%20-%20Frame%203.jpeg)

This script saves every step of the denoising process during image generation. It can be helpful for analyzing and understanding the evolution of images through the denoising steps.

#### How to Run:

This script doesn’t need to be run, place it at this location `"\stable-diffusion-webui\scripts\saving_steps.py"` then choose this script in Automatic1111 webui and copy the path to your output folder. Simply generate an image, and the script will automatically produce images corresponding to the number of sampling steps.

![image](https://res.craft.do/user/full/7a93547b-a2a3-6209-a5e3-1a49258c4f73/doc/4EDB58DA-8EE5-4FDC-801D-829937E8FF43/64B53CE5-A09F-499E-B6F6-05CC6752CE36_2/95yvSlZ3wu3EF3pw4VAFzPyzsEuemByoNvrb7dSm0sYz/Image.png)

## 🏗️ Prerequisites

- Install [automatic1111 webui](https://github.com/dvschultz/automatic1111) by following the instructions under the Read.me section
- Install the [ControlNet extension](https://github.com/Mikubill/sd-webui-controlnet) following their instructions and download at these four [ControlNet models](https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main) from the Hugging Face website:
	- `control_v11f1p_sd15_depth.pth`
	- `control_v11p_sd15_canny.pth`
	- `control_v11p_sd15_lineart.pth`
	- `control_v11p_sd15_scribble.pth`
- Download the `style.csv` document from this repository and place it at this location `"\stable-diffusion-webui\styles.csv"`
- Download the SD checkpoint models from [civitai.com](https://civitai.com/), the ones used in the scripts are 
	- `juggernautXL_version45.safetensors [ca4802bc3f]` 
	- `rundiffusionXL_beta.safetensors [f3efadbbaf]`
- The *prompt matrix* and *image generation* scripts can be run in [Visual Studio Code](https://code.visualstudio.com/)

## Contributors

- Yonah Bole
