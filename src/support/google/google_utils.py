import requests
from os import environ


def google_location_details(google_id):
    location_url = __location_detail_url(google_id)
    return __make_google_request(location_url, 'result')


def google_location_search(name, city, state, country=None):
    search_url = __location_search_url(name, city, state, country=country)
    return __make_google_request(search_url, 'candidates')

# TODO :: Add error handling to this (tenacity?)
def __make_google_request(request_url, request_key):
    keyed_url = f'{request_url}&key={environ["GOOGLE_PLACES_API"]}'
    response = requests.get(keyed_url).json()
    return response.get(request_key)

def __location_detail_url(google_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    fields = 'place_id,name,formatted_address,formatted_phone_number,url,geometry,address_components'
    return f'{url}?placeid={google_id}&fields={fields}'


def __location_search_url(name, city, state, country=None):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    fields = 'name,geometry,place_id,formatted_address'
    query = f'{name} {city} {state}{" {0}".format(country) if country else ""}'
    return f'{url}?inputtype=textquery&input={query}&fields={fields}'
