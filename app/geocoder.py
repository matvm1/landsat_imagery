import os
import googlemaps


def get_coordinates(city_name, state):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

    # Geocode the address (fetch the latitude and longitude)
    geocode_result = gmaps.geocode(f"{city_name}, {state}")

    if geocode_result:
        # Extract the latitude and longitude from the response
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        print(f"Could not find coordinates for {city_name}, {state}")
        return None, None
