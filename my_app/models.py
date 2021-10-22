from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from my_app import db
from datetime import datetime


class Role(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    user = relationship('User', backref="role", lazy=True)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    joined_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
    name = Column(String(80), nullable=False)
    email = Column(String(50), nullable = False)
    address = Column(String(100))
    phone = Column(String(11))
    image = Column(String(120))
    birthdate = Column(DateTime)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)
    room_book = relationship('RoomBook', backref="User_room", lazy=True)
    billcus = relationship('Bill', backref='User_bill', foreign_keys='Bill.customer_id', lazy=True)
    billemp = relationship('Bill', backref='User_emp', foreign_keys='Bill.employee_id', lazy=True)


    def __str__(self):
        return self.username



class CategoryCustomer(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20), nullable = False)
    percent = Column(Integer, default=0)
    book_information = relationship('BookInformation', backref="categoryCustomer", lazy=True)

    def __str__(self):
        return self.type

class CategoryRoom(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_people = Column(Integer, unique=True, nullable = False)
    max_people = Column(Integer)
    surcharge = Column(Integer)
    room = relationship('Room', backref="categoryRoom", lazy=True)

    def __str__(self):
        return str(self.number_people)


class LabelRoom(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(60), nullable = False)
    percent = Column(Float, default=0)
    typeRoom = relationship('TypeRoom', backref="labelRoom", lazy=True)

    def __str__(self):
        return self.description


class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    image = Column(String(100), nullable=True)
    status = Column(String(20))
    category_id = Column(Integer, ForeignKey(CategoryRoom.id), nullable=False)
    room_book = relationship('RoomBook', backref="room", lazy=True)
    typeRoom = relationship('TypeRoom', backref="room", lazy=True)

    def __str__(self):
        return self.name

class TypeBook(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20), nullable = False)
    percent_cost = Column(Float, default=0)
    room_book = relationship('RoomBook', backref="typeBook", lazy=True)

    def __str__(self):
        return self.type


class RoomBook(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    status = Column(String(20))
    room_id = Column(Integer, ForeignKey(Room.id))
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_id = Column(Integer, ForeignKey(TypeBook.id), nullable=False)
    book_information = relationship('BookInformation', backref="roomBook", lazy=True)
    bill = relationship('Bill', backref="roomBook", lazy=True)

    def __str__(self):
        return str(self.id)

class BookInformation(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(60))
    CMND = Column(String(10))
    address = Column(String(50))
    room_book_id = Column(Integer, ForeignKey(RoomBook.id), nullable=False)
    category_customer_id = Column(Integer, ForeignKey(CategoryCustomer.id), nullable=False)

    def __str__(self):
        return str(self.id)

class TypeRoom(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    label_id = Column(Integer, ForeignKey(LabelRoom.id), nullable=False)

    def __str__(self):
        return str(self.id)


class Bill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    costs = Column(Float, default=0)
    deposit = Column(Float, default=0)
    datetime = Column(DateTime, default=datetime.now())
    room_number_date = Column(Integer)
    customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    employee_id = Column(Integer, ForeignKey(User.id))
    room_book_id = Column(Integer, ForeignKey(RoomBook.id))

    def __str__(self):
        return str(self.id)


if __name__ == '__main__':
    db.create_all()



