import ee

def initialize_gee():
    """Authenticate and initialize Google Earth Engine."""
    try:
        ee.Authenticate()
        ee.Initialize(project='ee-city-center-detector')
        print("Google Earth Engine initialized successfully.")
    except Exception as e:
        print(f"Error initializing GEE: {e}")

def hello_gee():
    """Return a simple GEE Hello World response from the Earth Engine servers."""
    try:
        print(ee.String('Hello from the Earth Engine servers!').getInfo())
    except Exception as e:
        print(f"Error fetching message from GEE: {e}")
