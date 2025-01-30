from dotenv import load_dotenv
from app import create_app
from app.landsat_image_service import initialize_service, get_landsat_image
from flask import render_template, redirect, request
from app.geocoder_service import get_coordinates

load_dotenv(override=True)

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_landsat_img")
def landsat_image():
    initialize_service()

    lat, lon = get_coordinates(request.args.get('city'),
                               request.args.get('state'))

    # Check if the coordinates are valid
    if (lat, lon) == (None, None):
        print("Could not find the coordinates for the city.")
        return

    city_landsat_img_url = get_landsat_image(lat, lon)

    if not city_landsat_img_url:
        print(f"Error getting satellite image: {e}")
        return redirect("/")

    return render_template("city_center.html",
                           city_landsat_img_url=city_landsat_img_url)


if __name__ == "__main__":
    app.run(debug=True)
