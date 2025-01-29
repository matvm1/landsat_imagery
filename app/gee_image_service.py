import ee

def initialize_gee():
    """Authenticate and initialize Google Earth Engine."""
    try:
        ee.Authenticate()
        ee.Initialize(project='ee-city-center-detector')
        print("Google Earth Engine initialized successfully.")
    except Exception as e:
        print(f"Error initializing GEE: {e}")

def get_satellite_image():
    city_name = "NYC"
    # Get the coordinates of the city
    #lat, lon = get_coordinates(city_name)

    lat = 40.7128
    lon = 74.0060
    
    if lat is None or lon is None:
        print(f"Could not find the coordinates for {city_name}.")
        return
    else:
        print(f"Coordinates for {city_name}: {lat}, {lon}")
    
    # Define the region (a small buffer around the city)
    point = ee.Geometry.Point(lon, lat)
    region = point.buffer(10000)  # Buffer of 10km
    
    # Use Landsat 8 imagery (you can adjust the date range as needed)
    # Perhaps enhance by filtering out cloudy images rather than sorting
    image_collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterBounds(region) \
        .filterDate('2020-01-01', '2025-12-31') \
        .sort('CLOUDY_PIXEL_PERCENTAGE') \
        .first()  # Take the first image with least clouds
    
    # Get the image
    image = image_collection.clip(region)
    
    # You can visualize the image, e.g., using folium or exporting the image
    # For this example, we'll export the image
    url = image.getThumbURL({
        'min': 0,
        'max': 3000,
        'bands': ['SR_B4', 'SR_B3', 'SR_B2'],  # RGB bands
        'dimensions': 512
    })

    print(f"Satellite image URL: {url}")
    return url
    
