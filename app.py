from flask import Flask, session, redirect, render_template, request, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf FlaskForm
from flask_login import current_user
from wtforms import TextAreaField, SubmitField
from wtformt.validators import DataRequired
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve environment variables for database connection and secret key
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT') 
dbname = os.getenv('DB_NAME')
secret_key = os.getenv('SECRET_KEY')

# Create a connection string for the PostgreSQL database
connection_string = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.secret_key = secret_key

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models import User

# Defining a route for the index page
@app.route("/", methods=["GET"])
def index():
    if "username" in session:
        return redirect("/post_login")
    return render_template("index.html")

# Defining a route for the user profile page
@app.route("/profile", methods=["GET"])
def profile():
    if "username" not in session:
        return redirect(url_for('login'))
    return render_template("profile.html")

# Defining a route for user registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None 
    if request.method == 'POST':
        username = request.form.get('username')
        raw_password = request.form.get('password')

        if not username or not raw_password:
            error = "Invalid input."
        else:
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                error = "Username already exists."
            else:
                hashed_password = bcrypt.generate_password_hash(raw_password, 12).decode()
                new_user = User(username, hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login')
    
    return render_template("sign_up.html", error=error)

# Defining a route for user login
@app.route('/login', methods=["GET", "POST"])
def login():
    error_message = None
    if request.method == "POST":
        username = request.form.get('username')
        raw_password = request.form.get('password')
        if not username or not raw_password:
            error_message = 'Username and password are required.'
        else:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user or not bcrypt.check_password_hash(existing_user.password, raw_password):
                error_message = 'Incorrect username or password.'
            else:
                session['username'] = username
                return redirect('/')
    return render_template("login.html", error=error_message)

# Defining a route for the sign-up page
@app.route("/sign_up", methods=["GET"])
def sign_up():
    return render_template("sign_up.html")

# Defining a route for the user profile page after login
@app.route("/user_profile", methods=["GET"])
def user_profile():
    if "username" not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session["username"]).first()
    if user:
        join_date = user.creation_date.strftime('%m/%d/%Y')
        return render_template("user_profile.html", username=session["username"], join_date=join_date)
    else:
        return redirect(url_for('login'))

# Defining a route for creating a new post
@app.route("/make_post", methods=["GET", "POST"])
def make_post():
    if "username" not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        title = request.form["discussionTitle"]
        content = request.form["discussionContent"]
        tags = request.form.getlist("tags")
        posts.append({"title": title, "content": content, "tags": tags})
        return redirect(url_for("forum"))
    else:
        return render_template("make_post.html")

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

# Defining a route for user logout
@app.route("/forum", methods=["GET"])
def forum():
    posts = []
    if "username" not in session:
        return redirect(url_for('login'))
    # Pass the list of posts to the forum template
    posts = Post.query.all()
    return render_template("forum.html", posts=posts)

@app.route("/post/new", methods=["GET", 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        //TODO 
        //Make sure there is a post field in the data base sdf

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('forum'))
    return render_template('make_post.html', title = 'New Post', form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post=post)

class PostForm(FlaskForm):
    title = String('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')