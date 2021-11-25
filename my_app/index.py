import bdb

import math
from typing import Union

from flask import render_template, request, session, jsonify, url_for
from sqlalchemy import null
from my_app import app, my_login, utils, mail, ROOM_KEY, PHIEU_KEY, CART_KEY
from my_app.models import User
from flask_login import login_user
import hashlib
from admin import *
import datetime
from flask_mail import Message


# ------------------HOME-------------------------
@app.route("/")
def home():
    return render_template("home.html")


# ----------------END HOME----------------------------


# --------------LOGIN LOGOUT----------------------------
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


@app.route("/user-logout")
def normal_user_logout():
    logout_user()
    return redirect("/")


# ---------------END LOGIN LOGOUT----------------------------------


# @app.route('/upload', methods=['post'])
# def upload():
#     avatar = request.files.get("avatar")
#     if avatar:
#         avatar.save("%s/static/images/%s" % (app.root_path, avatar.filename))
#         return "SUCCESSFUL"
#
#     return "FAILED"


# ------------------ REGISTER ACCOUNT----------------------------
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
        return render_template("layout/activeUser.html", msg=msg)
    except:
        msg = 'that bai'
        return render_template("layout/activeUser.html", msg=msg)


# ----------------------END REGISTER ACCOUNT------------------------------


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
        return render_template('layout/reset_password_request.html', msg=msg)
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


# ----------------------BOOK ROOM NHANH------------------------------------
@app.route('/book_room', methods=['GET'])
def book_room():
    if (not current_user.is_authenticated):
        return render_template("layout/loginUser.html")

    type_book = request.args.get('type')
    list_loai_phong = utils.get_list_loai_phong()
    if type_book == 'fast':

        return render_template('layout/dat_phong_nhanh.html', list=list_loai_phong)
    else:
        features = utils.get_all_feature_room()
        msg = request.args.get('msg')
        if not msg:
            return render_template('layout/dat_phong_chi_tiet.html', features=features, list=list_loai_phong)
        else:
            return render_template('layout/dat_phong_chi_tiet.html', features=features, list=list_loai_phong, msg=msg)


@app.route('/book_room/fast', methods=['GET', 'POST'])
def book_room_fast():
    if (not current_user.is_authenticated):
        return render_template("layout/loginUser.html")

    if request.method == 'POST':
        loai_phong = request.form.get('loai_phong')
        type_book = request.form.get('type_book')
        date_check_in = request.form.get('date_check_in')
        msg = ''

        if not utils.is_book_fast(loai_phong, date_check_in):
            msg = "Dữ liệu không hợp lệ"
            list_loai_phong = utils.get_list_loai_phong()
            return render_template('layout/dat_phong_nhanh.html', msg=msg, list=list_loai_phong)
        else:
            list_room = utils.find_room_by_arg(loai_phong, 'Phòng Standard', 'Giường Đơn', 'Không có')
            if len(list_room) != 0:
                room = list_room[0]
                date_in = datetime.datetime.strptime(date_check_in, '%Y-%m-%d').date()
                date_out = date_in + datetime.timedelta(days=1)
                date_out = date_out.strftime("%Y-%m-%d")
                list_room_dto = utils.covert_room_bean(list_room, date_check_in, date_out, type_book)
                room_dict = session.get(ROOM_KEY)
                if not room_dict:
                    room_dict = {}
                room_dict = list_room_dto.get(str(room.id))

                session[ROOM_KEY] = room_dict

                num_people, max_people = utils.find_num_people_by_room(room)
                count_people = max_people - num_people
                loai_khach = CategoryCustomer.query.all()
                return render_template('layout/phieu_thue_phong_information.html', num_people=num_people,
                                       count_people=count_people, loai_khach=loai_khach)
    return redirect('/book_room?type=fast')


@app.route('/book_room/information', methods=['POST'])
def book_room_information():
    if (not current_user.is_authenticated):
        return render_template("layout/loginUser.html")

    if request.method == 'POST':
        customer_name_check = request.form.get('customer_name0')
        if customer_name_check:
            room_dict = session.get(ROOM_KEY)
            room = Room.query.get(room_dict.get('id'))
            num_people, max_people = utils.find_num_people_by_room(room)

            info_dict = session.get(PHIEU_KEY)
            if not info_dict:
                info_dict = {}

            info = {}
            for i in range(max_people):
                cus_name = request.form.get('customer_name' + str(i))
                cmnd = request.form.get('CMND' + str(i))
                addres = request.form.get('address' + str(i))
                loai_khach = request.form.get('loai_khach' + str(i))

                if cus_name:
                    info[str(i)] = {
                        'customer_name': cus_name,
                        'CMND': cmnd,
                        'address': addres,
                        'category_customer_id': loai_khach
                    }
            info_dict[str(room.id)] = info

            session[PHIEU_KEY] = info_dict

        room_dict = session.get(ROOM_KEY)
        room = Room.query.get(room_dict.get('id'))
        features = utils.get_features_room(room)

        return render_template('layout/thue_phong_infomation.html', features=features, room=room_dict)
    return redirect('/book_room?type=fast')


