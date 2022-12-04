class Txt2ImageApplication:
	def __init__(self):
		self.config = {'width':256, 'height':256, 'dim':'256x256', 'num_images':1, 'num_rows':1}

from simple_term_menu import TerminalMenu
def run_app():
	main_menu = TerminalMenu(
        menu_entries=["Choose model", "Change model config", "Generate images", "Quit"],
        title="    Text->Image->NFT app Menu.\n    Press Q or Esc to quit.\n",
        cycle_cursor=True,
        clear_screen=True,
    )
	
	while not main_menu_exit:
		main_sel = main_menu.show()

		if main_sel == 0:
			model = input("""
Choose pre-trained model for image generation:
\t1. Stable Diffusion free model
\t2. OpenAI model\n
Make you choice: """)
		elif main_sel == 1:
			config = input("""
Enter configuration for the generator as JSON.
Example: {'num_images':1, 'num_rows':1}
Current config: default_config
Enter desired changes: """)
			pairs = [pair.strip() for pair in config.split(',')]
			print(pairs)
		elif main_sel == 2:
			generate_images_loop()
		elif main_sel == 3 or main_sel == None:
			main_menu_exit = True
			print("Exiting the app - hope you enjoyed it!!!")


from consolemenu import *
from consolemenu.items import *
def console_menu():
	menu = ConsoleMenu("Text->Image->NFT app")

	menu_item = MenuItem("Choose pre-trained model")
	menu_item = MenuItem("Enter model configuration")

	function_item = FunctionItem("Generate images", generate_images_loop)

	menu.append_item(menu_item)
	menu.append_item(menu_item)
	menu.append_item(function_item)

	menu.show()

import txt2img
import json
import os
# alternatives are consolemenu, simple-term-menu
def generate_images_loop():
	model = txt2img.GetGlobalModel()
	
	while True:
		description = input("Enter your description or '__exit__' to exit: ")
		if description == '__exit__': break

		try:
			image = model.get_image(description)
			image.show()
		except Exception as ex:
			print(ex)
		
		os.system('clear')


# alternatives are consolemenu, simple-term-menu
if __name__ == '__main__':
	console_menu()