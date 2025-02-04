from ee import Authenticate as ee_Auth, Initialize as ee_Init


def init_lsatimg():
    """Authenticate and initialize Google Earth Engine."""
    try:
        ee_Auth()
        ee_Init(project='ee-city-center-detector')
        print('Google Earth Engine initialized successfully')
    except Exception as e:
        print(f"Error initializing GEE: {e}")


from .lsatimg import (get_lsatimg, viz_lsat_img, get_lsatimg_url,
                      BAND_COMBINATIONS, IMAGE_COLLECTION_NAME)
from .geocoder import get_coords