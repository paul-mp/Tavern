from flask import Flask, abort, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
app = Flask(__name__)

posts = []

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:abc@localhost/postgres"
#need a proper env file for this
app.secret_key = 'super secret key'
db.init_app(app)
bcrypt = Bcrypt(app)

from models import User


@app.route("/", methods=["GET"])
def index():
    if "username" in session:
        return redirect("/post_login")
    return render_template("index.html")


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        raw_password = request.form.get('password')
        if not username or not raw_password:
            abort(400)
        hashed_password = bcrypt.generate_password_hash(raw_password, 12).decode()
        new_user = User(username, hashed_password)
        db.session.add(new_user)
        db.session.commit()
    else: 
        return render_template("signup.html")
    return redirect('/login')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        raw_password = request.form.get('password')
        if not username or not raw_password:
            abort(401)
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            abort(401)
        if not bcrypt.check_password_hash(existing_user.password, raw_password):
            abort(401)
        session['username'] = username
        return redirect('/')
    else:
        return render_template("login.html")


@app.route("/sign_up", methods=["GET"])
def sign_up():
    return render_template("sign_up.html")


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

@app.get("/post_login")
def post_login():
    if "username" not in session:
        abort(401)
    return render_template("post_login.html")

@app.route("/forum", methods=["GET"])
def forum():
    # Pass the list of posts to the forum template
    return render_template("forum.html", posts=posts)
