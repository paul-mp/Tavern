from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

posts = []


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/new_login", methods=["GET"])
def new_login():
    return render_template("new_login.html")

@app.route("/user_profile", methods=["GET"])
def user_profile():
    return render_template("user_profile.html")


@app.route("/make_post", methods=["GET", "POST"])
def make_post():
    if request.method == "POST":
        title = request.form["discussionTitle"]
        content = request.form["discussionContent"]
        tags = request.form.getlist("tags")  # getting list of tags
        # save the post data to a database
        # add to posts list
        posts.append({"title": title, "content": content, "tags": tags})
        return redirect(url_for("forum"))
    else:
        return render_template("make_post.html")


@app.route("/forum", methods=["GET"])
def forum():
    # Pass the list of posts to the forum template
    return render_template("forum.html", posts=posts)
