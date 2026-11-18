import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import math
from datetime import datetime, date, timedelta
import json
from flask import render_template, request, redirect, session, jsonify, flash
from flask_login import login_user, logout_user, current_user
from my_app import app, db, my_login, utils
from my_app.models import (
    Phong, LoaiPhong, LoaiKhach, Khach, TaiKhoanKhach,
    TaiKhoanNhanVien, TaiKhoanAdmin, DatPhong, ChiTietThue,
    HoaDon, ThongSoQuyDinh, DanhGiaCuaKhach
)
from my_app.admin import *

@my_login.user_loader
def user_load(user_id):
    uid_str = str(user_id)
    if uid_str.startswith('nv_'):
        try:
            return TaiKhoanNhanVien.query.get(int(uid_str.replace('nv_', '')))
        except:
            return None
    if uid_str.startswith('kh_'):
        try:
            return TaiKhoanKhach.query.get(int(uid_str.replace('kh_', '')))
        except:
            return None
    try:
        raw_id = int(uid_str)
        nv = TaiKhoanNhanVien.query.get(raw_id)
        if nv:
            return nv
        return TaiKhoanKhach.query.get(raw_id)
    except:
        return None

@app.context_processor
def common_context():
    loai_phong = LoaiPhong.query.all()
    loai_khach = LoaiKhach.query.all()
    cart = session.get('cart', {})
    cart_stat = utils.cart_stats(cart)
    qd = utils.get_quy_dinh()
    return {
        'ds_loai_phong': loai_phong,
        'ds_loai_khach': loai_khach,
        'cart_stats': cart_stat,
        'quy_dinh': qd
    }

@app.route('/')
def home():
    kw = request.args.get('kw', '').strip()
    ma_loai = request.args.get('MaLoaiPhong', type=int)
    tinh_trang = request.args.get('TinhTrang', '').strip()
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    page = request.args.get('page', 1, type=int)
    page_size = 8

    phong_list, total = utils.get_phong(
        kw=kw,
        ma_loai_phong=ma_loai,
        tinh_trang=tinh_trang if tinh_trang else None,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size
    )

    page_num = math.ceil(total / page_size) if total > 0 else 1

    return render_template(
        'home.html',
        Phong=phong_list,
        kw=kw,
        MaLoaiPhong=ma_loai,
        TinhTrang=tinh_trang,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_num=page_num,
        total=total
    )

@app.route('/dangnhap')
def dangnhap():
    if current_user.is_authenticated:
        if getattr(current_user, 'is_admin', False):
            return redirect('/admin')
        if getattr(current_user, 'get_urole', lambda: '')() == 'NhanVien':
            return redirect('/nhanvien')
        return redirect('/')
    return render_template('layout/dangnhap.html')

@app.route('/login', methods=['POST'])
def login_exe():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    password_hash = utils.hash_password(password)

    user_admin = TaiKhoanNhanVien.query.filter(
        TaiKhoanNhanVien.username == username,
        TaiKhoanNhanVien.password == password_hash,
        TaiKhoanNhanVien.active == True
    ).first()

    if user_admin:
        is_admin = TaiKhoanAdmin.query.filter_by(emp_id=user_admin.emp_id).first()
        login_user(user_admin)
        session['khach'] = {'khach': {'username': username, 'id': user_admin.emp_id, 'role': 'Admin' if is_admin else 'NhanVien'}}
        if is_admin:
            return redirect('/admin')
        return redirect('/nhanvien')

    user_khach = TaiKhoanKhach.query.filter(
        TaiKhoanKhach.username == username,
        TaiKhoanKhach.password == password_hash
    ).first()

    if user_khach:
        login_user(user_khach)
        session['khach'] = {'khach': {'username': username, 'id': user_khach.MaKhach, 'role': 'Khach'}}
        return redirect('/')

    return render_template('layout/dangnhap.html', err_msg='Tên đăng nhập hoặc mật khẩu không chính xác!')

