import ee

def initialize_gee():
    """Authenticate and initialize Google Earth Engine."""
    try:
        ee.Authenticate()
        ee.Initialize(project='ee-city-center-detector')
        print("Google Earth Engine initialized successfully.")
    except Exception as e:
        print(f"Error initializing GEE: {e}")
