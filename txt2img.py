import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import openai
import os
import requests
from io import BytesIO

openai.api_key = open(os.path.join('keys', 'open_ai.key')).read()


def _get_image_grids(images, rows, cols):
	assert len(images) == rows*cols

	width, height = images[0].size
	grid = Image.new('RGB', size=(cols*width, rows*height))
	
	for i, img in enumerate(images):
		grid.paste(img, box=(i%cols*width, i//cols*height))
	return grid


class StableDiffusionTextImageGenerator:
	def __init__(self, model_id='CompVis/stable-diffusion-v1-4', config={}):
		self.pipe = StableDiffusionTextImageGenerator._get_diffusion_pipe(model_id)

	def get_image(self, description, num_images=1, num_rows=1):
		description = [description] * num_images
		images = self.pipe(description, height=256, width=256).images

		if num_images == 1:
			return images[0]
		else:
			return _get_image_grids(images, num_rows, num_images//num_rows)

	@staticmethod
	def _get_diffusion_pipe(model_id):
		if torch.cuda.is_available():
			device = 'cuda'
			kwargs = {'revision':'fp16', 'torch_dtype':'torch.float16'}
		else:
			device = 'cpu'
			kwargs = {}

		pipe = StableDiffusionPipeline.from_pretrained(
			model_id,
			use_auth_token=True,
			**kwargs
		)

		return pipe.to(device)


class OpenAiTextImageGenerator:
	def get_image(self, description, num_images=1, num_rows=1):
		response = openai.Image.create(
			prompt=description,
			n=num_images,
			size='256x256'
		)

		images = []
		for resp in response['data']:
			url = resp['url']
			response = requests.get(url)
			img = Image.open(BytesIO(response.content))
			images.append(img)

		if num_images == 1:
			return images[0]
		else:
			return _get_image_grids(images, num_rows, num_images//num_rows)


from enum import Enum
class ModelType(Enum):
    StableDiffusion = 1
    OpenAI = 2


from utils import constructdict
global_models = constructdict(lambda typ: InitModel(typ))
def GetGlobalModel(typ=None):
    global global_models

    if typ is None: typ = ModelType.OpenAI
    return global_models[(typ)]


def InitModel(typ):
    if typ == ModelType.StableDiffusion:
        return StableDiffusionTextImageGenerator()
    else:
        return OpenAiTextImageGenerator()