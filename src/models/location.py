from src.support import google_location_details
from src.support.location_collections import load_collection
from geopy.distance import vincenty


class Location:
    SUPPORTED_ATTRIBUTES = ['id', 'name', 'street', 'city', 'state', 'zipcode',
                            'formatted_address', 'phone', 'lat', 'lng', 'url']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.formatted_address = kwargs.get('formatted_address')
        self.street = kwargs.get('street')
        self.city = kwargs.get('city')
        self.state = kwargs.get('state')
        self.zipcode = kwargs.get('zipcode')
        self.phone = kwargs.get('phone')
        self.lat = kwargs.get('lat')
        self.lng = kwargs.get('lng')
        self.url = kwargs.get('url')

    @classmethod
    def build_from_google_id(cls, google_id):
        location_details = google_location_details(google_id)
        location_details['id'] = kwargs.get('place_id')
        parsed_address = cls.__parse_address_components(location_details.get('address_components', []))
        location_details['street'] = self.__build_street_name(parsed_address)
        location_details['city'] = parsed_address.get('city')
        location_details['state'] = parsed_address.get('state')
        location_details['zipcode'] = parsed_address.get('zipcode')
        location_details['phone'] = location_details.get('formatted_phone_number')
        location = location_details.get('geometry', {}).get('location', {})
        location_details['lat'] = location.get('lat')
        location_details['lng'] = location.get('lng')
        return Location(**location_details)

    @classmethod
    def load_locations_from_collection(cls, map_id, file_id=None):
        location_json = load_collection(map_id, file_id=file_id)
        locations = [Location(**details) for loc_id, details in location_json.items()]
        return locations

    def to_dict(self):
        location_dict = {}
        for attr_name in self.SUPPORTED_ATTRIBUTES:
            if not hasattr(self, attr_name): continue
            attr_value = getattr(self, attr_name)
            if attr_value:
                location_dict[attr_name] = attr_value
        return location_dict

    def to_row(self):
        row = []
        for attribute in self.SUPPORTED_ATTRIBUTES:
            if hasattr(self, attribute):
                row.append(getattr(self, attribute))
            else:
                row.append(None)
        return row

    def distance(self, location, unit='miles'):
        distance = vincenty((self.lat, self.lng), (location.lat, location.lng))
        return getattr(distance, unit)

    @staticmethod
    def best_zoom_level(distance):
        default_zoom = 8
        adjustment = int(float(distance)/0.6)
        return max(default_zoom - adjustment, 4)


    @staticmethod
    def __parse_address_components(address_components):
        type_mappings = {
            'subpremise': 'unit',
            'street_number': 'street_number',
            'route': 'street',
            'locality': 'city',
            'administrative_area_level_2': 'county',
            'administrative_area_level_1': 'state',
            'country': 'country',
            'postal_code': 'zipcode'
        }
        address = {}
        for ac in address_components:
            types = ac['types']
            component_type = types[0]
            short_name = ac['short_name']
            if component_type in type_mappings:
                type_mapping = type_mappings[component_type]
                address[type_mapping] = short_name
        return address

    @staticmethod
    def __build_street_name(parsed_address):
        street = parsed_address.get('street')
        street_number = parsed_address.get('street_number')
        unit = parsed_address.get('unit')
        if street_number:
            street = f'{street_number} {street}'
        if unit:
            street = f'{street} {unit}'
        return street
