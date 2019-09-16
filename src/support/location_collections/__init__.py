import json


def load_collection(collection_id):
    with open(f'src/support/location_collections/{collection_id}.json', 'r') as infile:
        return json.load(infile)
