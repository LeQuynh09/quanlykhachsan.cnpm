from datetime import datetime, date, timedelta
import hashlib
import json
from sqlalchemy import func, extract
from my_app import db
from my_app.models import (
    Phong, LoaiPhong, Khach, LoaiKhach, ChiTietThue, HoaDon,
    ThongSoQuyDinh, DatPhong, TaiKhoanKhach, TaiKhoanNhanVien
)

def get_quy_dinh():
    qd = ThongSoQuyDinh.query.first()
    if not qd:
        qd = ThongSoQuyDinh(
            SoLuongPhong=10,
            giaPhong=200000.0,
            SoKhachTrongPhong=3,
            TyLePhuThu=0.25,
            HeSoKhachNuocNgoai=1.5,
            SoNgayDatTruocToiDa=28
        )
        db.session.add(qd)
        db.session.commit()
    return qd

def get_loai_phong(ma_loai=None):
    if ma_loai:
        return LoaiPhong.query.filter_by(MaLoaiPhong=ma_loai).all()
    return LoaiPhong.query.all()

def get_loai_khach():
    return LoaiKhach.query.all()

def get_phong(kw=None, ma_loai_phong=None, tinh_trang=None, min_price=None, max_price=None, page=1, page_size=8):
    query = Phong.query.join(LoaiPhong)

    if kw:
        query = query.filter(Phong.MaPhong.like(f"%{kw}%") | Phong.GhiChu.like(f"%{kw}%"))

    if ma_loai_phong:
        query = query.filter(Phong.MaLoaiPhong == ma_loai_phong)

    if tinh_trang:
        query = query.filter(Phong.TinhTrang == tinh_trang)

    if min_price:
        query = query.filter(LoaiPhong.DonGia >= min_price)

    if max_price:
        query = query.filter(LoaiPhong.DonGia <= max_price)

    total = query.count()
    items = query.order_by(Phong.MaPhong).offset((page - 1) * page_size).limit(page_size).all()
    return items, total

def get_phong_by_id(ma_phong):
    return Phong.query.get(ma_phong)

def check_phong_trong(ma_phong):
    p = Phong.query.get(ma_phong)
    return p is not None and p.TinhTrang == 'FR'

def dat_phong(ho_ten, sdt, cmnd, dia_chi, ma_loai_khach, ma_phong, ngay_nhan, ngay_tra, so_luong_khach=1, danh_sach_khach=None):
    qd = get_quy_dinh()
    today = date.today()

    if isinstance(ngay_nhan, str):
        ngay_nhan = datetime.strptime(ngay_nhan, "%Y-%m-%d").date()
    if isinstance(ngay_tra, str):
        ngay_tra = datetime.strptime(ngay_tra, "%Y-%m-%d").date()

    if ngay_nhan < today:
        return None, "Ngày nhận phòng không được ở quá khứ!"

    if (ngay_nhan - today).days > qd.SoNgayDatTruocToiDa:
        return None, f"Thời điểm nhận phòng không được quá {qd.SoNgayDatTruocToiDa} ngày kể từ thời điểm đặt!"

    if ngay_tra <= ngay_nhan:
        return None, "Ngày trả phòng phải sau ngày nhận phòng!"

    if int(so_luong_khach) > qd.SoKhachTrongPhong:
        return None, f"Mỗi phòng chỉ được ở tối đa {qd.SoKhachTrongPhong} khách!"

    p = Phong.query.get(ma_phong)
    if not p:
        return None, "Phòng không tồn tại!"

    if p.TinhTrang == 'IU':
        return None, "Phòng hiện đang có khách thuê!"

    ds_khach_str = json.dumps(danh_sach_khach or [], ensure_ascii=False)

    dp = DatPhong(
        HoTen=ho_ten,
        SDT=sdt,
        CMND=cmnd,
        DiaChi=dia_chi,
        MaLoaiKhach=ma_loai_khach,
        MaPhong=ma_phong,
        NgayDat=today,
        NgayNhan=ngay_nhan,
        NgayTra=ngay_tra,
        SoLuongKhach=int(so_luong_khach),
        DanhSachKhach=ds_khach_str
    )
    db.session.add(dp)
    db.session.commit()
    return dp, None

