# Land Satellite Image Lookup

## Description
This project enables analysts and researchers to view land satellite image captures in multiple visual wavelengths.
The arrangement of different spectral bands allows them to view this image capture in the following representations:
- Natural  
- False Color (urban)  
- Color Infrared (vegetation)  
- Agriculture  
- Atmospheric Penetration  
- Healthy Vegetation  
- Land/Water  
- Natural With Atmospheric Removal  
- Shortwave Infrared  
- Vegetation Analysis  

The images rendered by this project are fetched from Google Earth Engine's Landsat 8 Surface Reflectance Tier 1 image collection.
For more, see [LANDSAT 8 Collection 2 Tier 1 Level 2 Dataset](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2).
Imagery metadata and images are available for download.

## Features
- Land satellite image lookup in 10 different spectral bands for almost any address
- Satellite capture metadata download
- Image gallery download

## Usage
The tool is available at https://mateovergara.pythonanywhere.com/. Recommended for desktop use only.
To obtain landsat imagery:
1. Enter a location name or address in the search box. This search is backed by Google Geocoding API, so most location names/addresses are supported.
2. Select the spectral band combinations to render the images in.
3. Click "See Land Satellite Imagery".

A gallery containing all of the images will be rendered, dislaying the satellite capture in all of the different spectral band combinations requested.
The satellite capture metadata is available for download, as well as all of the rendered images.
Images can be seen in full-screen by clikcing on them in the gallery.

## Technical Notes
This is a Flask web application that uses the [Google Geocoding API](https://github.com/googlemaps/google-maps-services-python) to fetch (lat, lon) coordinates for the location name/address entered by the user (app/services/geocoder.py).
It then queries the Google Earth Engine API's LANDSAT/LC08/C02/T1_L2 image collection for the least cloudy satellite image capture of a region around the fetched coordinates (app/services/lastimg.py). The image capture is then ["visualized"](https://developers.google.com/earth-engine/apidocs/ee-image-visualize) by [Google Earth Engine](https://developers.google.com/earth-engine/guides/python_install) into images colorized by the spectral band combinations requested. Visual enhancements are made to the images so that they are colored and brightened appropiately for users.
Client-side cookies are used to pass the capture metadata and image URLs to /get_landsat_img should the user want to download them. Going back to thehome page clears these session variables.
Several libraries are usedby this project. See requirements.txt.

## Installation

    git clone https://github.com/matvm1/city_center_detector
    pip install -r requirements.txt

Once cloned, create a .env file in the project root with the following variables:
- `GOOGLE_MAPS_API_KEY` = *Google Geocoding API key*
- `GOOGLE_APPLICATION_CREDENTIALS` = *path to JSON file containing Google Cloud service account key*
- `GEE_SERVICE_ACCOUNT` = *Google Cloud project service account email*
- `SESSION_KEY` = *key*
- `FLASK_APP` = `run.py`
- `FLASK_DEBUG` = 1 (Note: only needed when running in development)

A Google Cloud project is required, along with an API Key for the Geocoding API and a service account and service account key for the Earth Engine API.