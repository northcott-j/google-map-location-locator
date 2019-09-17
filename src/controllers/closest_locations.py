from flask import Blueprint, jsonify
from typing import List, Dict
from src.models import Location
from src.support import check_map_id, inject_request_body, inject_location_collection

closest_locations = Blueprint('closest_locations', __name__)

@closest_locations.route('<string:map_id>', methods=['POST'])
@check_map_id
@inject_location_collection
@inject_request_body()
def get_closest_locations(map_id: str, locations: List, data: Dict):
    """
    Gets closest locations for a query

    :param map_id: ID for the map to lookup relevant locations
    :param locations: array of Location for this map_id
    :param data: injected request body that contains needed query info
    :return: {zoom_level: int, closest_location: Location, locations: [Location]}
    """
    query_location = Location(**data)
    distances = []
    for location in locations:
        distances.append((query_location.distance(location), location.to_dict()))

    sorted_distances = sorted(distances, key=lambda d: d[0])

    # Adding distance to locations
    for sd in sorted_distances:
        distance = sd[0]
        location = sd[1]
        location['distance'] = distance

    closest_location = sorted_distances[0]
    zoom_level = Location.best_zoom_level(closest_location[0])
    location_limit = min([data.get('limit', 20), 20])
    other_locations = [cl[1] for cl in sorted_distances[:location_limit]]
    response = {'zoom_level': zoom_level, 'query': data, 'closest_location': closest_location[1],
                'locations': other_locations}
    return jsonify(response)
