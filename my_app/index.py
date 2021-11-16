import math
from typing import Union

from flask import render_template, request, session, jsonify
from my_app import app, my_login
from my_app.models import User
from flask_login import login_user
import hashlib
from admin import *



@app.route("/")
def home():
    return render_template("home.html")


@my_login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=['post'])
def login_exe():
    username = request.form.get("username")
    password = request.form.get("password")
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    user = User.query.filter(User.username == username,
                             User.password == password).first()
    if user: # dang nhap thanh cong
        login_user(user)
    return redirect("/admin")


# @app.route('/upload', methods=['post'])
# def upload():
#     avatar = request.files.get("avatar")
#     if avatar:
#         avatar.save("%s/static/images/%s" % (app.root_path, avatar.filename))
#         return "SUCCESSFUL"
#
#     return "FAILED"


@app.route("/loginUser")
def LoginControll():
    return render_template("/layout/loginUser.html")

@app.route("/registerUser")
def RegisterControll():
    return render_template("/layout/registerUser.html")

@app.route("/userInformation")
def UserInformationControll():
    return render_template("/layout/userInformation.html")

if __name__ == '__main__':
    app.run(debug=True)
