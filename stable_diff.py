import torch
from diffusers import StableDiffusionPipeline

def get_generator_pipe(model_id='CompVis/stable-diffusion-v1-4'):
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
	pipe = get_generator_pipe()

	while True:
		description = input("Enter image desc: ")
		if description == '__exit__': break

		image = pipe(description).images[0]
		image.show()