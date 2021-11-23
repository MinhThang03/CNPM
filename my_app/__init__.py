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
app.config['MAIL_USERNAME'] = 'hoangthai7514@gmail.com'
app.config['MAIL_PASSWORD'] = '25fnxzgm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



db = SQLAlchemy(app=app)
admin = Admin(app=app, name="UTE HOTEL", template_mode="bootstrap4")
my_login = LoginManager(app=app)

ROOM_KEY = "room"
PHIEU_KEY = "phieu_thue"