@app.route('/dangxuat')
def dangxuat():
    logout_user()
    session.pop('khach', None)
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    err_msg = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm-password', '').strip()
        ho_ten = request.form.get('HoTen', '').strip()
        cmnd = request.form.get('CMND', '').strip()
        dia_chi = request.form.get('DiaChi', '').strip()
        sdt = request.form.get('SDT', '').strip()
        ma_loai = request.form.get('LoaiKhach', 1, type=int)

        if password != confirm:
            err_msg = 'Mật khẩu xác nhận không khớp!'
        elif TaiKhoanKhach.query.filter_by(username=username).first():
            err_msg = 'Tên tài khoản đã tồn tại, vui lòng chọn tên khác!'
        else:
            kh = Khach(HoTen=ho_ten, CMND=cmnd, DiaChi=dia_chi, SDT=sdt, MaLoaiKhach=ma_loai)
            db.session.add(kh)
            db.session.commit()

            tk = TaiKhoanKhach(MaKhach=kh.MaKhach, username=username, password=utils.hash_password(password))
            db.session.add(tk)
            db.session.commit()
            return redirect('/dangnhap')

    return render_template('layout/dangky.html', err_msg=err_msg)

@app.route('/datphong', methods=['GET', 'POST'])
def route_dat_phong():
    ma_phong = request.args.get('ma_phong', type=int)
    phong = Phong.query.get(ma_phong) if ma_phong else None
    err_msg = ''
    success_dp = None

    if request.method == 'POST':
        ho_ten = request.form.get('ho_ten', '').strip()
        sdt = request.form.get('sdt', '').strip()
        cmnd = request.form.get('cmnd', '').strip()
        dia_chi = request.form.get('dia_chi', '').strip()
        ma_loai_khach = request.form.get('ma_loai_khach', 1, type=int)
        p_id = request.form.get('ma_phong', type=int)
        ngay_nhan = request.form.get('ngay_nhan')
        ngay_tra = request.form.get('ngay_tra')
        so_luong = request.form.get('so_luong', 1, type=int)

        danh_sach = []
        for i in range(1, so_luong + 1):
            ten_k = request.form.get(f'khach_ten_{i}', ho_ten if i == 1 else '').strip()
            cmnd_k = request.form.get(f'khach_cmnd_{i}', cmnd if i == 1 else '').strip()
            loai_k = request.form.get(f'khach_loai_{i}', ma_loai_khach)
            dc_k = request.form.get(f'khach_diachi_{i}', dia_chi if i == 1 else '').strip()
            if ten_k:
                danh_sach.append({
                    'stt': i,
                    'ho_ten': ten_k,
                    'cmnd': cmnd_k,
                    'loai_khach': loai_k,
                    'dia_chi': dc_k
                })

        dp, err = utils.dat_phong(
            ho_ten=ho_ten,
            sdt=sdt,
            cmnd=cmnd,
            dia_chi=dia_chi,
            ma_loai_khach=ma_loai_khach,
            ma_phong=p_id,
            ngay_nhan=ngay_nhan,
            ngay_tra=ngay_tra,
            so_luong_khach=so_luong,
            danh_sach_khach=danh_sach
        )

        if err:
            err_msg = err
            phong = Phong.query.get(p_id)
        else:
            return redirect(f'/phieudatphong/{dp.MaDatPhong}')

    return render_template('layout/datphong.html', phong=phong, err_msg=err_msg)

@app.route('/phieudatphong/<int:ma_dat_phong>')
def xem_phieu_dat_phong(ma_dat_phong):
    dp = DatPhong.query.get_or_404(ma_dat_phong)
    try:
        ds_khach = json.loads(dp.DanhSachKhach)
    except:
        ds_khach = []
    return render_template('layout/phieudatphong.html', dp=dp, ds_khach=ds_khach)

