from os import getenv
import googlemaps


def get_coords(address):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=getenv("GOOGLE_MAPS_API_KEY"))

    # Geocode the address (fetch the latitude and longitude)
    geocode_result = gmaps.geocode(f"{address}")

    if geocode_result:
        # Extract the latitude and longitude from the response
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        print(f"Could not find coordinates for {address}")
        return None, None
