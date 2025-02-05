from dotenv import load_dotenv
from app import create_app
from app.services import (init_lsatimg, get_lsatimg, viz_lsat_img,
                          get_lsatimg_url, get_coords, LANDSAT_8_BAND_COMBINATIONS,
                          IMAGE_COLLECTION_NAME)
from flask import render_template, redirect, request


load_dotenv(override=True)
app = create_app()


@app.route('/')
def index():
    return render_template('index.html',
                           band_combination_options=LANDSAT_8_BAND_COMBINATIONS)


@app.route('/get_landsat_img')
def landsat_image():
    init_lsatimg()

    address = request.args.get('address')
    lat, lon = get_coords(address)

    # Check if the coordinates are valid
    if (lat, lon) == (None, None):
        print('Could not find the coordinates for the city.')
        return

    lsatimg = get_lsatimg(lat, lon)
    band_combinations_req = request.args.getlist('band_combination_option')

    for user_selection in band_combinations_req:
        if LANDSAT_8_BAND_COMBINATIONS.get(user_selection) is None:
            raise Exception(f"Band combination {user_selection} is invalid.")

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