def tim_dat_phong(kw):
    if not kw:
        return []
    return DatPhong.query.filter(
        (DatPhong.HoTen.like(f"%{kw}%")) | (DatPhong.CMND.like(f"%{kw}%")) | (DatPhong.SDT.like(f"%{kw}%")),
        DatPhong.DaNhanPhong == False
    ).all()

def lap_phieu_thue(ma_phong, ho_ten, cmnd, dia_chi, ma_loai_khach, ngay_bat_dau, so_ngay, so_luong_khach=1, danh_sach_khach=None, ma_dat_phong=None):
    qd = get_quy_dinh()

    if int(so_luong_khach) > qd.SoKhachTrongPhong:
        return None, f"Mỗi phòng chỉ được ở tối đa {qd.SoKhachTrongPhong} khách!"

    p = Phong.query.get(ma_phong)
    if not p:
        return None, "Phòng không tồn tại!"

    if p.TinhTrang == 'IU':
        return None, "Phòng đang có khách ở, không thể lập phiếu thuê!"

    if isinstance(ngay_bat_dau, str):
        ngay_bat_dau = datetime.strptime(ngay_bat_dau, "%Y-%m-%d")

    ngay_tra_du_kien = ngay_bat_dau + timedelta(days=int(so_ngay))

    co_nuoc_ngoai = int(ma_loai_khach) == 2
    if danh_sach_khach:
        for k in danh_sach_khach:
            if str(k.get('loai_khach', '')) in ['2', 'Nước ngoài', 'NuocNgoai']:
                co_nuoc_ngoai = True
                break

    kh = Khach.query.filter_by(CMND=cmnd).first()
    if not kh:
        kh = Khach(HoTen=ho_ten, CMND=cmnd, DiaChi=dia_chi, MaLoaiKhach=ma_loai_khach)
        db.session.add(kh)
        db.session.commit()
    else:
        kh.HoTen = ho_ten
        kh.DiaChi = dia_chi
        kh.MaLoaiKhach = ma_loai_khach
        db.session.commit()

    ds_khach_str = json.dumps(danh_sach_khach or [], ensure_ascii=False)

    ct = ChiTietThue(
        MaPhong=ma_phong,
        MaKhach=kh.MaKhach,
        HoTen=ho_ten,
        CMND=cmnd,
        DiaChi=dia_chi,
        MaLoaiKhach=ma_loai_khach,
        NgayBatDau=ngay_bat_dau,
        NgayTraPhongDuKien=ngay_tra_du_kien,
        SoNgayODuKien=int(so_ngay),
        SoLuong=int(so_luong_khach),
        CoKhachNuocNgoai=co_nuoc_ngoai,
        DanhSachKhach=ds_khach_str,
        MaDatPhong=ma_dat_phong
    )
    p.TinhTrang = 'IU'

    if ma_dat_phong:
        dp = DatPhong.query.get(ma_dat_phong)
        if dp:
            dp.DaNhanPhong = True

    db.session.add(ct)
    db.session.commit()
    return ct, None

def get_danh_sach_thue_chua_thanh_toan():
    return ChiTietThue.query.filter(
        ~ChiTietThue.MaHopDong.in_(db.session.query(HoaDon.MaHopDong))
    ).all()

def tinh_tien_chi_tiet(ma_hop_dong):
    ct = ChiTietThue.query.get(ma_hop_dong)
    if not ct:
        return None

    qd = get_quy_dinh()
    don_gia = ct.phong.LoaiPhong.DonGia

    now = datetime.now()
    so_ngay = (now.date() - ct.NgayBatDau.date()).days
    if so_ngay <= 0:
        so_ngay = 1

    ty_le_phu_thu = 0.0
    if ct.SoLuong >= 3:
        ty_le_phu_thu = qd.TyLePhuThu

    he_so = 1.0
    if ct.CoKhachNuocNgoai or ct.MaLoaiKhach == 2:
        he_so = qd.HeSoKhachNuocNgoai

    thanh_tien = int(don_gia * so_ngay * (1.0 + ty_le_phu_thu) * he_so)

    return {
        "hop_dong": ct,
        "so_ngay": so_ngay,
        "don_gia": don_gia,
        "ty_le_phu_thu": ty_le_phu_thu,
        "phu_thu_phan_tram": int(ty_le_phu_thu * 100),
        "he_so": he_so,
        "thanh_tien": thanh_tien
    }