@app.route('/book_room/confirm', methods=['POST'])
def book_room_confirm():
    if (not current_user.is_authenticated):
        return render_template("layout/loginUser.html")

    if request.method == 'POST':
        return redirect('/book_room?type=fast')


@app.route('/book_room/finish', methods=['POST'])
def book_room_finish():
    if (not current_user.is_authenticated):
        return render_template("layout/loginUser.html")

    if request.method == 'POST':
        type = request.form.get('type')
        if type == 'online_fast':
            room_dict = session.get(ROOM_KEY)
            user_id = current_user.id
            room = Room.query.get(room_dict.get('id'))

            room_book = utils.insert_book_room(room_dict, user_id)
            info_dict = {}
            if session.get(PHIEU_KEY):
                if str(room.id) in session.get(PHIEU_KEY):
                    info_dict = session.get(PHIEU_KEY)[str(room.id)]

            if room_book:
                if info_dict:
                    utils.insert_book_information(room_book, info_dict)
                    temp = session.get(PHIEU_KEY)
                    temp.pop(str(room.id), None)
                    session[PHIEU_KEY] = temp

                utils.update_status_room(room, 'đầy')
                bill = utils.add_bill_dat_phong(room_book, user_id, room_dict, 'đã cọc')
                session.pop(PHIEU_KEY, None)
            return render_template('layout/thue_phong_nhanh_finnal.html')
        else:
            cart = session.get(CART_KEY)
            if not cart:
                cart = {}

            room_id = session.get(ROOM_KEY).get('id')

            msg = ''
            if str(room_id) in cart:
                msg = 'Phòng này đã được chọn'
            else:  # san pham chua bo vao gio
                cart[str(room_id)] = session.get(ROOM_KEY)
                msg = 'Đã thêm phòng vào trang thanh toán. Bạn có thể tiếp tục đặt phòng hoặc đến trang thanh toán để hoàn thiện đặt phòng'

            session[CART_KEY] = cart
            return render_template('layout/thue_phong_detail_final.html', msg=msg)

    return redirect('/book_room?type=fast')


# -------------------------END BOOK PHONG NHANH-------------------------------


# ----------------------BOOK DETAIL------------------------------
@app.route('/book_room/detail', methods=['POST'])
def book_room_detail():
    if not current_user.is_authenticated:
        return render_template("layout/loginUser.html")
    if request.method == 'POST':
        loai_phong = request.form.get('loai_phong')
        date_in = request.form.get('date_check_in')
        date_out = request.form.get('date_check_out')
        kieu_phong = request.form.get('Kiểu phòng')
        loai_giuong = request.form.get('Loại giường')
        view = request.form.get('Tầm nhìn')
        msg = ''
        if not utils.is_hop_le(loai_phong, kieu_phong, loai_giuong, view, date_in, date_out):
            msg = 'Dữ liệu không hợp lệ'
            return redirect('/book_room?type_book=online_detail&msg=' + msg)

        rooms = utils.get_list_room_arg(loai_phong, kieu_phong, loai_giuong, view)
        if len(rooms) != 0:
            room_dto_dict = utils.covert_room_bean(rooms, date_in, date_out, 'online_detail')
            session['list_current_room'] = room_dto_dict

        return render_template('layout/list_room.html', rooms=room_dto_dict)
    return redirect('/book_room?type=detail')


@app.route('/book_room/lap_phieu', methods=['GET'])
def book_room_lap_phieu():
    if not current_user.is_authenticated:
        return render_template("layout/loginUser.html")

    room_id = request.args.get('room_id')
    room_dto = session.get('list_current_room').get(str(room_id))
    session[ROOM_KEY] = room_dto
    room = Room.query.get(room_id)
    num_people, max_people = utils.find_num_people_by_room(room)
    count_people = max_people - num_people
    loai_khach = CategoryCustomer.query.all()
    return render_template('layout/phieu_thue_phong_information.html', num_people=num_people,
                           count_people=count_people, loai_khach=loai_khach)


@app.route("/api/add-item-cart", methods=['post'])
def add_to_cart():
    cart = session.get(CART_KEY)
    if not cart:
        cart = {}

    data = request.json

    room_id = str(data["room_id"])

    if room_id in cart:  # san pham da tung bo vao gio
        p = cart[room_id]
        p['msg'] = 'Phòng này đã được chọn'
    else:  # san pham chua bo vao gio
        cart[room_id] = session.get(ROOM_KEY)

    session[CART_KEY] = cart

    return jsonify(utils.cart_stats(cart))


