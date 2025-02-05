from os import getenv
import googlemaps


def get_coords(address):
    """
    Fetch the latitude and longitude for a given address using
    the Google Maps API.

    Google Maps API: https://developers.google.com/maps/documentation/geocoding/start

    Args:
        address (str): The address to geocode.

    Returns:
        tuple: A tuple containing latitude (float) and longitude (float),
        or (None, None) if not found.
    """
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=getenv("GOOGLE_MAPS_API_KEY"))

    # Geocode the address (fetch the latitude and longitude)
    geocode_result = gmaps.geocode(f"{address}")

    if geocode_result and len(geocode_result) > 0:
        # Extract the latitude and longitude from the response
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None, None
