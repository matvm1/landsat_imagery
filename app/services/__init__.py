from ee import Authenticate as ee_Auth, Initialize as ee_Init


def init_lsatimg_service():
    """Authenticate and initialize Google Earth Engine."""
    try:
        ee_Auth()
        ee_Init(project='ee-city-center-detector')
        print('Google Earth Engine initialized successfully')
    except Exception as e:
        print(f"Error initializing GEE: {e}")


from .lsatimg_service import get_lsatimg, viz_lsat_img, get_lsatimg_url