@app.route('/nhanvien')
def nhan_vien():
    ds_thue = utils.get_danh_sach_thue_chua_thanh_toan()
    phong_trong = Phong.query.filter_by(TinhTrang='FR').count()
    phong_thue = Phong.query.filter_by(TinhTrang='IU').count()
    return render_template('layout/NhanVien.html', ds_thue=ds_thue, phong_trong=phong_trong, phong_thue=phong_thue)

@app.route('/thuephong', methods=['GET', 'POST'])
def thue_phong():
    kw = request.args.get('kw', '').strip()
    dat_phong_found = utils.tim_dat_phong(kw) if kw else []

    dp_id = request.args.get('from_dat_phong', type=int)
    dp_selected = DatPhong.query.get(dp_id) if dp_id else None

    ds_phong_trong = Phong.query.filter_by(TinhTrang='FR').all()
    err_msg = ''

    if request.method == 'POST':
        ma_phong = request.form.get('ma_phong', type=int)
        ho_ten = request.form.get('ho_ten', '').strip()
        cmnd = request.form.get('cmnd', '').strip()
        dia_chi = request.form.get('dia_chi', '').strip()
        ma_loai_khach = request.form.get('ma_loai_khach', 1, type=int)
        ngay_thue = request.form.get('ngay_thue') or datetime.now().strftime('%Y-%m-%d')
        so_ngay = request.form.get('so_ngay', 1, type=int)
        so_luong = request.form.get('so_luong', 1, type=int)
        ma_dp = request.form.get('ma_dat_phong', type=int)

        danh_sach = []
        for i in range(1, so_luong + 1):
            ten_k = request.form.get(f'khach_ten_{i}', ho_ten if i == 1 else '').strip()
            cmnd_k = request.form.get(f'khach_cmnd_{i}', cmnd if i == 1 else '').strip()
            loai_k = request.form.get(f'khach_loai_{i}', ma_loai_khach)
            dc_k = request.form.get(f'khach_diachi_{i}', dia_chi if i == 1 else '').strip()
            if ten_k:
                danh_sach.append({
                    'stt': i,
                    'ho_ten': ten_k,
                    'cmnd': cmnd_k,
                    'loai_khach': loai_k,
                    'dia_chi': dc_k
                })

        ct, err = utils.lap_phieu_thue(
            ma_phong=ma_phong,
            ho_ten=ho_ten,
            cmnd=cmnd,
            dia_chi=dia_chi,
            ma_loai_khach=ma_loai_khach,
            ngay_bat_dau=ngay_thue,
            so_ngay=so_ngay,
            so_luong_khach=so_luong,
            danh_sach_khach=danh_sach,
            ma_dat_phong=ma_dp
        )

        if err:
            err_msg = err
        else:
            return redirect(f'/phieuthuephong/{ct.MaHopDong}')

    return render_template(
        'layout/thuephong.html',
        phong_trong=ds_phong_trong,
        dat_phong_found=dat_phong_found,
        dp_selected=dp_selected,
        kw=kw,
        err_msg=err_msg
    )

@app.route('/phieuthuephong/<int:ma_hop_dong>')
def xem_phieu_thue_phong(ma_hop_dong):
    ct = ChiTietThue.query.get_or_404(ma_hop_dong)
    try:
        ds_khach = json.loads(ct.DanhSachKhach)
    except:
        ds_khach = []
    return render_template('layout/phieuthuephong.html', ct=ct, ds_khach=ds_khach)

@app.route('/hoadon')
def lap_hoa_don():
    ma_hop_dong = request.args.get('mahopdong', type=int)
    ds_chua_tt = utils.get_danh_sach_thue_chua_thanh_toan()

    chi_tiet = None
    if ma_hop_dong:
        chi_tiet = utils.tinh_tien_chi_tiet(ma_hop_dong)

    return render_template(
        'layout/LapHoaDon.html',
        ds_chua_tt=ds_chua_tt,
        ma_selected=ma_hop_dong,
        chi_tiet=chi_tiet
    )

@app.route('/thanhtoan', methods=['POST'])
def xu_ly_thanh_toan():
    ma_hop_dong = request.form.get('mahopdong', type=int)
    hd, err = utils.thanh_toan(ma_hop_dong)
    if err:
        return redirect(f'/hoadon?mahopdong={ma_hop_dong}')
    return redirect(f'/in-hoadon/{hd.MaHopDong}')

@app.route('/in-hoadon/<int:ma_hop_dong>')
def in_hoa_don(ma_hop_dong):
    hd = HoaDon.query.get_or_404(ma_hop_dong)
    ct = hd.ChiTietThue
    return render_template('layout/inhoadon.html', hd=hd, ct=ct)

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_stat = utils.cart_stats(cart)
    return render_template('layout/cart.html', cart=cart, cart_stats=cart_stat)

@app.route('/api/add-item-cart', methods=['POST'])
def add_to_cart():
    cart = session.get('cart', {})
    data = request.json or {}
    ma_phong = str(data.get('MaPhong'))

    p = Phong.query.get(int(ma_phong))
    if not p or p.TinhTrang == 'IU':
        return jsonify({'error_code': 400, 'message': 'Phòng không còn trống!'})

    if ma_phong in cart:
        cart[ma_phong]['quantity'] = cart[ma_phong].get('quantity', 1) + 1
    else:
        cart[ma_phong] = {
            'MaPhong': p.MaPhong,
            'LoaiPhong': p.LoaiPhong.LoaiPhong,
            'DonGia': p.LoaiPhong.DonGia,
            'NgayBatDau': str(date.today()),
            'quantity': 1,
            'SoLuong': 1
        }

    session['cart'] = cart
    return jsonify({'error_code': 200, 'cart_stats': utils.cart_stats(cart)})

@app.route('/api/update-cart-item', methods=['PUT'])
def update_cart_item():
    cart = session.get('cart', {})
    data = request.json or {}
    ma_phong = str(data.get('MaPhong'))

    if cart and ma_phong in cart:
        cart[ma_phong]['quantity'] = int(data.get('quantity', 1))
        cart[ma_phong]['NgayBatDau'] = data.get('NgayBatDau', str(date.today()))
        cart[ma_phong]['SoLuong'] = int(data.get('SoLuong', 1))
        session['cart'] = cart
        return jsonify({'error_code': 200, 'cart_stats': utils.cart_stats(cart)})

    return jsonify({'error_code': 404})

@app.route('/api/delete-cart-item/<ma_phong>', methods=['DELETE'])
def delete_cart_item(ma_phong):
    cart = session.get('cart', {})
    if str(ma_phong) in cart:
        del cart[str(ma_phong)]
        session['cart'] = cart
        return jsonify({'error_code': 200, 'cart_stats': utils.cart_stats(cart)})
    return jsonify({'error_code': 404})

@app.route('/chitiet/<int:ma_phong>')
def chitiet_phong(ma_phong):
    p = Phong.query.get_or_404(ma_phong)
    danh_gia = DanhGiaCuaKhach.query.filter_by(MaPhong=ma_phong).all()
    return render_template('layout/chitiet.html', phong=p, danh_gia=danh_gia)

@app.route('/danhgia', methods=['GET', 'POST'])
def danh_gia():
    if request.method == 'POST':
        ma_phong = request.form.get('phong', type=int)
        ma_khach = request.form.get('khach', type=int)
        nhan_xet = request.form.get('nhanxet', '').strip()
        so_sao = request.form.get('SoSao', 5, type=int)

        if ma_phong and ma_khach and nhan_xet:
            dg = DanhGiaCuaKhach(MaPhong=ma_phong, MaKhach=ma_khach, NoiDung=nhan_xet, SoSao=so_sao)
            db.session.add(dg)
            db.session.commit()
            return redirect('/')

    phong_all = Phong.query.all()
    khach_all = Khach.query.all()
    return render_template('layout/danhgia.html', phong=phong_all, khach=khach_all)

@app.route('/mockup')
def view_mockup():
    mockup_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mockup_ui.html'))
    with open(mockup_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True, port=2000)
