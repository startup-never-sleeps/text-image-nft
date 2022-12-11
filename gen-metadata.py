import os
import json
from copy import deepcopy

BASE_JSON = {
    "name": "",
    "description": "",
    "attributes": [],
}

def generate_metadata(name: str, description: str):
    json_path = "./nfts/metadata/"
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    
    # Get a copy of the base JSON (python dict)
    item_json = deepcopy(BASE_JSON)
    item_json['name'] = name
    item_json['description'] = description
    #TODO: add attributes

    item_json_path = os.path.join(json_path, item_json['name'] + ".json")
    with open(item_json_path, 'w') as f:
        json.dump(item_json, f)

