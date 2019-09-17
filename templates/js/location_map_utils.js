function mapSourceUrl(lat, long, zoom) {
  var urlBase = 'https://www.google.com/maps/d/u/0/embed?mid=';
  // TODO :: make zoom dynamic based on nearest search result
  var z = 'z=' + zoom;
  return urlBase + placesMapId + '&ll=' + lat + '%2C' + long + '&' + z
}

function centerLocationMap(lat, long, zoom) {
  document.getElementById("locationMap").src = mapSourceUrl(lat, long, zoom);
}

function placeToQuery(place) {
  return {
    'name': place.name,
    'formatted_address': place.formatted_address,
    'street': place.address,
    'phone': place.formatted_phone_number,
    'lat': place.geometry.location.lat(),
    'lng': place.geometry.location.lng(),
    'url': place.url,
    'limit': 5
  }
}

const lookupClosestLocations = async (url, place, callback) => {
  const response = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(placeToQuery(place)),
    headers: {
      'Content-Type': 'application/json'
    }
  })

  const jsonResponse = await response.json()
  callback(jsonResponse);
}
