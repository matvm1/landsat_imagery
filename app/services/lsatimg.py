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


def get_lsatimg(lat, lon):
    lat = ee.Number(lat)
    lon = ee.Number(lon)

    # Define the region (a small rectangle around the city)
    # TODO: Refine the region based on the city's area
    region = ee.Geometry.Rectangle([
        lon.subtract(0.13), lat.subtract(0.07),
        lon.add(0.13), lat.add(0.07)
    ])

    # Use Landsat 8 imagery
    image_collection = ee.ImageCollection(IMAGE_COLLECTION_NAME) \
        .filterBounds(region) \
        .filterDate('2020-01-01', '2025-12-31') \
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
        bands=bands,  # Landsat 8 RGB bands
        min=min_vals,  # Convert EE values to Python
        max=max_vals,
        gamma=1.4  # Slight gamma adjustment for contrast
    )

    return normalized_image


def get_lsatimg_url(image):
    # Generate thumbnail URL
    url = image.getThumbURL({'region': image.geometry(), 'format': 'png'})

    return url


def get_lsatimg_stats(image):
    stats = image.reduceRegion(
        reducer=ee.Reducer.percentile([2, 98]),
        geometry=image.geometry(),
        scale=30,
        maxPixels=1e13
    )

    stats_info = stats.getInfo()
    band_stats = {}
    for band in [band for combination in BAND_COMBINATIONS.values() for band
                 in combination]:
        band_stats[band + '_min'] = stats_info[band + '_p2']
        band_stats[band + '_max'] = stats_info[band + '_p98']

    return band_stats
