import ee

IMAGE_COLLECTION_NAME = 'LANDSAT/LC08/C02/T1_L2'


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

    return image


def viz_lsat_img(image, bands):
    # Compute min/max values for normalization using percentiles
    stats = image.reduceRegion(
        # Compute 2nd and 98th percentile
        reducer=ee.Reducer.percentile([2, 98]),
        geometry=image.geometry(),
        scale=30,
        maxPixels=1e13
    )

    # Get min/max values in a single getInfo() call
    stats_info = stats.getInfo()

    # Get min/max values dynamically
    min_vals = [stats_info[band + '_p2'] for band in bands]
    max_vals = [stats_info[band + '_p98'] for band in bands]

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
