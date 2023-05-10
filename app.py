from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from model import create_collections, check_for_user, get_current_user_info, attempt_sign_in, upload_photo, list_images, list_all_images, attempt_sign_out
import os

app = Flask(__name__)

load_dotenv()
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app=app)
db = mongo.db

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    create_collections(db)
    if check_for_user(db):
        result = get_current_user_info(db)
        image_list = list_images(db, result["user_id"])
        return render_template("your_results.html", user=result["username"], images = image_list)
    else:
        return render_template('index.html')

@app.route('/signin', methods=['POST'])
def sign_in():
    create_collections(db)
    username = request.form['username']
    password = request.form['password']
    attempt_sign_in(db, username, password)
    result = get_current_user_info(db)
    image_list = list_images(db, result["user_id"])
    return render_template("your_results.html", user=username, images = image_list)

@app.route('/upload', methods=['POST'])
def upload():
    create_collections(db)
    img_link = request.form['img-link']
    upload_photo(db, img_link)
    return redirect("/")

@app.route('/all-pictures', methods=['GET', 'POST'])
def view_all_pictures():
    create_collections(db)
    all_image_list = list_all_images(db)
    return render_template("all_results.html", images = all_image_list)

@app.route('/signout', methods=['GET'])
def sign_out():
    attempt_sign_out(db)
    return redirect("/")

