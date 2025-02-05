import ee

# Name of the Landsat 8 image collection in Google Earth Engine
IMAGE_COLLECTION_NAME = 'LANDSAT/LC08/C02/T1_L2'

# Dictionary mapping different band combinations for visualization
LANDSAT_8_BAND_COMBINATIONS = {
    'Natural': ['SR_B4', 'SR_B3', 'SR_B2'],
    'False Color (urban)': ['SR_B7', 'SR_B6', 'SR_B4'],
    'Color Infrared (vegetation)': ['SR_B5', 'SR_B4', 'SR_B3'],
    'Agriculture': ['SR_B6', 'SR_B5', 'SR_B2'],
    'Atmospheric Penetration': ['SR_B7', 'SR_B6', 'SR_B5'],
    'Healthy Vegetation': ['SR_B5', 'SR_B6', 'SR_B2'],
    'Land/Water': ['SR_B5', 'SR_B6', 'SR_B4'],
    'Natural With Atmospheric Removal': ['SR_B7', 'SR_B5', 'SR_B3'],
    'Shortwave Infrared': ['SR_B7', 'SR_B5', 'SR_B4'],
    'Vegetation Analysis': ['SR_B6', 'SR_B5', 'SR_B4']
}

# Defines the width of the geographic area when fetching Landsat image
# (in geographic degrees)
REGION_X_DEGREE_WIDTH = 0.08
REGION_Y_DEGREE_WIDTH = 0.08

# Image collection start and end date filters
IMG_COLLECTION_START_DATE = '2020-01-01'
IMG_COLLECTION_END_DATE = '2025-12-31'

# Reducer options for image color adjustment and resolution
REDUCER_MIN = 2  # Lower percentile for normalization
REDUCER_MAX = 98  # Upper percentile for normalization
REDUCER_SCALE = 60  # Pixel scale for aggregation (smaller -> higher resolution)

# Gamma adjustment for contrast when visualizing images
GAMMA_ADJUSTMENT = 1.0


def init_lsatimg():
    """
    Authenticate and initialize Google Earth Engine (GEE).

    GEE API: https://developers.google.com/earth-engine/apidocs
    """
    try:
        ee.Authenticate()
        ee.Initialize(project='ee-city-center-detector')
        print('Google Earth Engine initialized successfully')
    except Exception as e:
        print(f"Error initializing GEE: {e}")


def get_lsatimg(lat, lon):
    """
    Retrieve the first available Landsat 8 image for a given latitude
    and longitude, clipped to a small region.

    Args:
        lat (float): Latitude of the target location.
        lon (float): Longitude of the target location.

    Returns:
        ee.Image: The clipped Landsat 8 image with computed statistics for
        each band.
    """
    lat = ee.Number(lat)
    lon = ee.Number(lon)

    # Define the region (a small rectangle around the city)
    region = ee.Geometry.Rectangle([
        lon.subtract(REGION_X_DEGREE_WIDTH),
        lat.subtract(REGION_Y_DEGREE_WIDTH),
        lon.add(REGION_X_DEGREE_WIDTH),
        lat.add(REGION_Y_DEGREE_WIDTH)
    ])

    # Get the Landsat 8 image collection,
    # Filtered by region and date, sorted asc by cloud coverage
    image_collection = ee.ImageCollection(IMAGE_COLLECTION_NAME) \
        .filterBounds(region) \
        .filterDate(IMG_COLLECTION_START_DATE, IMG_COLLECTION_END_DATE) \
        .sort('CLOUD_COVER')

    # Get the first image in the collection and clip the bounds
    image = image_collection.first().clip(region)

    # Get stats for each band and set new attribute `stats`
    image.stats = get_lsatimg_stats(image)

    return image


def viz_lsat_img(image, band_comp_str):
    """
    Apply visualization parameters to a Landsat 8 image using a selected
    band combination.

    Args:
        image (ee.Image): The Landsat 8 image to visualize.
        band_comp_str (str): The band combination name.

    Returns:
        ee.Image: The visualized image with normalization and gamma correction.
    """
    bands = LANDSAT_8_BAND_COMBINATIONS[band_comp_str]

    # Get min/max values from computed band stats
    min_vals = [image.stats[band + '_min'] for band in bands]
    max_vals = [image.stats[band + '_max'] for band in bands]

    # Visualize the image using computed min/max values
    normalized_image = image.visualize(
        bands=bands,
        min=min_vals,
        max=max_vals,
        gamma=GAMMA_ADJUSTMENT
    )

    return normalized_image


def get_lsatimg_url(image):
    """
    Generate a thumbnail URL for the given Landsat 8 image.

    Args:
        image (ee.Image): The Landsat 8 image.

    Returns:
        str: A URL for viewing the image as a PNG.
    """
    url = image.getThumbURL({'region': image.geometry(), 'format': 'png'})
    return url


def get_lsatimg_stats(image):
    """
    Compute min and max percentile statistics for each band in the image.

    Args:
        image (ee.Image): The Landsat 8 image.

    Returns:
        dict: A dictionary containing min/max values for each band.
    """
    # Apply a reducer to the image for aggregation
    stats = image.reduceRegion(
        reducer=ee.Reducer.percentile([REDUCER_MIN, REDUCER_MAX]),
        geometry=image.geometry(),
        scale=REDUCER_SCALE,
        bestEffort=True
    )

    # Get image stats from GEE
    stats_info = stats.getInfo()
    band_stats = {}

    # Set the min/max percentiles for each band
    # List comprehension flattens all the bands in LANDSAT_8_BAND_COMBINATIONS
    for band in [band for combination in LANDSAT_8_BAND_COMBINATIONS.values()
                 for band in combination]:
        band_stats[band + '_min'] = stats_info[f"{band}_p{REDUCER_MIN}"]
        band_stats[band + '_max'] = stats_info[f"{band}_p{REDUCER_MAX}"]

    return band_stats
