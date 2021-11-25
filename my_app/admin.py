from datetime import datetime

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect, request
from my_app import db, admin, utils
from my_app.models import Room, CategoryRoom, User, Role, CategoryCustomer, LabelRoom, RoomBook, TypeRoom, \
    BookInformation, TypeBook, Bill, GroupLabelRoom


class AuthenticatedView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.active == True:
            role_name = Role.query.get(current_user.role_id).name
            if role_name == 'admin':
                return True
        return False


class AuthenticatedView_Staff(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.active == True:
            role_name = Role.query.get(current_user.role_id).name
            if role_name == 'staff':
                return True
        return False


class RoomModelView_Staff(AuthenticatedView_Staff):
    can_export = True
    form_excluded_columns = ('room_book', 'typeRoom')
    can_view_details = True
    can_delete = False
    column_searchable_list = ('name',)


# -------------------View Admin-----------------------------

class RoomModelView(AuthenticatedView):
    can_export = True
    form_excluded_columns = ('room_book', 'typeRoom')
    can_view_details = True
    column_searchable_list = ('name',)


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
    column_searchable_list = ('user_id',)
    column_display_pk = True


class LabelRoomView(AuthenticatedView):
    form_excluded_columns = ('typeRoom')


class TypeRoomView(AuthenticatedView):
    pass


class BookInformationView(AuthenticatedView):
    can_export = True
    can_view_details = True
    column_searchable_list = ('room_book_id',)


class TypeBookView(AuthenticatedView):
    form_excluded_columns = ('room_book')


class GroupLabelRoomView(AuthenticatedView):
    form_excluded_columns = ('labelRoom')


class BillView(AuthenticatedView):
    can_export = True
    can_view_details = True
    column_searchable_list = ('customer_id', 'employee_id', 'datetime')


# -----------END VIEW ADMIN-----------------------------------------


# --------------- VIEW STAFF-------------------------------
class room_model_view_Staff(AuthenticatedView_Staff):
    can_export = True
    form_excluded_columns = ('room_book', 'typeRoom')
    can_view_details = True
    can_delete = False
    column_searchable_list = ('name',)


class room_book_view_staff(AuthenticatedView_Staff):
    form_excluded_columns = ('book_information', 'bill')
    can_export = True
    can_view_details = True
    column_searchable_list = ('user_id',)
    column_display_pk = True


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


# ------------- Add view Admin
admin.add_view(UserView(User, db.session, name='Người dùng', category='Quản lý người dùng'))
admin.add_view(RoleView(Role, db.session, name='Quyền', category='Quản lý người dùng'))
admin.add_view(CategoryCustomerView(CategoryCustomer, db.session, name='Loại khách', category='Quản lý người dùng'))
admin.add_view(RoomModelView(Room, db.session, name='Phòng', category='Quản lý phòng'))
admin.add_view(LabelRoomView(LabelRoom, db.session, name='Nhãn mô tả', category='Quản lý phòng'))
admin.add_view(TypeRoomView(TypeRoom, db.session, name='Đặc tính phòng', category='Quản lý phòng'))
admin.add_view(CategoryRoomView(CategoryRoom, db.session, name='Loại phòng', category='Quản lý phòng'))
admin.add_view(RoomBookView(RoomBook, db.session, name='Phiếu đặt phòng', category='Quản lý đặt phòng'))
admin.add_view(
    BookInformationView(BookInformation, db.session, name="Thông tin phiếu đặt phòng", category='Quản lý đặt phòng'))
admin.add_view(TypeBookView(TypeBook, db.session, name='Kiểu đặt phòng', category='Quản lý đặt phòng'))
admin.add_view(BillView(Bill, db.session, name='Hóa đơn', category='Thống kê'))
admin.add_view(GroupLabelRoomView(GroupLabelRoom, db.session, name='Loại nhãn phòng', category='Quản lý phòng'))

# admin.add_view(StatsView(name="Thong ke doanh thu"))

# --------------- Add view staff ---------------------
admin.add_view(
    room_model_view_Staff(Room, db.session, name='Phòng', category='Quản lí phòng', endpoint="view/staff/room"))
admin.add_view(
    room_book_view_staff(RoomBook, db.session, name='Danh sách phiếu thuê phòng', category='Quản lí đặt phòng',
                         endpoint="vew/staff/dsphieu"))


class AuthenticatedViewWithBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class ThongKeDoanhThu(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/ThongKeDoanhThu.html')


class BaoCaoMatDoSuDungPhong(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/BCMatDoDungPhong.html')


class LapPhieuThuePhong(AuthenticatedViewWithBaseView):
    @expose('/', methods=['GET'])
    def index(self):
        date_in = request.args.get('date_in')
        room_book_id = request.args.get('room_book_id')
        if room_book_id:
            msg = request.args.get('msg')
            room_book_infos = BookInformation.query.filter(BookInformation.room_book_id == room_book_id).all()
            room_id = RoomBook.query.get(room_book_id).room_id
            room = Room.query.get(room_id)

            numbers_people, max_people = utils.find_num_people_by_room(room)
            count_people = max_people - numbers_people
            loai_khach = CategoryCustomer.query.all()

            return self.render('admin/lap_phieu_thue_phong.html', num_people=numbers_people,
                           count_people=count_people, loai_khach=loai_khach, date_in=date_in,
                           room_book_infos=room_book_infos, room_id=room_id, room_book_id=room_book_id, msg=msg)
        return self.render('admin/lap_phieu_thue_phong.html', num_people=0, count_people=0)

class LapHoaDon(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/LapHoaDon.html')


class danh_sach_phong(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        rooms = Room.query.all()
        roomsdto = utils.covert_room_been_staff(rooms)
        return self.render('admin/danh_sach_phong.html', roomsdto=roomsdto)


class danh_sach_phong_dang_dat(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        room_books = RoomBook.query.filter(RoomBook.status == 'Chưa nhận phòng').all()
        roomdtos = utils.convert_room_book(room_books)
        return self.render('admin/ds_phong_dang_dat.html', rooms=roomdtos)


class danh_sach_hoa_don_chua_thanh_toan(AuthenticatedViewWithBaseView):
    @expose('/')
    def index(self):
        bills = Bill.query.filter(Bill.status != 'Đã thanh toán').all()
        return self.render('admin/ds_hoa_don_chua_thanh_toan.html', bills=bills)


admin.add_view(danh_sach_phong(name='Danh sách phòng', category='Quản lí phòng'))
admin.add_view(danh_sach_phong_dang_dat(name='Phiếu phòng đang đặt', category='Quản lí đặt phòng'))
admin.add_view(LapPhieuThuePhong(name='Lập phiếu thuê phòng', category='Quản lí đặt phòng'))
admin.add_view(LapHoaDon(name='Lập Hoá Đơn'))
admin.add_view(BaoCaoMatDoSuDungPhong(name='Báo cáo mật độ sử dụng phòng', category='Thống kê'))
admin.add_view(LogoutView(name="Đăng xuất"))
admin.add_view(ThongKeDoanhThu(name='Thống kê doanh thu', category='Thống kê'))
admin.add_view(danh_sach_hoa_don_chua_thanh_toan(name='Danh sách hóa đơn chưa thanh toán', category='Thanh toán'))
