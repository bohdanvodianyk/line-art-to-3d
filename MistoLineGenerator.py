from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline, AutoencoderKL
from diffusers.utils import load_image
from PIL import Image
import torch
import numpy as np
import cv2

# prompt = "aerial view, a futuristic research complex in a bright foggy jungle, hard lighting"
# prompt = "photo of elephant 8k high definition in jungle"
prompt = "Generate an anime-style image of a grand pirate ship with exaggerated proportions and vibrant colors. Feature ornate sails and a tumultuous sea, conveying action and adventure."
negative_prompt = 'low quality, bad quality, sketches, blurry, ugly, duplicate, poorly drawn, deformed, mosaic'

# image = load_image("https://huggingface.co/datasets/hf-internal-testing/diffusers-images/resolve/main/sd_controlnet/hf-logo.png")
image = load_image("input-LineArt/car_future.jpg")
controlnet_conditioning_scale = 0.5

controlnet = ControlNetModel.from_pretrained(
    "diffusers/controlnet-canny-sdxl-1.0",
    torch_dtype=torch.float16
)
vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    controlnet=controlnet,
    vae=vae,
    torch_dtype=torch.float16,
)
pipe.enable_model_cpu_offload()

image = np.array(image)
image = cv2.Canny(image, 100, 200)
image = image[:, :, None]
image = np.concatenate([image, image, image], axis=2)
image = Image.fromarray(image)

images = pipe(
    prompt, negative_prompt=negative_prompt, image=image, controlnet_conditioning_scale=controlnet_conditioning_scale,
    ).images

images[0].save(f"output-LineArt/car_future_new.png")

