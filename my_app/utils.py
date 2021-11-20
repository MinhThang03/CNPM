import string
from threading import Thread
from flask import render_template
from sqlalchemy import null
from my_app import app, db
import hashlib
from my_app.models import User, Role
from flask_mail import Message
from my_app import mail
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_user(name, username, password, email):
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    # code_active = id_generator()
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
