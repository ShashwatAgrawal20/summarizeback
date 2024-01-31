from flask import Flask

app = Flask(__name__)


@app.route("/")
def back():
    return "<h1>Ram Ram</h1>"


if __name__ == "__main__":
    app.run()
