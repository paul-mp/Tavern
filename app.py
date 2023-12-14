from flask import (
    Flask,
    session,
    redirect,
    render_template,
    request,
    abort,
    url_for,
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

# Retrieve environment variables for database connection and secret key
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
secret_key = os.getenv("SECRET_KEY")

# Create a connection string for the PostgreSQL database
connection_string = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.secret_key = secret_key

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

from models import User, Post, Reply


# Defining a route for the index page
@app.route("/", methods=["GET"])
def index():
    if "username" in session:
        return redirect("/post_login")
    return render_template("index.html", index_active=True)


# Defining a route for user registration
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        raw_password = request.form.get("password")

        if not username or not raw_password:
            error = "Invalid input."
        else:
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                error = "Username already exists."
            else:
                hashed_password = bcrypt.generate_password_hash(
                    raw_password, 12
                ).decode()
                new_user = User(username = username, password = hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect("/login")

    return render_template("sign_up.html", error=error)


# Defining a route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None
    if request.method == "POST":
        username = request.form.get("username")
        raw_password = request.form.get("password")
        if not username or not raw_password:
            error_message = "Username and password are required."
        else:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user or not bcrypt.check_password_hash(
                existing_user.password, raw_password
            ):
                error_message = "Incorrect username or password."
            else:
                session["username"] = username
                return redirect("/")
    return render_template("login.html", error=error_message)


# Defining a route for the sign-up page
@app.route("/sign_up", methods=["GET"])
def sign_up():
    return render_template("sign_up.html")


# Defining a route for the user profile page after login
@app.route("/user_profile", methods=["GET"])
def user_profile():
    if "username" not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(username=session["username"]).first()
    if user:
        join_date = user.creation_date.strftime("%m/%d/%Y")
        if(user.battle_scars >= 250):
            user.vip = True
            db.session.commit()
        return render_template(
            "user_profile.html", username=session["username"], join_date=join_date, battle_scars =  user.battle_scars, vip = user.vip
        )
    else:
        return redirect(url_for("login"))


# Defining a route for creating a new post
@app.route("/make_post", methods=["GET", "POST"])
def make_post():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["discussionTitle"]
        content = request.form["discussionContent"]
        tags = ", ".join(request.form.getlist("tags"))  # Join tags into a string
        user = User.query.filter_by(username=session["username"]).first()
        user.battle_scars += 10
        if user:
            new_post = Post(
                title=title, content=content, tags=tags, user_id=user.user_id
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("forum"))
        else:
            pass
    else:
        return render_template("make_post.html", create_active=True)


# Defining a route for the login page
@app.get("/post_login")
def post_login():
    if "username" not in session:
        return abort(401)
    return render_template("post_login.html", username=session["username"])


# Defining a route for the post-login page
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    session.modified = True
    return redirect("/")


@app.route("/forum")
@app.route("/forum/page/<int:page>")
def forum(page=1):
    per_page = 4
    pagination = Post.query.order_by(Post.creation_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    return render_template("forum.html", posts=posts, pagination=pagination, forum_active=True)


@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "username" not in session:
        return redirect(url_for("login"))

    post_to_delete = Post.query.get_or_404(post_id)
    if session["username"] != post_to_delete.user.username:
        return redirect(url_for("forum"))

    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("forum"))


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if "username" not in session:
        return redirect(url_for("login"))

    post_to_edit = Post.query.get_or_404(post_id)
    if session["username"] != post_to_edit.user.username:
        return redirect(url_for("forum"))

    if request.method == "POST":
        post_to_edit.title = request.form["title"]
        post_to_edit.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("forum"))
    else:
        return render_template("edit_post.html", post=post_to_edit)


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.views_count is None:
        post.views_count = 0
    post.views_count += 1
    db.session.commit()
    replies = (
        Reply.query.filter_by(post_id=post.id)
        .order_by(Reply.creation_date.desc())
        .all()
    )
    return render_template("post_detail.html", post=post, replies=replies)


@app.route("/submit_reply/<int:post_id>", methods=["POST"])
def submit_reply(post_id):
    if "username" not in session:
        flash("You must be logged in to reply.")
        return redirect(url_for("login"))

    reply_content = request.form["reply_content"]
    user = User.query.filter_by(username=session["username"]).first()
    user.battle_scars += 5

    if user and reply_content:
        # new Reply object with user.user_id
        reply = Reply(content=reply_content, post_id=post_id, user_id=user.user_id)
        db.session.add(reply)

        # get Post object and +1 replies_count
        post = Post.query.get(post_id)
        if post.replies_count is None:
            post.replies_count = 0
        post.replies_count += 1
        db.session.commit()
        flash("Your reply has been posted.")
    else:
        flash("There was an error posting your reply.")

    return redirect(url_for("show_post", post_id=post_id))
