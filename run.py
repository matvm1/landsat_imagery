from dotenv import load_dotenv
from app import create_app
from app.services import (init_lsatimg, get_lsatimg, viz_lsat_img,
                          get_lsatimg_url, get_coords)
from flask import render_template, redirect, request


load_dotenv(override=True)
app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_landsat_img')
def landsat_image():
    init_lsatimg()

    lat, lon = get_coords(request.args.get('city'),
                          request.args.get('state'))

    # Check if the coordinates are valid
    if (lat, lon) == (None, None):
        print('Could not find the coordinates for the city.')
        return

    city_landsat_img_url = get_lsatimg_url(viz_lsat_img(
        get_lsatimg(lat, lon), "RBG"))

    if not city_landsat_img_url:
        print('Error getting satellite image.')
        return redirect('/')

    return render_template('city_center.html',
                           city_landsat_img_url=city_landsat_img_url)


if __name__ == '__main__':
    app.run(debug=True)
