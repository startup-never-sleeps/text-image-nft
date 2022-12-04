import torch
from diffusers import StableDiffusionPipeline
from PIL import Image


class TextImageDiffusion:
	def __init__(self, model_id='CompVis/stable-diffusion-v1-4'):
		self.pipe = TextImageDiffusion.get_diffusion_pipe(model_id)

	def genImage(self, description, num_images=1, num_rows=1):
		if num_images == 1:
			return self.pipe(description).images[0]
		else:
			description = [description] * num_images
			images = self.pipe(description).images

			num_cols = num_images // num_rows
			grid = TextImageDiffusion.get_image_grids(images, rows=num_rows, cols=num_cols)
			return grid

	@staticmethod
	def get_image_grids(images, rows, cols):
		assert len(images) == rows*cols

		width, height = images[0].size
		grid = Image.new('RGB', size=(cols*width, rows*height))
		
		for i, img in enumerate(img):
			grid.paste(img, box=(i%cols*width, i//cols*height))
		return grid

	@staticmethod
	def get_diffusion_pipe(model_id):
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


if __name__ == '__main__':
	imageGen = TextImageDiffusion()

	while True:
		description = input("Enter image desc: ")
		if description == '__exit__': break

		image = imageGen.genImage(description, num_images=6, num_rows=2)