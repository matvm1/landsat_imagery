from app import create_app
from app.image_service import initialize_gee, get_satellite_image
from flask import render_template

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_landsat_img")
def get_landsat_image():
    initialize_gee()
    city_landsat_img_url = get_satellite_image()
    return render_template("city_center.html",
                           city_landsat_img_url=city_landsat_img_url)


if __name__ == "__main__":
    app.run(debug=True)
