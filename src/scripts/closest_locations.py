from os import environ
from dotenv import load_dotenv
from src.models.location import Location

load_dotenv()


locations = Location.load_locations_from_collection(environ['MAP_ID_UNTAPPED'])
query = {
    'name': 'Northeastern University',
    'formatted_address': '360 Huntington Ave, Boston, MA 02115, USA',
    'street': '360 Huntington Ave',
    'city': 'Boston',
    'state': 'MA',
    'zipcode': '02115',
    'phone': '(617) 373-2000',
    'lat': 42.3398067,
    'lng': -71.08917170000001,
    'url': 'https://maps.google.com/?cid=14518198813298178444'
}

query_location = Location(**query)
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
other_locations = [cl[1] for cl in sorted_distances[:5]]

print({'zoom_level': zoom_level, 'query': query, 'closest_location': closest_location[1],
        'locations': other_locations})
