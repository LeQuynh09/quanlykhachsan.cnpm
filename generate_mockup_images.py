import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('mockup_images', exist_ok=True)

try:
    font_title = ImageFont.truetype('segoeuib.ttf', 20)
    font_bold = ImageFont.truetype('segoeuib.ttf', 14)
    font_reg = ImageFont.truetype('segoeui.ttf', 13)
    font_small = ImageFont.truetype('segoeui.ttf', 11)
    font_badge = ImageFont.truetype('segoeuib.ttf', 11)
except:
    font_title = font_bold = font_reg = font_small = font_badge = ImageFont.load_default()

def draw_window_frame(draw, w, h, title):
    draw.rectangle([0, 0, w, h], fill='#ffffff', outline='#222222', width=2)
    draw.rectangle([0, 0, w, 38], fill='#f0f0f0', outline='#222222', width=2)
    draw.ellipse([12, 13, 24, 25], outline='#333333', width=1)
    draw.ellipse([30, 13, 42, 25], outline='#333333', width=1)
    draw.ellipse([48, 13, 60, 25], outline='#333333', width=1)
    draw.text((70, 10), title, fill='#222222', font=font_bold)

def draw_btn(draw, xy, text, dark=False):
    fill = '#222222' if dark else '#ffffff'
    txt_fill = '#ffffff' if dark else '#222222'
    draw.rounded_rectangle(xy, radius=4, fill=fill, outline='#222222', width=2)
    bbox = font_bold.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    cx = (xy[0] + xy[2] - tw) / 2
    cy = (xy[1] + xy[3] - th) / 2 - 1
    draw.text((cx, cy), text, fill=txt_fill, font=font_bold)

def draw_input(draw, xy, text="", placeholder=True):
    draw.rounded_rectangle(xy, radius=3, fill='#ffffff', outline='#222222', width=1)
    if text:
        txt_fill = '#888888' if placeholder else '#111111'
        draw.text((xy[0] + 8, xy[1] + 6), text, fill=txt_fill, font=font_reg)

