import cloudinary as cloudinary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:nhoclun3112001@localhost/qlkhachsan?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "!@#$%^&*()(*&^%$#@#$%^&*("
app.config["PAGE_SIZE"] = 6

mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cnpmute@gmail.com'
app.config['MAIL_PASSWORD'] = '25fnxzgm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["PAGE_SIZE"] = 10


app.config["CLOUDINARY_INFO"] = {
    "cloud_name": "ho-chi-minh-city-of-technology-and-education",
    "api_key": "169675629425989",
    "api_secret": "OSrJG1bxxUKpQfMHZ0iPjR1nX90"
}
cloudinary.config(cloud_name=app.config["CLOUDINARY_INFO"]['cloud_name'],
                                      api_key=app.config["CLOUDINARY_INFO"]['api_key'],
                                      api_secret=app.config["CLOUDINARY_INFO"]['api_secret'])


mail = Mail(app)

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="UTE HOTEL", template_mode="bootstrap4")
my_login = LoginManager(app=app)

ROOM_KEY = "room"
PHIEU_KEY = "phieu_thue"
CART_KEY = "cart"