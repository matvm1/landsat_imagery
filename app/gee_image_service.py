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
    # lat, lon = get_coordinates(city_name)

    # NYC
    #lat = ee.Number(40.7128)
    #lon = ee.Number(-74.0060)

    # Miami
    lat = ee.Number(25.7617)
    lon = ee.Number(-80.1918)

    if lat is None or lon is None:
        print(f"Could not find the coordinates for {city_name}.")
        return
    else:
        print(f"Coordinates for {city_name}: {lat}, {lon}")

    # Define the region (a small rectangle around the city)
    # TODO: Refine the region based on the city's area
    region = ee.Geometry.Rectangle([
        lon.subtract(0.13), lat.subtract(0.07),  # Bottom-left corner
        lon.add(0.13), lat.add(0.07)   # Top-right corner
    ])

    # Use Landsat 8 imagery (you can adjust the date range as needed)
    image_collection = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2') \
        .filterBounds(region) \
        .filterDate('2020-01-01', '2025-12-31')

    #image_collection = image_collection.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 50));

    image = image_collection.first().clip(region)

    out_image = image.visualize(
        bands=['SR_B4', 'SR_B3', 'SR_B2'],  # RGB bands
    )

    url = out_image.getThumbURL({region: region, format: 'png'})

    # Export the image
    print(f"Satellite image URL: {url}")
    return url

