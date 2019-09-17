import json
from os import getcwd, path
from src.support import download_location_collection
from src.support.exceptions import UnsupportedMapException


def load_collection(collection_id, file_id=None):
    if not collection_exists(collection_id) and file_id:
        return download_location_collection(file_id, collection_path(collection_id))
    elif collection_exists(collection_id):
        with open(collection_path(collection_id), 'r') as infile:
            return json.load(infile)
    else:
        raise UnsupportedMapException(collection_id)


def collection_exists(collection_id):
    return path.exists(collection_path(collection_id))


def collection_path(collection_id):
    return path.join(getcwd(), 'src', 'support', 'location_collections', f'{collection_id}.json')
