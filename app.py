import txt2img
import os
import json
from simple_term_menu import TerminalMenu

MODEL_TYPE = txt2img.ModelType.OpenAI
MODEL_CONFIG = {"num_images":1, "num_rows":1}


def run_app():
	global MODEL_TYPE, MODEL_CONFIG	

	main_menu_exit = False
	main_menu = TerminalMenu(
        menu_entries=["Choose pre-trained model", "Change model config", "Generate images", "Quit"],
        title="    Text->Image->NFT app\n",
        cycle_cursor=True,
        clear_screen=True,
    )
	
	while not main_menu_exit:
		main_sel = main_menu.show()

		if main_sel == 0:
			model_type = input("""
Choose pre-trained model for image generation:
\t1. Stable Diffusion free model
\t2. OpenAI model\n
Current model is {}. Make you choice: """.format(MODEL_TYPE.name))
			MODEL_TYPE = txt2img.ModelType(int(model_type))

		elif main_sel == 1:
			model_config = input("""
Enter configuration for the generator as JSON.
Example: {'num_images':1, 'num_rows':1}
Current config: %s. Enter desired changes: """ % json.dumps(MODEL_CONFIG))
			model_config = json.loads(model_config)

			for key in MODEL_CONFIG:
				if key in model_config:
					MODEL_CONFIG[key] = model_config[key]

			input('Saved config is {}'.format(json.dumps(MODEL_CONFIG)))
			
		elif main_sel == 2:
			generate_images_loop(MODEL_TYPE, MODEL_CONFIG)
		elif main_sel == 3 or main_sel == None:
			main_menu_exit = True
			print("Exiting the app - hope you enjoyed it!!!")


# alternatives are consolemenu, simple-term-menu
def generate_images_loop(typ=None, config={}):
	model = txt2img.GetGlobalModel(typ)
	
	while True:
		description = input("Enter your description or '__exit__' to exit: ")
		if description == '__exit__': break

		try:
			image = model.get_image(description, **config)
			image.show()
		except Exception as ex:
			print(ex)
		
		os.system('clear')


# alternatives are consolemenu, simple-term-menu
if __name__ == '__main__':
	run_app()