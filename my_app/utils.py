import string
from threading import Thread
from flask import render_template
from sqlalchemy import null
from my_app import app, db
import hashlib
from my_app.models import *
from flask_mail import Message
from my_app import mail
import random
import datetime


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_user(name, username, password, email):
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    roles_id = Role.query.filter(Role.name.contains('user')).all()[0].id
    user = User(role_id=roles_id,
                name=name,
                username=username,
                password=password,
                email=email,
                )

    db.session.add(user)
    try:
        send_active_account_email(user, app.config['MAIL_USERNAME'])
        db.session.commit()
        return user
    except:
        return null


def active_account(user):
    user.active = True
    db.session.add(user)
    db.session.commit()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user, admin_email):
    token = user.get_reset_password_token()
    send_email('[UTEHOTEL] Reset Your Password',
               sender=admin_email,
               recipients=[user.email],
               text_body=render_template("email/reset_password.txt",
                                         user=user, token=token),
               html_body=render_template("email/reset_password.html",
                                         user=user, token=token))


def send_active_account_email(user, admin_email):
    token = user.get_active_account_token()
    send_email('[UTEHOTEL] Active Account',
               sender=admin_email,
               recipients=[user.email],
               text_body=render_template("email/active_account.txt",
                                         user=user, token=token),
               html_body=render_template("email/active_account.html",
                                         user=user, token=token))


def get_list_loai_phong():
    list_loai_phong = CategoryRoom.query.all()
    return list_loai_phong


def get_list_phong_trong():
    list_room = Room.query.filter(Room.status == 'trong').all()
    return list_room


def find_room_by_arg(num_people=1, loai_phong='', loai_giuong='', view=''):
    list_room = Room.query.join(CategoryRoom).filter(
        Room.status == 'trống').filter(CategoryRoom.id == num_people).all()
    list_room_result = []
    msg = ''
    if len(list_room) != 0:
        for item in list_room:

            list_room_loaiphong = Room.query.join(CategoryRoom).join(TypeRoom).join(
                LabelRoom).join(
                GroupLabelRoom).add_columns().filter(
                GroupLabelRoom.group_name == 'Kiểu phòng').filter(LabelRoom.description == loai_phong).filter(
                Room.id == item.id).all()

            list_room_kieuphong = Room.query.join(CategoryRoom).join(TypeRoom).join(LabelRoom).join(
                GroupLabelRoom).filter(
                Room.id == item.id).filter(GroupLabelRoom.group_name == 'Loại giường').filter(
                LabelRoom.description == loai_giuong).all()

            list_room_view = Room.query.join(CategoryRoom).join(TypeRoom).join(LabelRoom).join(
                GroupLabelRoom).filter(
                Room.id == item.id).filter(GroupLabelRoom.group_name == 'Tầm nhìn').filter(
                LabelRoom.description == view).all()

            if len(list_room_view) != 0 and len(list_room_kieuphong) != 0 and len(list_room_loaiphong) != 0:
                list_room_result.append(list_room_view[0])
                list_room_kieuphong = []
                list_room_view = []
                list_room_loaiphong = []
    return list_room_result


def find_num_people_by_room(room):
    cate_room = \
        CategoryRoom.query.join(Room, Room.category_id == CategoryRoom.id).filter(Room.id == room.id).all()[0]
    return cate_room.number_people, cate_room.max_people


def get_features_room(room):
    results = []
    features = GroupLabelRoom.query.all()
    for feature in features:
        labels = LabelRoom.query.join(TypeRoom, LabelRoom.id == TypeRoom.label_id).join(Room,
                                                                                        TypeRoom.room_id == Room.id).join(
            GroupLabelRoom, GroupLabelRoom.id == LabelRoom.group_id).filter(
            GroupLabelRoom.group_name == feature.group_name).filter(
            Room.id == room.id).all()

        label_room = []
        for label in labels:
            label_room.append(label.description)
        value = ' '.join(label_room)
        dict_result = {}
        dict_result['name'] = feature.group_name
        dict_result['value'] = value
        results.append(dict_result)

    return results


def calculate_price_room_basic(room):
    basic_price = CategoryRoom.query.join(Room, Room.category_id == CategoryRoom.id).filter(Room.id == room.id).all()[
        0].price

    list_label_room = LabelRoom.query.join(TypeRoom).join(Room).filter(Room.id == room.id).all()
    percent = 0
    for label in list_label_room:
        percent = percent + label.percent

    return basic_price + basic_price * (percent / 100)


def sum_price_basic(date_in, date_out, price):
    date_check_in = datetime.datetime.strptime(date_in, '%Y-%m-%d').date()
    date_check_out = datetime.datetime.strptime(date_out, '%Y-%m-%d').date()
    compare_time = (date_check_out - date_check_in).days
    if (compare_time <= 0):
        compare_time = 1
    return price * compare_time


def tien_coc(sum_price, type_book):
    percent = TypeBook.query.filter(TypeBook.type == type_book).all()[0].percent_cost
    return sum_price * (percent/100)


