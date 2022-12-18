from collections import defaultdict
import os
import base64
import uuid


class constructdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def save_image(image, store_dir):
    if not os.path.isdir(store_dir):
        os.makedirs(store_dir)

    image_name = 'image' + base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    image_path = os.path.join(store_dir, image_name)
    image.save(image_path, format=image.format)

    return image_name, os.path.abspath(image_path)
