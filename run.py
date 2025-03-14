from dotenv import load_dotenv
from app import create_app
from app.services import (init_lsatimg, get_lsatimg, viz_lsat_img,
                          get_lsatimg_url, get_lsatimg_info, get_coords,
                          LANDSAT_8_BAND_COMBINATIONS,
                          IMAGE_COLLECTION_NAME)
import os
from flask import render_template, request, session, send_file
import logging
import datetime
import io
import json
import locale
import zipfile
import requests

# Load environment variables from .env file
load_dotenv(override=True)

# Create the Flask app instance
app = create_app()

# Set Flask session configuration
app.config['SECRET_KEY'] = os.getenv('SESSION_KEY')
app.config['SESSION_PERMANENT'] = False
# Session expires after 30 mins
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

# Define valid request arguments for the homepage
VALID_HOMEPAGE_REQUEST_ARGS = ['address', 'band_combination_option']


@app.route('/')
def index():
    """
    Render the homepage and clear session data.
    """
    # Clear session data on page load
    clear_session()
    return render_template('index.html',
                           band_combinations=LANDSAT_8_BAND_COMBINATIONS)


@app.route('/get_landsat_img')
def landsat_image():
    """
    Process land satellite image request, fetch coordinates,
    generate image URLs, and render gallery page.
    """
    # Initialize Google Earth Engine
    gee_init_status = init_lsatimg()
    if gee_init_status != 0:
        error_message = "Failed to authenticate/initialize Google Earth Engine"
        return render_template("error.html", error_message=error_message)

    address = request.args.get('address')  # Get address from request arguments

    # Fetch the coordinates for the given address
    lat, lon = None, None
    try:
        lat, lon = get_coords(address)
    except Exception as e:
        logging.exception(e)
        error_message = "Failed to fetch coordinates for the address"
        return render_template("error.html", error_message=error_message)

    # Ensure that the address was successfully geocoded
    if (lat, lon) == (None, None):
        error_message = f"Could not find coordinates for {address}"
        return render_template("error.html", error_message=error_message)

    # Retrieve Landsat image data
    lsatimg = get_lsatimg(lat, lon)
    # Store image metadata and address in session
    session['lsatimg'] = get_lsatimg_info(lsatimg)
    session['lsatimg_address'] = address

    # Validate request arguments
    for arg in request.args.keys():
        if arg not in VALID_HOMEPAGE_REQUEST_ARGS:
            error_message = f"Request argument {arg} not supported"
            return render_template("error.html", error_message=error_message)

    # Get requested band combinations
    band_combinations_req = request.args.getlist('band_combination_option')
    for user_selection in band_combinations_req:
        if LANDSAT_8_BAND_COMBINATIONS.get(user_selection) is None:
            error_message = f"Band combination {user_selection} is invalid"
            return render_template("error.html", error_message=error_message)

    # Generate URLs for the selected band combinations
    lsatimg_urls = {}
    for combination in band_combinations_req:
        lsatimg_urls[combination] = (get_lsatimg_url(
                                            viz_lsat_img(
                                                lsatimg,
                                                combination)))
        # Store image URLs in session
        session['lsatimg_urls'] = lsatimg_urls

    return render_template('city_center.html',
                           image_collection_name=IMAGE_COLLECTION_NAME,
                           address=address,
                           lsatimg_urls=lsatimg_urls)


@app.route('/download_lsatimg_info')
def download_lsatimg_info():
    """
    Allow users to download land satellite image metadata as a JSON file.
    """
    lsatimg = session.get('lsatimg')
    address = session.get('lsatimg_address')
    if lsatimg is None or address is None:
        error_message = "Failed to get session data for Landsat 8 image"
        logging.error(error_message)
        return render_template("error.html", error_message=error_message)

    try:
        # Convert metadata to JSON and store in memory
        output = io.BytesIO()
        json_data = json.dumps(lsatimg, indent=4)
        encoded_json_data = json_data.encode(locale.getpreferredencoding())
        output.write(encoded_json_data)
        output.seek(0)

        # Generate filename
        curr_datetime = datetime.datetime.now().isoformat()
        address = address.replace("/", "_")
        curr_datetime = curr_datetime.replace("/", "_")
        download_name = f"lsat8_img_info_{address}_{curr_datetime}.json"

        return send_file(output, as_attachment=True, mimetype='text/json',
                         download_name=download_name)
    except Exception as e:
        logging.exception(e)
        error_message = "Failed to download Landsat 8 image info"
        return render_template("error.html", error_message=error_message)


@app.route('/download_lsatimg_images')
def download_lsatimg_images():
    """
    Create and serve a ZIP file containing land satellite images (PNG format)
    based on user selections.
    """
    lsatimg_urls = session.get('lsatimg_urls')
    address = session.get('lsatimg_address')
    if lsatimg_urls is None or address is None:
        error_message = "Failed to get session data for Landsat 8 image URLs"
        logging.error(error_message)
        return render_template("error.html", error_message=error_message)

    try:
        # Create an in-memory ZIP file
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for combination, url in lsatimg_urls.items():
                address = address.replace("/", "_")
                combination = combination.replace("/", "_")
                img = requests.get(url)
                zipf.writestr(f"{address}_{combination}.png",
                              img.content)
        output.seek(0)

        # Generate filename
        curr_datetime = datetime.datetime.now().isoformat()
        download_name = f"lsat8_img_{address}_{curr_datetime}.zip"

        return send_file(output, as_attachment=True,
                         mimetype='application/zip',
                         download_name=download_name)
    except Exception as e:
        logging.exception(e)
        error_message = "Failed to download Landsat 8 images"
        return render_template("error.html", error_message=error_message)


def clear_session():
    """
    Remove stored session data related to land satellite images.
    """
    session.pop('lsatimg', None)
    session.pop('lsatimg_address', None)
    session.pop('lsatimg_urls', None)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
