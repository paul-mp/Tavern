from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/forum")
def forum():
    return render_template("forum.html", forum=True)