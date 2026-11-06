from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from my_app import db

class TaiKhoanNhanVien(db.Model, UserMixin):
    emp_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    taiKhoanAdmin = relationship('TaiKhoanAdmin', backref='taiKhoanNhanVien', lazy=True)

    def __str__(self):
        return self.name

    def get_id(self):
        return f"nv_{self.emp_id}"

    def is_active(self):
        return self.active

    def get_username(self):
        return self.username

    def get_urole(self):
        return 'NhanVien'

    @property
    def is_admin(self):
        return bool(self.taiKhoanAdmin and len(self.taiKhoanAdmin) > 0)

class TaiKhoanAdmin(db.Model):
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(Integer, ForeignKey('tai_khoan_nhan_vien.emp_id'), nullable=False)

    def __str__(self):
        return str(self.admin_id)

class LoaiPhong(db.Model):
    MaLoaiPhong = Column(Integer, primary_key=True, autoincrement=True)
    LoaiPhong = Column(String(50), nullable=False)
    DonGia = Column(Integer, nullable=False)
    phong = relationship('Phong', backref='LoaiPhong', lazy=True)

    def __str__(self):
        return str(self.LoaiPhong)

class Phong(db.Model):
    MaPhong = Column(Integer, primary_key=True, autoincrement=True)
    MaLoaiPhong = Column(Integer, ForeignKey('loai_phong.MaLoaiPhong'), nullable=False)
    GhiChu = Column(String(255), nullable=True)
    TinhTrang = Column(String(10), default='FR', nullable=False)
    HinhAnh = Column(String(255), nullable=True)

    chiTietThue = relationship('ChiTietThue', backref='phong', lazy=True)
    danhGia = relationship('DanhGiaCuaKhach', backref='phong', lazy=True)
    datPhong = relationship('DatPhong', backref='phong', lazy=True)

    def __str__(self):
        return str(self.MaPhong)

class LoaiKhach(db.Model):
    MaLoaiKhach = Column(Integer, primary_key=True, autoincrement=True)
    LoaiKhach = Column(String(50), nullable=False)
    HeSo = Column(Float, default=1.0)
    khach = relationship('Khach', backref='LoaiKhach', lazy=True)

    def __str__(self):
        return self.LoaiKhach

class Khach(db.Model):
    MaKhach = Column(Integer, primary_key=True, autoincrement=True)
    MaLoaiKhach = Column(Integer, ForeignKey('loai_khach.MaLoaiKhach'), nullable=False)
    HoTen = Column(String(100), default='')
    CMND = Column(String(20), nullable=False)
    DiaChi = Column(String(255), nullable=False)
    SDT = Column(String(20), nullable=True)
    NgaySinh = Column(Date, nullable=True)

    chiTietThue = relationship('ChiTietThue', backref='khach', lazy=True)
    danhGia = relationship('DanhGiaCuaKhach', backref='khach', lazy=True)
    taiKhoan = relationship('TaiKhoanKhach', backref='khach', uselist=False, lazy=True)

    def __str__(self):
        return self.HoTen if self.HoTen else str(self.MaKhach)

class TaiKhoanKhach(db.Model, UserMixin):
    MaKhach = Column(Integer, ForeignKey('khach.MaKhach'), primary_key=True, nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    def get_id(self):
        return f"kh_{self.MaKhach}"

    def is_active(self):
        return True

    def get_username(self):
        return self.username

    def get_urole(self):
        return 'Khach'

    @property
    def name(self):
        return self.khach.HoTen if (self.khach and self.khach.HoTen) else self.username

    @property
    def is_admin(self):
        return False

class DatPhong(db.Model):
    MaDatPhong = Column(Integer, primary_key=True, autoincrement=True)
    HoTen = Column(String(100), nullable=False)
    SDT = Column(String(20), nullable=False)
    CMND = Column(String(20), nullable=False)
    DiaChi = Column(String(255), nullable=False)
    MaLoaiKhach = Column(Integer, ForeignKey('loai_khach.MaLoaiKhach'), default=1)
    MaPhong = Column(Integer, ForeignKey('phong.MaPhong'), nullable=False)
    NgayDat = Column(Date, default=datetime.utcnow)
    NgayNhan = Column(Date, nullable=False)
    NgayTra = Column(Date, nullable=False)
    SoLuongKhach = Column(Integer, default=1)
    DaNhanPhong = Column(Boolean, default=False)
    DanhSachKhach = Column(String(2000), default='[]')

    loaiKhach = relationship('LoaiKhach', backref='danhSachDat')

    def __str__(self):
        return str(self.MaDatPhong)

class ChiTietThue(db.Model):
    MaHopDong = Column(Integer, primary_key=True, autoincrement=True)
    MaPhong = Column(Integer, ForeignKey('phong.MaPhong'), nullable=False)
    MaKhach = Column(Integer, ForeignKey('khach.MaKhach'), nullable=True)
    HoTen = Column(String(100), default='')
    CMND = Column(String(20), default='')
    DiaChi = Column(String(255), default='')
    MaLoaiKhach = Column(Integer, default=1)
    NgayBatDau = Column(DateTime, default=datetime.now, nullable=False)
    NgayTraPhongDuKien = Column(DateTime, nullable=True)
    SoNgayODuKien = Column(Integer, default=1)
    SoLuong = Column(Integer, default=1)
    CoKhachNuocNgoai = Column(Boolean, default=False)
    DanhSachKhach = Column(String(2000), default='[]')
    MaDatPhong = Column(Integer, nullable=True)

    hopDong = relationship('HoaDon', backref='ChiTietThue', uselist=False, lazy=True)

    def __str__(self):
        return str(self.MaHopDong)

class HoaDon(db.Model):
    MaHopDong = Column(Integer, ForeignKey('chi_tiet_thue.MaHopDong'), primary_key=True)
    NgayTraPhong = Column(DateTime, default=datetime.now, nullable=False)
    SoNgayO = Column(Integer, default=1)
    DonGia = Column(Integer, default=0)
    TyLePhuThu = Column(Float, default=0.0)
    HeSo = Column(Float, default=1.0)
    ThanhTien = Column(Integer, nullable=False)

    def __str__(self):
        return str(self.MaHopDong)

class ThongSoQuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenQuyDinh = Column(String(100), default='Quy định chung')
    SoLuongPhong = Column(Integer, default=10)
    giaPhong = Column(Float, default=200000.0)
    SoKhachTrongPhong = Column(Integer, default=3)
    TyLePhuThu = Column(Float, default=0.25)
    HeSoKhachNuocNgoai = Column(Float, default=1.5)
    SoNgayDatTruocToiDa = Column(Integer, default=28)
    loai_phong_id = Column(Integer, ForeignKey('loai_phong.MaLoaiPhong'), nullable=True)

    loai_phong = relationship('LoaiPhong', backref='thong_so_quy_dinh')

    @property
    def GiaTri(self):
        return self.HeSoKhachNuocNgoai

    def __str__(self):
        return self.TenQuyDinh

class DanhGiaCuaKhach(db.Model):
    MaDanhGia = Column(Integer, primary_key=True, autoincrement=True)
    MaPhong = Column(Integer, ForeignKey('phong.MaPhong'), nullable=False)
    MaKhach = Column(Integer, ForeignKey('khach.MaKhach'), nullable=False)
    NgayBatDau = Column(DateTime, default=datetime.now, nullable=False)
    NoiDung = Column(String(255), nullable=False)
    SoSao = Column(Integer, default=5)

    def __str__(self):
        return str(self.MaDanhGia)