def thanh_toan(ma_hop_dong):
    data = tinh_tien_chi_tiet(ma_hop_dong)
    if not data:
        return None, "Không tìm thấy hợp đồng thuê!"

    hd = HoaDon.query.get(ma_hop_dong)
    if hd:
        return hd, "Hợp đồng đã được thanh toán trước đó!"

    ct = data["hop_dong"]
    hd = HoaDon(
        MaHopDong=ma_hop_dong,
        NgayTraPhong=datetime.now(),
        SoNgayO=data["so_ngay"],
        DonGia=data["don_gia"],
        TyLePhuThu=data["ty_le_phu_thu"],
        HeSo=data["he_so"],
        ThanhTien=data["thanh_tien"]
    )
    ct.phong.TinhTrang = 'FR'
    db.session.add(hd)
    db.session.commit()
    return hd, None

def bao_cao_doanh_thu_thang(thang=None, nam=None):
    now = datetime.now()
    thang = int(thang) if thang else now.month
    nam = int(nam) if nam else now.year

    ds_loai = LoaiPhong.query.all()
    loai_dict = {lp.MaLoaiPhong: {"ten": lp.LoaiPhong, "doanh_thu": 0, "luot_thue": 0} for lp in ds_loai}

    hoa_dons = db.session.query(HoaDon, ChiTietThue, Phong).join(
        ChiTietThue, HoaDon.MaHopDong == ChiTietThue.MaHopDong
    ).join(
        Phong, ChiTietThue.MaPhong == Phong.MaPhong
    ).filter(
        extract('month', HoaDon.NgayTraPhong) == thang,
        extract('year', HoaDon.NgayTraPhong) == nam
    ).all()

    tong_doanh_thu = 0
    for hd, ct, p in hoa_dons:
        ma_lp = p.MaLoaiPhong
        if ma_lp in loai_dict:
            loai_dict[ma_lp]["doanh_thu"] += hd.ThanhTien
            loai_dict[ma_lp]["luot_thue"] += 1
            tong_doanh_thu += hd.ThanhTien

    ket_qua = []
    stt = 1
    for ma_lp, v in loai_dict.items():
        dt = v["doanh_thu"]
        ty_le = round((dt / tong_doanh_thu * 100), 2) if tong_doanh_thu > 0 else 0
        ket_qua.append({
            "stt": stt,
            "loai_phong": v["ten"],
            "doanh_thu": dt,
            "luot_thue": v["luot_thue"],
            "ty_le": ty_le
        })
        stt += 1

    return {
        "thang": thang,
        "nam": nam,
        "chi_tiet": ket_qua,
        "tong_doanh_thu": tong_doanh_thu
    }

def bao_cao_mat_do_thang(thang=None, nam=None):
    now = datetime.now()
    thang = int(thang) if thang else now.month
    nam = int(nam) if nam else now.year

    ds_phong = Phong.query.order_by(Phong.MaPhong).all()
    phong_dict = {p.MaPhong: 0 for p in ds_phong}

    hoa_dons = db.session.query(HoaDon, ChiTietThue).join(
        ChiTietThue, HoaDon.MaHopDong == ChiTietThue.MaHopDong
    ).filter(
        extract('month', HoaDon.NgayTraPhong) == thang,
        extract('year', HoaDon.NgayTraPhong) == nam
    ).all()

    tong_ngay = 0
    for hd, ct in hoa_dons:
        so_ngay = hd.SoNgayO if hd.SoNgayO else 1
        if ct.MaPhong in phong_dict:
            phong_dict[ct.MaPhong] += so_ngay
            tong_ngay += so_ngay

    ket_qua = []
    stt = 1
    for ma_p, so_ngay in phong_dict.items():
        ty_le = round((so_ngay / tong_ngay * 100), 2) if tong_ngay > 0 else 0
        ket_qua.append({
            "stt": stt,
            "ma_phong": ma_p,
            "so_ngay": so_ngay,
            "ty_le": ty_le
        })
        stt += 1

    return {
        "thang": thang,
        "nam": nam,
        "chi_tiet": ket_qua,
        "tong_ngay": tong_ngay
    }

def cart_stats(cart):
    total_quantity = 0
    total_amount = 0
    if cart:
        for item in cart.values():
            qty = int(item.get("quantity", 1))
            price = int(item.get("DonGia", 0))
            total_quantity += 1
            total_amount += price * qty
    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }

def hash_password(password):
    return str(hashlib.md5(password.encode("utf-8")).digest())
