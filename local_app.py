from flask import Flask
import local_wip

app = Flask(__name__)

@app.route("/")
def index():
    text = local_wip.catch_a_ride()
    return text

app.run(host="127.0.0.1", port=8080)