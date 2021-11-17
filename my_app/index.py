import datetime
import math
from typing import Union

from flask import render_template, request, session, jsonify, url_for
from sqlalchemy import null
from my_app import app, my_login, utils, mail
from my_app.models import User
from flask_login import login_user
import hashlib
from admin import *
from flask_mail import Message


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
    if user:  # dang nhap thanh cong
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


@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = ""
    alert = 'danger'
    if request.method == 'POST':
        try:
            password = request.form["password"]
            confirm_password = request.form['confirm-password']
            if password.strip() == confirm_password.strip():

                data = request.form.copy()
                del data['confirm-password']

                user = utils.add_user(**data)
                if user != null:
                    alert = 'success'
                    err_msg = "Vui long kiem tra email de kich hoat tai khoan"
                else:
                    err_msg = "Du lieu dau vao khong hop le!"
            else:
                err_msg = "Xac nhan mat khau khong khop!"
        except:
            err_msg = "He thong dang co loi! Vui long quay lai sau!"

    return render_template('layout/registerUser.html', err_msg=err_msg, alert=alert)



@app.route('/active_account/<token>', methods=['GET'])
def active_account(token):
    code_token = token
    if current_user.is_authenticated:
        return redirect("/")
    user = User.verify_active_account_token(token)
    if not user:
        return redirect("/")
    msg = ""
    try:
        if (user.active == True):
            msg = "Tai khoan da kick hoat"
        else:
            utils.active_account(user)
            msg = "Kich hoat tai khoan thanh cong"
        return  msg
    except:
        msg = 'that bai'
        return msg


@app.route("/user-login", methods=['get', 'post'])
def normal_user_login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.encode("utf-8")).digest())
        user = User.query.filter(User.username == username,
                                 User.password == password).first()
        if user and user.active == True:  # dang nhap thanh cong
            login_user(user)
            return redirect(request.args.get("next", "/"))
        else:
            err_msg = "Username hoac password khong chinh xac!"

    return render_template("layout/loginUser.html", err_msg=err_msg)


# @app.route("/email")
# def email():
#     x = datetime.datetime.now()
#     date_time = x.strftime("%m/%d/%Y-%H:%M:%S")
#     username = 'thang'
#     good_referrer = 'Vui long click vao day de kich hoat tai khoan cua ban \nhttp://{0}?username={1}&active=True&{2}'.format(
#         request.host, username, date_time)
#     msg = Message('Kích hoạt tài khoản', sender='hoangthai7514@gmail.com', recipients=['nhoclun31101@gmail.com'])
#     msg.body = good_referrer
#     mail.send(msg)
#     return good_referrer



##-----------------Email reset password-----------------------

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect("/")

    email = request.form.get("email")
    if email:
        user = User.query.filter(User.email == email).first()
        if user:
            utils.send_password_reset_email(user, app.config['MAIL_USERNAME'])
        msg = 'Check your email for the instructions to reset your password'
        return render_template('layout/reset_password_request.html', msg = msg)
    return render_template('layout/reset_password_request.html')


@app.route('/reset_password/<token>', methods=['GET'])
def reset_password(token):
    code_token = token
    if current_user.is_authenticated:
        return redirect("/")
    return render_template('layout/reset_password.html', token=code_token)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_post():
    if request.method == 'POST':
        token = request.form.get('token')
        user = User.verify_reset_password_token(token)
        if not user:
            return redirect("/")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        if new_password != null and new_password == confirm_password:
            user.password = str(hashlib.md5(new_password.encode("utf-8")).digest())
            db.session.add(user)
            db.session.commit()
            return redirect('/user-login')
    return render_template('layout/reset_password.html')


##------------------end email reset password-------------------------


@app.route("/user-logout")
def normal_user_logout():
    logout_user()
    return redirect("/user-login")


@app.route("/userInformation")
def UserInformationControll():
    return render_template("layout/userInformation.html")


if __name__ == '__main__':
    app.run(debug=True)