def insert_book_room(room_dict, user_id):
    type = TypeBook.query.filter(TypeBook.type == room_dict.get('type_book')).all()[0]
    date_in = datetime.datetime.strptime(room_dict.get('date_in'), '%Y-%m-%d').date()

    room_book = RoomBook(date=date_in,
                         status='Chưa nhận phòng',
                         room_id=room_dict.get('id'),
                         user_id=user_id,
                         book_id=type.id
                         )

    db.session.add(room_book)
    try:
        db.session.commit()
        return room_book
    except:
        return null


def insert_book_information(room_book, info_dict):
    room_book_id = room_book.id
    room = Room.query.get(room_book.room_id)
    number_people, max_people = find_num_people_by_room(room)

    for i in range(max_people):
        item = info_dict.get(str(i))
        if item:
            book_information = BookInformation(customer_name=item.get('customer_name'),
                                               CMND=item.get('CMND'),
                                               address=item.get('address'),
                                               room_book_id=room_book_id,
                                               category_customer_id=item.get('category_customer_id')
                                               )

            db.session.add(book_information)
            db.session.commit()


def update_status_room(room):
    room.status = 'đầy'
    db.session.add(room)
    db.session.commit()


def add_bill_dat_phong(room_book, user_id, date_in, date_out, status):
    room = Room.query.get(room_book.room_id)
    price_basic = calculate_price_room_basic(room)
    sum_price = sum_price_basic(date_in, date_out, price_basic)

    type_book = TypeBook.query.filter(TypeBook.id == room_book.book_id).all()[0].type
    deposit = tien_coc(sum_price, type_book)

    bill = Bill(deposit=deposit,
                customer_id=user_id,
                room_book_id=room_book.id,
                status=status,
                costs=sum_price
                )

    db.session.add(bill)
    try:
        db.session.commit()
        return bill
    except:
        return null


def get_all_feature_room():
    results = []
    features = GroupLabelRoom.query.all()
    for feature in features:
        labels = LabelRoom.query.join(GroupLabelRoom).filter(
            GroupLabelRoom.group_name == feature.group_name).all()

        dict_result = {}
        dict_result['name'] = feature.group_name
        dict_result['value'] = labels
        results.append(dict_result)

    return results


def get_list_room_arg(loai_phong, kieu_phong, loai_giuong, tam_nhin):
    rooms = Room.query.join(CategoryRoom).filter(CategoryRoom.id == loai_phong).filter(Room.status=='trống').all()
    result = []
    for room in rooms:
        kieu_phong_room = Room.query.join(TypeRoom).join(LabelRoom).filter(LabelRoom.id == kieu_phong).filter(
            Room.id == room.id).all()
        loai_giuong_room = Room.query.join(TypeRoom).join(LabelRoom).filter(LabelRoom.id == loai_giuong).filter(
            Room.id == room.id).all()
        view_room = Room.query.join(TypeRoom).join(LabelRoom).filter(LabelRoom.id == tam_nhin).filter(
            Room.id == room.id).all()

        if len(kieu_phong_room) != 0 and len(loai_giuong_room) != 0 and len(view_room) != 0:
            result.append(view_room[0])
            kieu_phong_room=[]
            loai_giuong_room=[]
            view_room=[]

    return result

def covert_room_bean(rooms, date_in, date_out, type_book):

    result = {}
    for room in rooms:
        price = calculate_price_room_basic(room)
        features = get_features_room(room)
        sum_price = sum_price_basic(date_in, date_out, price)
        number_people, max_people = find_num_people_by_room(room)
        phi_coc = tien_coc(sum_price, type_book)
        room_dto = {
            'id': room.id,
            'name': room.name,
            'image': room.image,
            'status': room.status,
            'category_id': room.category_id,
            'date_in': date_in,
            'date_out': date_out,
            'price': price,
            'number_people': number_people,
            'type_book': type_book,
            'sum_price_basic': sum_price,
            'phi_coc': phi_coc
        }

        for item in features:
            room_dto[item.get('name')] =item.get('value')

        result[str(room.id)] = room_dto

    return result


def is_hop_le(loai_phong, kieu_phong, loai_giuong, tam_nhin, date_in, date_out):
    if (not loai_phong or not kieu_phong or not loai_giuong or not tam_nhin or not date_in or not date_out):
        return False

    date_check_in = datetime.datetime.strptime(date_in, '%Y-%m-%d').date()
    date_now  = datetime.datetime.now().date()
    compare_time = (date_check_in - date_now).days
    if compare_time < 0 or compare_time > 100:
        return False

    date_check_out = datetime.datetime.strptime(date_out, '%Y-%m-%d').date()
    compare_time = (date_check_out - date_check_in).days
    if compare_time < 0:
        return False
    return True


def is_book_fast(loai_phong, date_in):
    if (not loai_phong  or not date_in ):
        return False

    date_check_in = datetime.datetime.strptime(date_in, '%Y-%m-%d').date()
    date_now  = datetime.datetime.now().date()
    compare_time = (date_check_in - date_now).days
    if compare_time < 0 or compare_time > 100:
        return False

    return True


def cart_stats(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for p in cart.values():
            total_quantity += p["quantity"]
            total_amount += p["quantity"] * p["product_price"]

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }

