from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect
from my_app import db, admin
from my_app.models import Room, CategoryRoom, User, Role, CategoryCustomer, LabelRoom, RoomBook, TypeRoom, \
    BookInformation, TypeBook, Bill, GroupLabelRoom


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated



class RoomModelView(AuthenticatedView):
    can_export = True
    form_excluded_columns = ('room_book', 'typeRoom')
    can_view_details = True
    column_searchable_list = ('name', )

class CategoryRoomView(AuthenticatedView):
    form_excluded_columns = ('room')

class UserView(AuthenticatedView):
    form_excluded_columns = ('room_book', 'billcus', 'billemp')
    column_default_sort = 'name'
    can_view_details = True
    column_searchable_list = ('name', 'email')
    column_sortable_list = ('name',)

class RoleView(AuthenticatedView):
    form_excluded_columns = ('user')

class CategoryCustomerView(AuthenticatedView):
    form_excluded_columns = ('book_information')

class RoomBookView(AuthenticatedView):
    form_excluded_columns = ('book_information', 'bill')
    can_export = True
    can_view_details = True
    column_searchable_list = ('user_id', )
    column_display_pk = True


class LabelRoomView(AuthenticatedView):
    form_excluded_columns = ('typeRoom')

class TypeRoomView(AuthenticatedView):
    pass

class BookInformationView(AuthenticatedView):
    can_export = True
    can_view_details = True
    column_searchable_list = ('room_book_id', )

class TypeBookView(AuthenticatedView):
    form_excluded_columns = ('room_book')

class GroupLabelRoomView(AuthenticatedView):
    form_excluded_columns = ('labelRoom')


class BillView(AuthenticatedView):
    can_export = True
    can_view_details = True
    column_searchable_list = ('customer_id', 'employee_id', 'datetime')






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

admin.add_view(UserView(User, db.session,  name = 'Người dùng' , category='Quản lý người dùng'))
admin.add_view(RoleView(Role, db.session , name = 'Quyền', category='Quản lý người dùng'))
admin.add_view(CategoryCustomerView(CategoryCustomer, db.session , name = 'Loại khách', category='Quản lý người dùng'))
admin.add_view(RoomModelView(Room, db.session, name='Phòng', category='Quản lý phòng' ))
admin.add_view(LabelRoomView(LabelRoom, db.session, name='Nhãn mô tả', category='Quản lý phòng'))
admin.add_view(TypeRoomView(TypeRoom, db.session, name ='Đặc tính phòng', category='Quản lý phòng'))
admin.add_view(CategoryRoomView(CategoryRoom, db.session, name='Loại phòng', category='Quản lý phòng'))
admin.add_view(RoomBookView(RoomBook, db.session , name='Phiếu đặt phòng', category='Quản lý đặt phòng'))
admin.add_view(BookInformationView(BookInformation, db.session, name = "Thông tin phiếu đặt phòng", category='Quản lý đặt phòng'))
admin.add_view(TypeBookView(TypeBook, db.session, name = 'Kiểu đặt phòng', category='Quản lý đặt phòng'))
admin.add_view(BillView(Bill, db.session, name = 'Hóa đơn', category='Thống kê'))
admin.add_view(GroupLabelRoomView(GroupLabelRoom, db.session, name='Loại nhãn phòng', category='Quản lý phòng'))
# admin.add_view(StatsView(name="Thong ke doanh thu"))



class AuthenticatedViewWithBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class ThongKeDoanhThu(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/ThongKeDoanhThu.html')



admin.add_view(ThongKeDoanhThu(name='Thống kê doanh thu', category='Thống kê'))

class BaoCaoMatDoSuDungPhong(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/BCMatDoDungPhong.html')


admin.add_view(BaoCaoMatDoSuDungPhong(name='Báo cáo mật độ sữ dụng phòng', category='Thống kê'))

admin.add_view(LogoutView(name="Đăng xuất"))


class LapPhieuThuePhong(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/LapPhieuThuePhong.html')


admin.add_view(LapPhieuThuePhong(name='Lập phiếu thuê phòng'))

class LapHoaDon(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/LapHoaDon.html')


admin.add_view(LapHoaDon(name='Lập Hoá Đơn'))