from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/forum", methods=["GET"])
def forum():
    return render_template("forum.html", forum=True)

@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html", forum=True)

