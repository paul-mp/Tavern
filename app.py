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
    return render_template("profile.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/new_login", methods=["GET"])
def new_login():
    return render_template("new_login.html")