@app.context_processor
def common_context():
    cart_stats = utils.cart_stats(session.get(CART_KEY))

    return {'cart_stats': cart_stats}


@app.route("/cart")
def cart():
    return render_template("layout/list_cart.html")


@app.route("/api/delete-cart-item/<room_id>", methods=['delete'])
def delete_cart_item(room_id):
    cart = session.get(CART_KEY)
    if cart:
        if str(room_id) in cart:
            del cart[room_id]
            session[CART_KEY] = cart

        phieu = session.get(PHIEU_KEY)
        if phieu:
            if str(room_id) in session.get(PHIEU_KEY):
                del phieu[room_id]
                session[PHIEU_KEY] = phieu

        return jsonify({
            "error_code": 200,
            "cart_stats": utils.cart_stats(cart)
        })

    return jsonify({
        "error_code": 404
    })


# ---------------------END BOOK DETAIL---------------------------------


# -------------------- THANH TOAN ONLINE ---------------------
@app.route('/api/pay', methods=['post'])
def pay():
    cart = session.get(CART_KEY)
    phieu = session.get(PHIEU_KEY)
    if cart:
        if utils.update_receipt_final(cart, phieu):
            del session[CART_KEY]

            return jsonify({
                "error_code": 200
            })

    return jsonify({
        "error_code": 404
    })


# ---------------------- ADMIN -------------------
@app.route('/admin/confirm_check_in', methods=['post'])
def admin_confirm_check_in():
    if not current_user.is_authenticated:
        return render_template("layout/loginUser.html")

    room_book_id = request.form.get('room_book_id')

    room = Room.query.get(RoomBook.query.get(room_book_id).room_id)
    numbers_people, max_people = utils.find_num_people_by_room(room)
    for i in range(max_people):
        info_if = request.form.get('book_info_id' + str(i))
        cus_name = request.form.get('customer_name' + str(i))
        cmnd = request.form.get('CMND' + str(i))
        addres = request.form.get('address' + str(i))
        loai_khach = request.form.get('loai_khach' + str(i))

        if info_if:
            info = BookInformation.query.get(info_if)
            info.customer_name = cus_name
            info.address = addres
            info.CMND = cmnd
            info.category_customer_id = loai_khach

            db.session.add(info)
            db.session.commit()
        else:
            if cus_name:
                info = BookInformation(customer_name=cus_name,
                                       CMND=cmnd,
                                       address=addres,
                                       room_book_id=room_book_id,
                                       category_customer_id=loai_khach)

                db.session.add(info)
                db.session.commit()

    list_info = BookInformation.query.filter(BookInformation.room_book_id == room_book_id).all()
    msg = ''
    if list_info:
        room_book = RoomBook.query.get(room_book_id)
        room_book.status = 'Đã nhận phòng'
        db.session.add(room_book)
        db.session.commit()

        bill = Bill.query.filter(Bill.room_book_id == room_book.id).all()
        if bill:
            utils.update_bill(bill[0])
        else:
            utils.add_new_bill(room_book)
        msg = 'Check in thành cồng'
    else:
        msg = 'check in thất bại'

    date_int = room_book.date.strftime("%d-%m-%Y")
    return redirect(
        '/admin/lapphieuthuephong?msg=' + msg + '&date_in=' + date_int + '&room_book_id=' + str(room_book_id))


@app.route("/api/update-confirm-bill/<bill_id>", methods=['put'])
def update_confirm_bill(bill_id):
    bill = Bill.query.get(bill_id)

    if bill:
        bill = utils.thanh_toan_hoa_don(bill)
        if bill:
            return jsonify({
                "error_code": 200,
            })
        else:
            return jsonify({
                "error_code": 404})

    return jsonify({
        "error_code": 404
})


@app.route("/userInformation")
def UserInformationControll():
    return render_template("layout/userInformation.html")


@app.route("/test")
def test():
    return render_template("layout/dat_phong_nhanh.html")


@app.route("/register/active")
def UserActiveControll():
    return render_template("layout/activeUser.html")


@app.route("/RegisterRoomFast")
def RegisterRoomFastControll():
    return render_template("layout/RegisterRoomFast.html")


@app.route("/RegisterRoomDetails")
def RegisterRoomDetailsControll():
    return render_template("layout/RegisterRoomDetails.html")


@app.route("/listMyRoom")
def ListRoomDetailsControll():
    return render_template("layout/listMyRoom.html")


@app.route("/MyRoomDetails")
def MyRoomDetailsFormControll():
    return render_template("layout/MyRoomDetails.html")


if __name__ == '__main__':
    app.run(debug=True)
