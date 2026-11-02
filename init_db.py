import sys
import hashlib
import pymysql
from datetime import datetime, date, timedelta

sys.stdout.reconfigure(encoding='utf-8')

conn = pymysql.connect(host='localhost', user='root', password='16122003', charset='utf8mb4')
with conn.cursor() as cur:
    cur.execute("DROP DATABASE IF EXISTS dbks;")
    cur.execute("CREATE DATABASE dbks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
conn.commit()
conn.close()

from my_app import app, db
from my_app.models import (
    TaiKhoanNhanVien, TaiKhoanAdmin, LoaiPhong, Phong,
    LoaiKhach, Khach, TaiKhoanKhach, DatPhong, ChiTietThue,
    HoaDon, ThongSoQuyDinh, DanhGiaCuaKhach
)

with app.app_context():
    db.create_all()

    lk1 = LoaiKhach(MaLoaiKhach=1, LoaiKhach="Nội địa", HeSo=1.0)
    lk2 = LoaiKhach(MaLoaiKhach=2, LoaiKhach="Nước ngoài", HeSo=1.5)
    db.session.add_all([lk1, lk2])
    db.session.commit()

    lp1 = LoaiPhong(MaLoaiPhong=1, LoaiPhong="Standard", DonGia=150000)
    lp2 = LoaiPhong(MaLoaiPhong=2, LoaiPhong="Deluxe", DonGia=250000)
    lp3 = LoaiPhong(MaLoaiPhong=3, LoaiPhong="VIP", DonGia=400000)
    db.session.add_all([lp1, lp2, lp3])
    db.session.commit()

    qd = ThongSoQuyDinh(
        TenQuyDinh="Quy định khách sạn 2024",
        SoLuongPhong=10,
        giaPhong=150000.0,
        SoKhachTrongPhong=3,
        TyLePhuThu=0.25,
        HeSoKhachNuocNgoai=1.5,
        SoNgayDatTruocToiDa=28
    )
    db.session.add(qd)
    db.session.commit()

    rooms = [
        Phong(MaPhong=101, MaLoaiPhong=1, GhiChu="Phòng Standard 1 giường đôi, wifi, nước nóng", TinhTrang="FR", HinhAnh="https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=500"),
        Phong(MaPhong=102, MaLoaiPhong=1, GhiChu="Phòng Standard 2 giường đơn, thoáng mát", TinhTrang="FR", HinhAnh="https://images.unsplash.com/photo-1590490360182-c33d57733427?w=500"),
        Phong(MaPhong=103, MaLoaiPhong=1, GhiChu="Phòng Standard ban công đón nắng", TinhTrang="FR", HinhAnh="https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=500"),
        Phong(MaPhong=201, MaLoaiPhong=2, GhiChu="Phòng Deluxe view thành phố, minibar", TinhTrang="FR", HinhAnh="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=500"),
        Phong(MaPhong=202, MaLoaiPhong=2, GhiChu="Phòng Deluxe ban công rộng, bồn tắm", TinhTrang="FR", HinhAnh="https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=500"),
        Phong(MaPhong=203, MaLoaiPhong=2, GhiChu="Phòng Deluxe tiện nghi cao cấp", TinhTrang="FR", HinhAnh="https://images.unsplash.com/photo-1595576508898-0ad5c879a061?w=500"),
        Phong(MaPhong=301, MaLoaiPhong=3, GhiChu="Phòng VIP Tổng Thống có sảnh tiếp khách", TinhTrang="FR", HinhAnh="https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500"),
        Phong(MaPhong=302, MaLoaiPhong=3, GhiChu="Phòng VIP Hoàng Gia bồn sục jacuzzi", TinhTrang="FR", HinhAnh="https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=500")
    ]
    db.session.add_all(rooms)
    db.session.commit()

    pass_hash = str(hashlib.md5("123".encode("utf-8")).digest())

    nv = TaiKhoanNhanVien(emp_id=1, name="Nguyễn Văn Lễ Tân", username="nhanvien", password=pass_hash, active=True)
    admin_user = TaiKhoanNhanVien(emp_id=2, name="Quản Trị Viên (Admin)", username="admin", password=pass_hash, active=True)
    db.session.add_all([nv, admin_user])
    db.session.commit()

    admin_role = TaiKhoanAdmin(admin_id=1, emp_id=2)
    db.session.add(admin_role)
    db.session.commit()

    k1 = Khach(MaKhach=1, HoTen="Trần Thị Mai", MaLoaiKhach=1, CMND="079201014412", DiaChi="Quận 1, TP.HCM", SDT="0909123456", NgaySinh=date(1998, 4, 12))
    k2 = Khach(MaKhach=2, HoTen="David Johnson", MaLoaiKhach=2, CMND="987654321000", DiaChi="California, USA", SDT="0918987654", NgaySinh=date(1992, 9, 25))
    db.session.add_all([k1, k2])
    db.session.commit()

    tk1 = TaiKhoanKhach(MaKhach=1, username="khachhang", password=pass_hash)
    tk2 = TaiKhoanKhach(MaKhach=2, username="john_doe", password=pass_hash)
    db.session.add_all([tk1, tk2])
    db.session.commit()

    today = date.today()
    dp1 = DatPhong(
        HoTen="Lê Hoàng Nam",
        SDT="0933112233",
        CMND="079198765432",
        DiaChi="Bình Thạnh, TP.HCM",
        MaLoaiKhach=1,
        MaPhong=101,
        NgayDat=today,
        NgayNhan=today + timedelta(days=2),
        NgayTra=today + timedelta(days=4),
        SoLuongKhach=2,
        DaNhanPhong=False,
        DanhSachKhach='[{"stt": 1, "ho_ten": "Lê Hoàng Nam", "cmnd": "079198765432", "loai_khach": "1", "dia_chi": "Bình Thạnh, TP.HCM"}, {"stt": 2, "ho_ten": "Phạm Bích Ngọc", "cmnd": "079198765433", "loai_khach": "1", "dia_chi": "Bình Thạnh, TP.HCM"}]'
    )
    db.session.add(dp1)
    db.session.commit()

    now = datetime.now()
    thue1 = ChiTietThue(
        MaHopDong=1,
        MaPhong=102,
        MaKhach=1,
        HoTen="Trần Thị Mai",
        CMND="079201014412",
        DiaChi="Quận 1, TP.HCM",
        MaLoaiKhach=1,
        NgayBatDau=now - timedelta(days=6),
        NgayTraPhongDuKien=now - timedelta(days=3),
        SoNgayODuKien=3,
        SoLuong=2,
        CoKhachNuocNgoai=False,
        DanhSachKhach='[{"stt": 1, "ho_ten": "Trần Thị Mai", "cmnd": "079201014412", "loai_khach": "1", "dia_chi": "Quận 1, TP.HCM"}, {"stt": 2, "ho_ten": "Trần Văn An", "cmnd": "079201014413", "loai_khach": "1", "dia_chi": "Quận 1, TP.HCM"}]'
    )
    thue2 = ChiTietThue(
        MaHopDong=2,
        MaPhong=201,
        MaKhach=2,
        HoTen="David Johnson",
        CMND="987654321000",
        DiaChi="California, USA",
        MaLoaiKhach=2,
        NgayBatDau=now - timedelta(days=5),
        NgayTraPhongDuKien=now - timedelta(days=3),
        SoNgayODuKien=2,
        SoLuong=2,
        CoKhachNuocNgoai=True,
        DanhSachKhach='[{"stt": 1, "ho_ten": "David Johnson", "cmnd": "987654321000", "loai_khach": "2", "dia_chi": "California, USA"}, {"stt": 2, "ho_ten": "Sarah Johnson", "cmnd": "987654321001", "loai_khach": "2", "dia_chi": "California, USA"}]'
    )
    thue3 = ChiTietThue(
        MaHopDong=3,
        MaPhong=301,
        MaKhach=1,
        HoTen="Trần Thị Mai",
        CMND="079201014412",
        DiaChi="Quận 1, TP.HCM",
        MaLoaiKhach=1,
        NgayBatDau=now - timedelta(days=4),
        NgayTraPhongDuKien=now - timedelta(days=2),
        SoNgayODuKien=2,
        SoLuong=3,
        CoKhachNuocNgoai=False,
        DanhSachKhach='[{"stt": 1, "ho_ten": "Trần Thị Mai", "cmnd": "079201014412", "loai_khach": "1", "dia_chi": "Quận 1, TP.HCM"}, {"stt": 2, "ho_ten": "Trần Văn An", "cmnd": "079201014413", "loai_khach": "1", "dia_chi": "Quận 1, TP.HCM"}, {"stt": 3, "ho_ten": "Trần Thị Lan", "cmnd": "079201014414", "loai_khach": "1", "dia_chi": "Quận 1, TP.HCM"}]'
    )
    db.session.add_all([thue1, thue2, thue3])
    db.session.commit()

    hd1 = HoaDon(MaHopDong=1, NgayTraPhong=now - timedelta(days=3), SoNgayO=3, DonGia=150000, TyLePhuThu=0.0, HeSo=1.0, ThanhTien=450000)
    hd2 = HoaDon(MaHopDong=2, NgayTraPhong=now - timedelta(days=3), SoNgayO=2, DonGia=250000, TyLePhuThu=0.0, HeSo=1.5, ThanhTien=750000)
    hd3 = HoaDon(MaHopDong=3, NgayTraPhong=now - timedelta(days=2), SoNgayO=2, DonGia=400000, TyLePhuThu=0.25, HeSo=1.0, ThanhTien=1000000)
    db.session.add_all([hd1, hd2, hd3])
    db.session.commit()

    thue_active = ChiTietThue(
        MaHopDong=4,
        MaPhong=202,
        MaKhach=1,
        HoTen="Vũ Minh Tuấn",
        CMND="079200112233",
        DiaChi="Đà Nẵng",
        MaLoaiKhach=1,
        NgayBatDau=now - timedelta(days=1),
        NgayTraPhongDuKien=now + timedelta(days=2),
        SoNgayODuKien=3,
        SoLuong=3,
        CoKhachNuocNgoai=False,
        DanhSachKhach='[{"stt": 1, "ho_ten": "Vũ Minh Tuấn", "cmnd": "079200112233", "loai_khach": "1", "dia_chi": "Đà Nẵng"}, {"stt": 2, "ho_ten": "Vũ Minh Đức", "cmnd": "079200112234", "loai_khach": "1", "dia_chi": "Đà Nẵng"}, {"stt": 3, "ho_ten": "Nguyễn Mai Anh", "cmnd": "079200112235", "loai_khach": "1", "dia_chi": "Đà Nẵng"}]'
    )
    p202 = Phong.query.get(202)
    p202.TinhTrang = 'IU'
    db.session.add(thue_active)
    db.session.commit()

    dg1 = DanhGiaCuaKhach(MaPhong=101, MaKhach=1, NoiDung="Phòng rất sạch sẽ, yên tĩnh, phục vụ tận tình!", SoSao=5)
    dg2 = DanhGiaCuaKhach(MaPhong=201, MaKhach=2, NoiDung="Very nice hotel, friendly staff and great view!", SoSao=5)
    db.session.add_all([dg1, dg2])
    db.session.commit()

print("DATABASE INITIALIZED SUCCESSFULLY")
