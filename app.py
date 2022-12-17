import txt2img
import os
import json
from simple_term_menu import TerminalMenu
import uuid
import base64

MODEL_TYPE = txt2img.ModelType.OpenAI
MODEL_CONFIG = {"num_images": 1, "num_rows": 1}


def run_app():
    global MODEL_TYPE, MODEL_CONFIG

    main_menu_exit = False
    main_menu = TerminalMenu(
        menu_entries=["Choose pre-trained model",
                      "Change model config", "Generate images", "Quit"],
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
            model_config = json.loads(model_config) if model_config else {}

            for key in MODEL_CONFIG:
                if key in model_config:
                    MODEL_CONFIG[key] = model_config[key]

            input('Saved config is {}. Press any key to continue...'.format(
                json.dumps(MODEL_CONFIG)))

        elif main_sel == 2:
            generate_images_loop(MODEL_TYPE, MODEL_CONFIG)
        elif main_sel == 3 or main_sel == None:
            main_menu_exit = True
            print("Exiting the app - hope you enjoyed it!!!")


# alternatives are consolemenu, simple-term-menu
def generate_images_loop(typ=None, config={}):
    model = txt2img.GetGlobalModel(typ)

    while True:
        try:
            description = input("""General commands:
	1. __exit__ to exit
	2. __save__ to save previous image
	3. __upload__ to upload image to OpenSea
	Enter your description to generate new image: """)
            if description == '__exit__':
                break
            elif description == '__save__':
                if not os.path.isdir('images'):
                    os.makedirs('images')
                filename = os.path.join(
                    'images', 'image' + base64.b64encode(uuid.uuid4().bytes).decode('utf-8'))
                image.save(filename, format=image.format)
                input('Image saved to {}. Press any key to continue...'.format(filename))
            elif description == '__upload__':
                # Upload image to OpenSea
                pass
            else:
                image = model.get_image(description, **config)
                image.show()

        except Exception as ex:
            print(ex)

        os.system('clear')


# alternatives are consolemenu, simple-term-menu
if __name__ == '__main__':
    run_app()
