import json
import csv
import requests
from sys import argv
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
from src.models import Location
from src.support import google_location_search

load_dotenv()

example_location = []
test_candidates = [example_location]


def google_csv_to_google_mapping(file_name):
    locations = None
    with open(file_name, 'r') as infile:
        reader = csv.reader(infile)
        locations = transform_google_rows(reader)
    save_locations(locations, file_name)


def google_geocode_csv(file_name):
    locations = None
    with open(file_name, 'r') as infile:
        reader = csv.reader(infile)
        locations = run_geocodes(reader)
    save_locations(locations, file_name)


def test_sample_locations():
    locations = run_geocodes(test_candidates)
    save_locations(locations, 'test-candidates.csv')


def save_locations(locations, file_name):
    location_map = {location.id: location.to_dict() for location in locations}
    out_file_name = f'google-geocode-{file_name}'.replace('.csv', '')
    with open(f'{out_file_name}.json', 'w') as outfile:
        json.dump(location_map, outfile)


def transform_google_rows(rows):
    locations = []
    for row in rows:
        locations.append(Location(**{
            'id': row[0],
            'name': row[1],
            'street': row[2],
            'city': row[3],
            'state': row[4],
            'zipcode': row[5],
            'formatted_address': row[6],
            'phone': row[7],
            'lat': float(row[8]),
            'lng': float(row[9]),
            'url': row[10]
        }))
    return locations


def run_geocodes(candidates):
    locations = []
    for candidate in candidates:
        name = candidate[0]
        street = candidate[1]
        city = candidate[2]
        state = candidate[3]
        lat = 0 if not candidate[4] else float(candidate[4])
        lng = 0 if not candidate[5] else float(candidate[5])
        print(f'Getting geocoding for {name}')
        results = google_location_search(name, city, state)
        if len(results) == 0:
            print(f'WARNING:: Could not find match for {name} in {city}, {state}')
            continue
        elif len(results) == 1:
            result = results[0]
        else:
            result = pick_best_result(results, name, street, city, state, lat, lng)
        location = Location.build_from_google_id(result['place_id'])
        locations.append(location)
    return locations


def pick_best_result(results, name, street, city, state, lat, lng):
    target_address = f'{street} {city}, {state}'
    best_result = None
    best_lat_lng_diff = 9999999
    best_address_score = -1

    for result in results:
        result_name = result.get('name')
        result_address = result.get('formatted_address')
        result_location = result.get('geometry', {}).get('location', {})
        result_lat = result_location.get('lat')
        result_lng = result_location.get('lng')

        if lat and lng and result_lat and result_lng:
            lat_diff = abs(lat) - abs(result_lat)
            lng_diff = abs(lng) - abs(result_lng)
            total_diff = abs(lat_diff) + abs(lng_diff)
            if total_diff < best_lat_lng_diff:
                best_lat_lng_diff = total_diff
                best_result = result
        elif (best_lat_lng_diff == 0) or (best_lat_lng_diff >= 0.02):
            partial_score = fuzz.partial_ratio(result_address.lower(), target_address.lower())
            ratio_score = fuzz.ratio(result_address.lower(), target_address.lower())
            best_score = max([partial_score, ratio_score])
            if best_score > best_address_score:
                best_address_score = best_score
                best_result = result
    return best_result


if __name__ == '__main__':
    # TODO :: Keep original mapping ID to better QA errors
    TEST_RUN = False
    ALREADY_FORMATTED = False
    if ALREADY_FORMATTED:
        google_csv_to_google_mapping(argv[1])
    elif TEST_RUN:
        test_sample_locations()
    else:
        google_geocode_csv(argv[1])