def create_mockup_01_trang_chu():
    W, H = 840, 620
    im = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(im)
    draw_window_frame(d, W, H, "MOCKUP UI-01: TRANG CHỦ (HOMEPAGE) - MESP HOTEL")

    # Navbar
    d.rectangle([20, 50, W-20, 95], fill='#f9f9f9', outline='#222222', width=1)
    d.text((35, 62), "[MESP HOTEL]", fill='#111111', font=font_title)
    d.text((200, 66), "Trang chủ     Loại phòng v     Giỏ phòng (0)     Kênh Lễ tân", fill='#333333', font=font_reg)
    draw_btn(d, [630, 58, 715, 87], "Đăng nhập")
    draw_btn(d, [725, 58, 805, 87], "Đăng ký", dark=True)

    # Search & Filter bar
    d.rectangle([20, 110, W-20, 165], fill='#f5f5f5', outline='#222222', width=1)
    d.text((32, 116), "TÌM KIẾM VÀ LỌC PHÒNG:", fill='#222222', font=font_bold)
    draw_input(d, [32, 133, 300, 158], "Nhập số phòng, ghi chú...")
    draw_input(d, [315, 133, 490, 158], "-- Loại phòng: Tất cả v --")
    draw_input(d, [505, 133, 670, 158], "-- Tình trạng: Tất cả v --")
    draw_btn(d, [685, 133, 805, 158], "TÌM KIẾM", dark=True)

    # Room list header
    d.text((20, 180), "DANH SÁCH PHÒNG KHÁCH SẠN (Hiển thị kết quả tìm kiếm)", fill='#111111', font=font_bold)

    # 3 Room Cards
    cards = [
        {"ma": "Phòng 101", "loai": "Phòng Đơn", "gia": "150,000 đ/ngày", "tt": "Còn trống", "free": True},
        {"ma": "Phòng 102", "loai": "Phòng Đôi", "gia": "350,000 đ/ngày", "tt": "Còn trống", "free": True},
        {"ma": "Phòng 201", "loai": "Phòng VIP", "gia": "600,000 đ/ngày", "tt": "Đang thuê", "free": False},
    ]

    for i, c in enumerate(cards):
        x1 = 20 + i * 275
        x2 = x1 + 255
        y1, y2 = 205, 535
        d.rounded_rectangle([x1, y1, x2, y2], radius=6, fill='#ffffff', outline='#222222', width=1)

        # Image placeholder
        d.rectangle([x1+10, y1+10, x2-10, y1+150], fill='#fafafa', outline='#555555', width=1)
        d.line([x1+10, y1+10, x2-10, y1+150], fill='#cccccc', width=1)
        d.line([x1+10, y1+150, x2-10, y1+10], fill='#cccccc', width=1)
        d.text((x1+60, y1+70), f"[ HÌNH ẢNH {c['ma']} ]", fill='#555555', font=font_bold)

        # Details
        d.text((x1+12, y1+165), c['ma'], fill='#111111', font=font_title)
        d.rounded_rectangle([x2-85, y1+165, x2-12, y1+188], radius=3, fill='#f0f0f0', outline='#222222', width=1)
        d.text((x2-80, y1+168), c['loai'], fill='#222222', font=font_badge)

        d.text((x1+12, y1+200), f"Đơn giá: {c['gia']}", fill='#111111', font=font_bold)
        d.text((x1+12, y1+225), f"Tối đa 3 khách / phòng", fill='#666666', font=font_reg)

        tt_fill = '#222222' if c['free'] else '#f0f0f0'
        tt_txt = '#ffffff' if c['free'] else '#666666'
        d.rounded_rectangle([x1+12, y1+252, x1+100, y1+275], radius=10, fill=tt_fill, outline='#222222', width=1)
        d.text((x1+24, y1+255), c['tt'], fill=tt_txt, font=font_badge)

        # Buttons
        draw_btn(d, [x1+12, y1+290, x1+115, y1+318], "Chi tiết")
        if c['free']:
            draw_btn(d, [x1+125, y1+290, x2-12, y1+318], "+ Đặt phòng", dark=True)
        else:
            d.rounded_rectangle([x1+125, y1+290, x2-12, y1+318], radius=4, fill='#eeeeee', outline='#aaaaaa', width=1)
            d.text((x1+140, y1+296), "Hết phòng", fill='#888888', font=font_bold)

    # Pagination
    d.text((300, 560), "Trang:", fill='#444444', font=font_reg)
    draw_btn(d, [350, 552, 405, 580], "<< Trước")
    draw_btn(d, [415, 552, 450, 580], "1", dark=True)
    draw_btn(d, [460, 552, 495, 580], "2")
    draw_btn(d, [505, 552, 540, 580], "3")
    draw_btn(d, [550, 552, 605, 580], "Sau >>")

    im.save('mockup_images/mockup_01_trang_chu.png', dpi=(150, 150))

