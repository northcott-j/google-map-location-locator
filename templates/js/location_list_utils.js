function makeLocationHtml(location) {
  var contactHtml = makeContactHtml(location);
  var directionsHtml = makeDirectionsHtml(location);
  var locationHtml = '<div class="location-block">' + contactHtml + directionsHtml + '</div>';
  return locationHtml
}
function makeContactHtml(location) {
  var name = location.name;
  var nameHtml = '<span class="contact-detail location-name">' + name + '</span>';
  var street = location.street;
  var streetHtml = '<span class="contact-detail">' + street + '</span>';
  var city = location.city;
  var state = location.state;
  var zipcode = location.zipcode;
  var stateHtml = '<span class="contact-detail">' + city + ', ' + state + ' ' + zipcode + '</span>';
  var phone = location.phone;
  var phoneHtml = '<span class="contact-detail">' + phone + '</span>';
  return '<div>' + nameHtml + streetHtml + stateHtml + phoneHtml + '</div>';
}
function makeDirectionsHtml(location) {
  var distance = location.distance;
  var distanceHtml = '<span>' + distance.toString() + ' mi</span>';
  var mapsUrl = location.url;
  var navigateButton = '<a class="navigate-button" href="' + mapsUrl + '" target="_blank">Navigate</a>';
  return '<div><div class="directions">' + distanceHtml + navigateButton + '</div></div>'
}
function insertLocationBlock(location) {
  var locationHtml = makeLocationHtml(location);
  document.getElementById('locationList').insertAdjacentHTML('beforeend', locationHtml);
}
function renderLocationList(locations) {
  // Clear innerhtml first
  document.getElementById('locationList').innerHTML = '';
  locations.forEach(insertLocationBlock);
}
