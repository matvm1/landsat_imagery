from app import create_app
from app.gee_image_service import initialize_gee, hello_gee

app = create_app()

@app.route("/")
def hello_world():
    initialize_gee()
    hello_gee()
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)

