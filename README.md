## Google Map Location Locator

### Requirements
#### For Map View
- A Custom Google Map that is shared with the public
- Google Project API Key in order to search Places and show Map

#### For Location List
- Running backend service from this codebase that is available from the website hosting the map
- A Custom Google Map that is shared with the public

### Map View
Map view uses a map of locations that is made Public to show all locations.
These maps can be created using the Google [My Maps](https://www.google.com/maps/d/u/0/?hl=en) tool.

Search bar shows results biased to where the map is currently focused. When a location is
selected, the map refocuses and displays relevant pins.

*Limited styling has been applied. You will likely need to add your own CSS for your project*


### Location List (COMING SOON)
Using the user selected location, the closest store results are displayed in a list.

The zoom level of the map is dynamic and will adapt to get the closest location in focus.

This functionality requires making a POST request to a service that will generate the list
of results using the locations shown in the custom Google Map built for the **Map View**.


### Starting Location List Service
#### First Steps
- (COMING SOON)

#### Deploying to Heroku
- (COMING SOON)
