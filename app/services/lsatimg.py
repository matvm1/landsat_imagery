import ee

IMAGE_COLLECTION_NAME = 'LANDSAT/LC08/C02/T1_L2'
BAND_COMBINATIONS = {
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

# Defines the width of the geographic area when fetching landsat image
# (in geographic degrees)
REGION_X_DEGREE_WIDTH = 0.08
REGION_Y_DEGREE_WIDTH = 0.08

# ImageCollection start and end date filters
IMG_COLLECTION_START_DATE = '2020-01-01'
IMG_COLLECTION_END_DATE = '2025-12-31'

# Reducer options (for image color adjustment and resolution):
#   Min/Max: Percentile options for band RGB values
#   Scale: The size of the pixel grid during aggregation
#           (smaller scale -> higher resolution)
REDUCER_MIN = 2
REDUCER_MAX = 98
REDUCER_SCALE = 60

# Gamma adjustment for contrast when visualizing
GAMMA_ADJUSTMENT = 1.4


def get_lsatimg(lat, lon):
    lat = ee.Number(lat)
    lon = ee.Number(lon)

    # Define the region (a small rectangle around the city)
    region = ee.Geometry.Rectangle([
        lon.subtract(REGION_X_DEGREE_WIDTH),
        lat.subtract(REGION_Y_DEGREE_WIDTH),
        lon.add(REGION_X_DEGREE_WIDTH),
        lat.add(REGION_Y_DEGREE_WIDTH)
    ])

    # Use Landsat 8 imagery
    image_collection = ee.ImageCollection(IMAGE_COLLECTION_NAME) \
        .filterBounds(region) \
        .filterDate(IMG_COLLECTION_START_DATE, IMG_COLLECTION_END_DATE) \
        .sort('CLOUD_COVER')

    image = image_collection.first().clip(region)
    image.stats = get_lsatimg_stats(image)

    return image


def viz_lsat_img(image, band_comp_str):
    bands = BAND_COMBINATIONS[band_comp_str]

    # Get min/max values dynamically
    min_vals = [image.stats[band + '_min'] for band in bands]
    max_vals = [image.stats[band + '_max'] for band in bands]

    # Normalize the image using computed min/max values
    normalized_image = image.visualize(
        bands=bands,
        min=min_vals,
        max=max_vals,
        gamma=GAMMA_ADJUSTMENT
    )

    return normalized_image


def get_lsatimg_url(image):
    # Generate thumbnail URL
    url = image.getThumbURL({'region': image.geometry(), 'format': 'png'})

    return url


def get_lsatimg_stats(image):
    stats = image.reduceRegion(
        reducer=ee.Reducer.percentile([REDUCER_MIN, REDUCER_MAX]),
        geometry=image.geometry(),
        scale=REDUCER_SCALE,
        bestEffort=True
    )

    stats_info = stats.getInfo()
    band_stats = {}
    for band in [band for combination in BAND_COMBINATIONS.values() for band
                 in combination]:
        band_stats[band + '_min'] = stats_info[f"{band}_p{REDUCER_MIN}"]
        band_stats[band + '_max'] = stats_info[f"{band}_p{REDUCER_MAX}"]

    return band_stats