def create_mockup_02_dang_nhap():
    W, H = 650, 480
    im = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(im)
    draw_window_frame(d, W, H, "MOCKUP UI-02: ĐĂNG NHẬP HỆ THỐNG (LOGIN)")

    # Box center
    bx1, by1, bx2, by2 = 120, 70, 530, 435
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill='#ffffff', outline='#222222', width=2)

    # Title
    d.text((bx1+110, by1+25), "ĐĂNG NHẬP HỆ THỐNG", fill='#111111', font=font_title)
    d.text((bx1+75, by1+55), "Hệ thống Quản lý Khách sạn MESP Hotel", fill='#555555', font=font_reg)
    d.line([bx1+30, by1+80, bx2-30, by1+80], fill='#dddddd', width=1)

    # Form
    d.text((bx1+40, by1+100), "TÊN ĐĂNG NHẬP (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+40, by1+125, bx2-40, by1+162], "Nhập username (khách hàng, lễ tân, admin)...")

    d.text((bx1+40, by1+180), "MẬT KHẨU (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+40, by1+205, bx2-40, by1+242], "Nhập mật khẩu...", placeholder=True)

    # Button
    draw_btn(d, [bx1+40, by1+265, bx2-40, by1+310], "ĐĂNG NHẬP HỆ THỐNG", dark=True)

    d.line([bx1+40, by1+335, bx2-40, by1+335], fill='#dddddd', width=1)
    d.text((bx1+100, by1+345), "Chưa có tài khoản khách hàng?", fill='#555555', font=font_reg)
    d.text((bx1+125, by1+370), ">> Đăng ký tài khoản ngay <<", fill='#111111', font=font_bold)

    im.save('mockup_images/mockup_02_dang_nhap.png', dpi=(150, 150))

def create_mockup_03_dang_ky():
    W, H = 720, 600
    im = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(im)
    draw_window_frame(d, W, H, "MOCKUP UI-03: ĐĂNG KÝ TÀI KHOẢN KHÁCH HÀNG (REGISTER)")

    bx1, by1, bx2, by2 = 60, 60, W-60, H-30
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill='#ffffff', outline='#222222', width=2)

    d.text((bx1+140, by1+20), "ĐĂNG KÝ TÀI KHOẢN KHÁCH HÀNG", fill='#111111', font=font_title)
    d.text((bx1+130, by1+50), "Vui lòng nhập đầy đủ và chính xác các thông tin dưới đây", fill='#666666', font=font_reg)
    d.line([bx1+25, by1+75, bx2-25, by1+75], fill='#cccccc', width=1)

    # Row 1
    d.text((bx1+30, by1+90), "HỌ VÀ TÊN KHÁCH HÀNG (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+30, by1+112, bx1+275, by1+145], "Ví dụ: Nguyễn Văn A")

    d.text((bx1+305, by1+90), "SỐ CMND / CĂN CƯỚC (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+305, by1+112, bx2-30, by1+145], "Ví dụ: 079201004567")

    # Row 2
    d.text((bx1+30, by1+160), "SỐ ĐIỆN THOẠI LIÊN HỆ (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+30, by1+182, bx1+275, by1+215], "Ví dụ: 0901234567")

    d.text((bx1+305, by1+160), "LOẠI KHÁCH HÀNG (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+305, by1+182, bx2-30, by1+215], "Nội địa (Hệ số 1.0) v")

    # Row 3: Address
    d.text((bx1+30, by1+230), "ĐỊA CHỈ THƯỜNG TRÚ (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+30, by1+252, bx2-30, by1+285], "Số nhà, tên đường, Phường/Xã, Quận/Huyện, Tỉnh/TP...")

    d.line([bx1+25, by1+300, bx2-25, by1+300], fill='#dddddd', width=1)

    # Row 4: Account
    d.text((bx1+30, by1+315), "TÊN ĐĂNG NHẬP (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+30, by1+337, bx2-30, by1+370], "Chọn tên tài khoản đăng nhập (viết liền không dấu)...")

    # Row 5: Passwords
    d.text((bx1+30, by1+385), "MẬT KHẨU (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+30, by1+407, bx1+275, by1+440], "Nhập mật khẩu...")

    d.text((bx1+305, by1+385), "XÁC NHẬN MẬT KHẨU (*):", fill='#222222', font=font_bold)
    draw_input(d, [bx1+305, by1+407, bx2-30, by1+440], "Nhập lại mật khẩu...")

    # Button
    draw_btn(d, [bx1+30, by1+465, bx2-30, by1+505], "XÁC NHẬN ĐĂNG KÝ TÀI KHOẢN", dark=True)

    d.text((bx1+170, by1+515), "Đã có tài khoản? Nhấn vào đây để Đăng nhập", fill='#444444', font=font_reg)

    im.save('mockup_images/mockup_03_dang_ky.png', dpi=(150, 150))

def create_mockup_04_phieu_thue_phong():
    W, H = 840, 680
    im = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(im)
    draw_window_frame(d, W, H, "MOCKUP UI-04: LẬP PHIẾU THUÊ PHÒNG (DÀNH CHO LỄ TÂN)")

    # Search reservation box
    d.rounded_rectangle([25, 55, W-25, 120], radius=4, fill='#f9f9f9', outline='#222222', width=1)
    d.text((38, 63), "[TRA CỨU KHÁCH ĐÃ ĐẶT PHÒNG TRƯỚC]", fill='#111111', font=font_bold)
    draw_input(d, [38, 83, W-165, 110], "Nhập họ tên hoặc SĐT khách để tìm phiếu đặt phòng...")
    draw_btn(d, [W-155, 83, W-38, 110], "TRA CỨU")

    # Main Form Box
    d.rounded_rectangle([25, 135, W-25, H-25], radius=5, fill='#ffffff', outline='#222222', width=2)
    d.text((40, 150), "PHIẾU THUÊ PHÒNG KHÁCH SẠN", fill='#111111', font=font_title)
    d.text((W-220, 155), "Ngày lập: 26/11/2026", fill='#555555', font=font_reg)
    d.line([40, 180, W-40, 180], fill='#222222', width=1)

    # Row 1
    d.text((40, 195), "CHỌN PHÒNG THUÊ (*):", fill='#222222', font=font_bold)
    draw_input(d, [40, 217, 400, 248], "Phòng 102 (Loại: Đôi - Đơn giá: 350.000 đ) v", placeholder=False)

    d.text((425, 195), "SỐ LƯỢNG KHÁCH Ở (Tối đa 3 khách) (*):", fill='#222222', font=font_bold)
    draw_input(d, [425, 217, W-40, 248], "3 khách (Có khách thứ 3 phụ thu +25%) v", placeholder=False)

    # Row 2
    d.text((40, 260), "NGÀY BẮT ĐẦU THUÊ (*):", fill='#222222', font=font_bold)
    draw_input(d, [40, 282, 400, 313], "26/11/2026", placeholder=False)

    d.text((425, 260), "SỐ NGÀY Ở DỰ KIẾN (*):", fill='#222222', font=font_bold)
    draw_input(d, [425, 282, W-40, 313], "3 ngày", placeholder=False)

    # Table of guests
    d.text((40, 330), "DANH SÁCH CHI TIẾT KHÁCH HÀNG TRONG PHÒNG:", fill='#111111', font=font_bold)

    tx1, ty1, tx2, ty2 = 40, 355, W-40, 520
    d.rectangle([tx1, ty1, tx2, ty2], fill='#ffffff', outline='#222222', width=1)

    # Header row
    d.rectangle([tx1, ty1, tx2, ty1+30], fill='#e8e8e8', outline='#222222', width=1)
    cols = [40, 90, 310, 460, 620, W-40]
    for c in cols[1:-1]:
        d.line([c, ty1, c, ty2], fill='#222222', width=1)

    d.text((50, ty1+7), "STT", fill='#111111', font=font_bold)
    d.text((150, ty1+7), "Họ tên khách hàng", fill='#111111', font=font_bold)
    d.text((345, ty1+7), "Loại khách", fill='#111111', font=font_bold)
    d.text((500, ty1+7), "CMND / CCCD", fill='#111111', font=font_bold)
    d.text((690, ty1+7), "Địa chỉ", fill='#111111', font=font_bold)

    # Rows
    rows_data = [
        ("1", "Nguyễn Văn A (Người đặt)", "Nội địa", "079201004567", "Hà Nội"),
        ("2", "John Smith", "Nước ngoài (x1.5)", "USA-9876543", "California, USA"),
        ("3", "Trần Thị B (Khách thứ 3)", "Nội địa (+25%)", "080201009876", "Hà Nội")
    ]

    for idx, r in enumerate(rows_data):
        ry = ty1 + 30 + idx * 45
        d.line([tx1, ry, tx2, ry], fill='#cccccc', width=1)
        d.text((60, ry+12), r[0], fill='#111111', font=font_reg)
        draw_input(d, [cols[1]+6, ry+6, cols[2]-6, ry+38], r[1], placeholder=False)
        draw_input(d, [cols[2]+6, ry+6, cols[3]-6, ry+38], r[2], placeholder=False)
        draw_input(d, [cols[3]+6, ry+6, cols[4]-6, ry+38], r[3], placeholder=False)
        draw_input(d, [cols[4]+6, ry+6, cols[5]-6, ry+38], r[4], placeholder=False)

    # Note
    d.text((40, 532), "* Quy định Yêu cầu 2: Mỗi phòng tối đa 3 khách. Có 2 loại khách (nội địa và nước ngoài).", fill='#555555', font=font_small)
    d.text((40, 550), "* Quy định Yêu cầu 3: Khách thứ 3 phụ thu 25%. Nếu có khách nước ngoài nhân hệ số 1.5.", fill='#555555', font=font_small)

    # Action buttons
    draw_btn(d, [W-340, 580, W-180, 620], "LÀM LẠI")
    draw_btn(d, [W-165, 580, W-40, 620], "LẬP PHIẾU THUÊ", dark=True)

    im.save('mockup_images/mockup_04_phieu_thue_phong.png', dpi=(150, 150))

def create_mockup_05_hoa_don():
    W, H = 800, 720
    im = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(im)
    draw_window_frame(d, W, H, "MOCKUP UI-05: HÓA ĐƠN THANH TOÁN (INVOICE)")

    bx1, by1, bx2, by2 = 40, 55, W-40, H-25
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill='#ffffff', outline='#222222', width=2)

    # Header
    d.text((bx1+220, by1+20), "HÓA ĐƠN THANH TOÁN TIỀN PHÒNG", fill='#111111', font=font_title)
    d.text((bx1+255, by1+48), "KHÁCH SẠN MESP HOTEL - TP. HỒ CHÍ MINH", fill='#444444', font=font_bold)
    d.text((bx1+245, by1+68), "Mã hóa đơn: HD-2026-0089  |  Ngày lập: 26/11/2026", fill='#666666', font=font_reg)
    d.line([bx1+25, by1+95, bx2-25, by1+95], fill='#222222', width=2)

    # Info 2 columns
    d.text((bx1+30, by1+110), "Họ tên khách đại diện:", fill='#555555', font=font_reg)
    d.text((bx1+180, by1+110), "Nguyễn Văn A", fill='#111111', font=font_bold)

    d.text((bx1+30, by1+135), "Số CMND / CCCD:", fill='#555555', font=font_reg)
    d.text((bx1+180, by1+135), "079201004567", fill='#111111', font=font_bold)

    d.text((bx1+30, by1+160), "Địa chỉ liên lạc:", fill='#555555', font=font_reg)
    d.text((bx1+180, by1+160), "Hà Nội", fill='#111111', font=font_reg)

    d.text((bx1+400, by1+110), "Phòng thanh toán:", fill='#555555', font=font_reg)
    d.text((bx1+530, by1+110), "Phòng 102 (Loại: Đôi)", fill='#111111', font=font_bold)

    d.text((bx1+400, by1+135), "Ngày nhận phòng:", fill='#555555', font=font_reg)
    d.text((bx1+530, by1+135), "23/11/2026", fill='#111111', font=font_reg)

    d.text((bx1+400, by1+160), "Ngày trả phòng:", fill='#555555', font=font_reg)
    d.text((bx1+530, by1+160), "26/11/2026 (Số ngày: 3)", fill='#111111', font=font_bold)

    # Table of fees
    tx1, ty1, tx2, ty2 = bx1+25, by1+195, bx2-25, by1+395
    d.rectangle([tx1, ty1, tx2, ty2], fill='#ffffff', outline='#222222', width=1)

    # Table header
    d.rectangle([tx1, ty1, tx2, ty1+32], fill='#f0f0f0', outline='#222222', width=1)
    t_cols = [tx1, tx1+310, tx1+410, tx1+530, tx2]
    for c in t_cols[1:-1]:
        d.line([c, ty1, c, ty2], fill='#222222', width=1)

    d.text((tx1+80, ty1+7), "Khoản mục thanh toán", fill='#111111', font=font_bold)
    d.text((tx1+335, ty1+7), "Số lượng", fill='#111111', font=font_bold)
    d.text((tx1+445, ty1+7), "Đơn giá", fill='#111111', font=font_bold)
    d.text((tx1+555, ty1+7), "Thành tiền (VNĐ)", fill='#111111', font=font_bold)

    # Rows
    inv_rows = [
        ("1. Tiền phòng (Đơn giá phòng đôi 2 khách)", "3 ngày", "350,000 đ", "1,050,000 đ"),
        ("2. Phụ thu khách thứ 3 (+25% đơn giá)", "1 khách", "+25%", "+262,500 đ"),
        ("3. Hệ số khách nước ngoài (John Smith)", "1 khách", "Hệ số x 1.5", "x 1.5"),
    ]

    for idx, r in enumerate(inv_rows):
        ry = ty1 + 32 + idx * 42
        d.line([tx1, ry, tx2, ry], fill='#cccccc', width=1)
        d.text((tx1+15, ry+12), r[0], fill='#111111', font=font_reg)
        d.text((tx1+340, ry+12), r[1], fill='#333333', font=font_reg)
        d.text((tx1+435, ry+12), r[2], fill='#333333', font=font_reg)
        d.text((tx1+560, ry+12), r[3], fill='#111111', font=font_bold)

    # Total row
    tot_y = ty1 + 32 + 3 * 42
    d.rectangle([tx1, tot_y, tx2, ty2], fill='#222222')
    d.text((tx1+100, tot_y+10), "TỔNG TIỀN PHẢI THANH TOÁN:", fill='#ffffff', font=font_title)
    d.text((tx1+520, tot_y+10), "1,968,750 VNĐ", fill='#ffffff', font=font_title)

    # Calculation formula note
    d.text((bx1+30, by1+410), "* Công thức tính theo Yêu cầu 3:", fill='#222222', font=font_bold)
    d.text((bx1+30, by1+430), "  Tổng tiền = Đơn giá x Số ngày ở x (1 + Phụ thu 25%) x Hệ số nước ngoài 1.5", fill='#444444', font=font_reg)
    d.text((bx1+30, by1+450), "  Chi tiết:   350,000 đ x 3 ngày x 1.25 x 1.5 = 1,968,750 đ", fill='#111111', font=font_bold)

    # Signatures
    d.text((bx1+80, by1+485), "KHÁCH HÀNG KÝ TÊN", fill='#111111', font=font_bold)
    d.text((bx1+85, by1+505), "(Ký và ghi rõ họ tên)", fill='#666666', font=font_small)
    d.text((bx1+105, by1+570), "Nguyễn Văn A", fill='#111111', font=font_bold)

    d.text((bx2-220, by1+485), "NHÂN VIÊN THU NGÂN", fill='#111111', font=font_bold)
    d.text((bx2-225, by1+505), "(Ký và xác nhận thu tiền)", fill='#666666', font=font_small)
    d.text((bx2-225, by1+570), "Lễ tân: Nguyễn Văn Thuận", fill='#111111', font=font_bold)

    # Action buttons
    draw_btn(d, [bx1+180, by1+605, bx1+320, by1+640], "IN HÓA ĐƠN")
    draw_btn(d, [bx1+350, by1+605, bx2-180, by1+640], "XÁC NHẬN ĐÃ THU TIỀN", dark=True)

    im.save('mockup_images/mockup_05_hoa_don.png', dpi=(150, 150))

if __name__ == '__main__':
    create_mockup_01_trang_chu()
    create_mockup_02_dang_nhap()
    create_mockup_03_dang_ky()
    create_mockup_04_phieu_thue_phong()
    create_mockup_05_hoa_don()
    print("Generated 5 mockup images successfully!")
