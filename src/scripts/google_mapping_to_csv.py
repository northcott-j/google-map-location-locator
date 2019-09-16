import csv
from sys import argv
from src.models import Location


def google_mapping_to_csv(map_id):
    locations = Location.load_locations_from_collection(map_id)
    rows = [Location.SUPPORTED_ATTRIBUTES]
    for location in locations:
        rows.append(location.to_row())

    with open(f'{map_id}.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


if __name__ == '__main__':
    google_mapping_to_csv(argv[1])
