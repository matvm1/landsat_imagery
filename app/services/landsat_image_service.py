import ee


def init_landsat_service():
    """Authenticate and initialize Google Earth Engine."""
    try:
        ee.Authenticate()
        ee.Initialize(project='ee-city-center-detector')
        print("Google Earth Engine initialized successfully.")
    except Exception as e:
        print(f"Error initializing GEE: {e}")


def get_landsat_image(lat, lon):
    lat = ee.Number(lat)
    lon = ee.Number(lon)

    # Define the region (a small rectangle around the city)
    # TODO: Refine the region based on the city's area
    region = ee.Geometry.Rectangle([
        lon.subtract(0.13), lat.subtract(0.07),
        lon.add(0.13), lat.add(0.07)
    ])

    # Use Landsat 8 imagery
    image_collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterBounds(region) \
        .filterDate('2020-01-01', '2025-12-31') \
        .sort('CLOUD_COVER')

    image = image_collection.first().clip(region)

    image_id = image.get('system:index').getInfo()

    print("Image ID:", image_id)

    # Compute min/max values for normalization using percentiles
    stats = image.reduceRegion(
        # Compute 2nd and 98th percentile
        reducer=ee.Reducer.percentile([2, 98]),
        geometry=region,
        scale=30,
        maxPixels=1e13
    )

    # Get min/max values in a single getInfo() call
    stats_info = stats.getInfo()
    
    RGBbands = ['SR_B4', 'SR_B3', 'SR_B2']

    # Get min/max values dynamically
    min_vals = [stats_info[band + '_p2'] for band in RGBbands]
    max_vals = [stats_info[band + '_p98'] for band in RGBbands]

    # Normalize the image using computed min/max values
    normalized_image = image.visualize(
        bands=RGBbands,  # Landsat 8 RGB bands
        min=min_vals,  # Convert EE values to Python
        max=max_vals,
        gamma=1.4  # Slight gamma adjustment for contrast
    )

    # Generate thumbnail URL
    url = normalized_image.getThumbURL({'region': region, 'format': 'png'})

    print(f"Satellite image URL: {url}")
    return url
