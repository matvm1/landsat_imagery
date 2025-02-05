from dotenv import load_dotenv
from app import create_app
from app.services import (init_lsatimg, get_lsatimg, viz_lsat_img,
                          get_lsatimg_url, get_coords,
                          LANDSAT_8_BAND_COMBINATIONS,
                          IMAGE_COLLECTION_NAME)
from flask import render_template, redirect, request


load_dotenv(override=True)
app = create_app()

VALID_HOMEPAGE_REQUEST_ARGS = ['address', 'band_combination_option']


@app.route('/')
def index():
    return render_template('index.html',
                           band_combinations=LANDSAT_8_BAND_COMBINATIONS)


@app.route('/get_landsat_img')
def landsat_image():
    try:
        init_lsatimg()
    except Exception:
        error_message = "Failed to authenticate/initialize Google Earth Engine"
        return render_template("error.html", error_message=error_message)

    address = request.args.get('address')
    lat, lon = get_coords(address)

    # Check if the coordinates are valid
    if (lat, lon) == (None, None):
        error_message = f"Could not find coordinates for {address}"
        return render_template("error.html", error_message=error_message)

    lsatimg = get_lsatimg(lat, lon)

    for arg in request.args.keys():
        if arg not in VALID_HOMEPAGE_REQUEST_ARGS:
            error_message = f"Request argument {arg} not supported"
            return render_template("error.html", error_message=error_message)

    band_combinations_req = request.args.getlist('band_combination_option')

    for user_selection in band_combinations_req:
        if LANDSAT_8_BAND_COMBINATIONS.get(user_selection) is None:
            error_message = f"Band combination {user_selection} is invalid"
            return render_template("error.html", error_message=error_message)

    city_lsatimg_urls = {}
    for combination in band_combinations_req:
        city_lsatimg_urls[combination] = (get_lsatimg_url(
                                            viz_lsat_img(
                                                lsatimg,
                                                combination)))

    return render_template('city_center.html',
                           image_collection_name=IMAGE_COLLECTION_NAME,
                           address=address,
                           city_lsatimg_urls=city_lsatimg_urls)


if __name__ == '__main__':
    app.run(debug=True)
