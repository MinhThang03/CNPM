from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect
from my_app import db, admin
from my_app.models import Room, CategoryRoom, User, Role, CategoryCustomer, LabelRoom, RoomBook, TypeRoom, BookInformation, TypeBook, Bill


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated



class RoomModelView(AuthenticatedView):
    can_export = True

class CategoryRoomView(AuthenticatedView):
    form_excluded_columns = ('room')

class UserView(AuthenticatedView):
    form_excluded_columns = ('room_book', 'billcus', 'billemp')
    column_default_sort = 'name'

class RoleView(AuthenticatedView):
    form_excluded_columns = ('user')

class CategoryCustomerView(AuthenticatedView):
    form_excluded_columns = ('book_information')

class RoomBookView(AuthenticatedView):
    form_excluded_columns = ('book_information', 'bill')
    can_export = True

class LabelRoomView(AuthenticatedView):
    form_excluded_columns = ('typeRoom')

class TypeRoomView(AuthenticatedView):
    pass

class BookInformationView(AuthenticatedView):
    can_export = True

class TypeBookView(AuthenticatedView):
    form_excluded_columns = ('room_book')

class BillView(AuthenticatedView):
    can_export = True





# class StatsView(BaseView):
#     @expose("/")
#     def index(self):
#         return self.render("admin/stats.html")
#
#     def is_accessible(self):
#         return current_user.is_authenticated


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(RoomModelView(Room, db.session))
admin.add_view(CategoryRoomView(CategoryRoom, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(CategoryCustomerView(CategoryCustomer, db.session))
admin.add_view(RoomBookView(RoomBook, db.session))
admin.add_view(LabelRoomView(LabelRoom, db.session))
admin.add_view(TypeRoomView(TypeRoom, db.session))
admin.add_view(BookInformationView(BookInformation, db.session))
admin.add_view(TypeBookView(TypeBook, db.session))
admin.add_view(BillView(Bill, db.session))
# admin.add_view(RoomModelView(Room, db.session))
# admin.add_view(StatsView(name="Thong ke doanh thu"))
admin.add_view(LogoutView(name="Dang xuat"))