from flask import redirect, session, request, url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from my_app import admin, db, utils
from my_app.models import (
    Phong, LoaiPhong, LoaiKhach, Khach, DatPhong,
    ChiTietThue, HoaDon, ThongSoQuyDinh, TaiKhoanNhanVien
)

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/dangnhap')

class PhongModelView(AuthenticatedView):
    column_list = ['MaPhong', 'LoaiPhong', 'TinhTrang', 'GhiChu']
    column_searchable_list = ['MaPhong', 'GhiChu']
    column_filters = ['TinhTrang']
    form_columns = ['MaLoaiPhong', 'GhiChu', 'TinhTrang', 'HinhAnh']

class LoaiPhongModelView(AuthenticatedView):
    column_list = ['MaLoaiPhong', 'LoaiPhong', 'DonGia']
    form_columns = ['LoaiPhong', 'DonGia']

class LoaiKhachModelView(AuthenticatedView):
    column_list = ['MaLoaiKhach', 'LoaiKhach', 'HeSo']
    form_columns = ['LoaiKhach', 'HeSo']

class ThongSoQuyDinhModelView(AuthenticatedView):
    column_list = ['TenQuyDinh', 'SoKhachTrongPhong', 'TyLePhuThu', 'HeSoKhachNuocNgoai', 'SoNgayDatTruocToiDa']
    form_columns = ['TenQuyDinh', 'SoKhachTrongPhong', 'TyLePhuThu', 'HeSoKhachNuocNgoai', 'SoNgayDatTruocToiDa']

class DatPhongModelView(AuthenticatedView):
    column_list = ['MaDatPhong', 'HoTen', 'SDT', 'MaPhong', 'NgayNhan', 'NgayTra', 'SoLuongKhach', 'DaNhanPhong']
    column_searchable_list = ['HoTen', 'SDT', 'CMND']

class ChiTietThueModelView(AuthenticatedView):
    column_list = ['MaHopDong', 'MaPhong', 'HoTen', 'NgayBatDau', 'SoNgayODuKien', 'SoLuong', 'CoKhachNuocNgoai']
    column_searchable_list = ['HoTen', 'CMND']

class HoaDonModelView(AuthenticatedView):
    column_list = ['MaHopDong', 'NgayTraPhong', 'SoNgayO', 'DonGia', 'TyLePhuThu', 'HeSo', 'ThanhTien']

class StatsView(BaseView):
    @expose('/')
    def index(self):
        thang = request.args.get('thang')
        nam = request.args.get('nam')
        data = utils.bao_cao_doanh_thu_thang(thang=thang, nam=nam)
        return self.render('admin/LapBaoCaoThang.html', data=data)

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

class MatDoView(BaseView):
    @expose('/')
    def index(self):
        thang = request.args.get('thang')
        nam = request.args.get('nam')
        data = utils.bao_cao_mat_do_thang(thang=thang, nam=nam)
        return self.render('admin/BaoCaoMatDo.html', data=data)

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        session.pop('khach', None)
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(PhongModelView(Phong, db.session, name='Danh mục phòng'))
admin.add_view(LoaiPhongModelView(LoaiPhong, db.session, name='Loại phòng'))
admin.add_view(LoaiKhachModelView(LoaiKhach, db.session, name='Loại khách'))
admin.add_view(ThongSoQuyDinhModelView(ThongSoQuyDinh, db.session, name='Thay đổi quy định'))
admin.add_view(DatPhongModelView(DatPhong, db.session, name='Phiếu đặt phòng'))
admin.add_view(ChiTietThueModelView(ChiTietThue, db.session, name='Phiếu thuê phòng'))
admin.add_view(HoaDonModelView(HoaDon, db.session, name='Hóa đơn'))
admin.add_view(StatsView(name='Báo cáo doanh thu'))
admin.add_view(MatDoView(name='Báo cáo mật độ'))
admin.add_view(LogoutView(name='Đăng xuất'))
