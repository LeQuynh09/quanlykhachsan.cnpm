import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = Document()

# Set standard margins (1 inch = 1440 twips)
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.0)
    s.right_margin = Inches(1.0)
    
    footer = s.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_run = f_p.add_run("Tài liệu Thiết kế Mockup UI & Xử lý Giao diện - Quản lý Khách sạn")
    f_run.font.name = "Arial"
    f_run.font.size = Pt(8.5)
    f_run.font.color.rgb = RGBColor(120, 120, 120)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=90, bottom=90, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text, bold_title="LƯU Ý NGHIỆP VỤ: "):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F5F5F5")
    set_cell_margins(cell, top=110, bottom=110, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="222222"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(bold_title)
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(9.5)
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Arial"
    r_txt.font.size = Pt(9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].width = Inches(col_widths[i])
        set_cell_background(hdr_cells[i], "EAEAEA")
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9)
            r.bold = True
            
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg = "FFFFFF" if row_idx % 2 == 0 else "FAFAFA"
        for i, val in enumerate(row_data):
            row_cells[i].text = str(val)
            row_cells[i].width = Inches(col_widths[i])
            set_cell_background(row_cells[i], bg)
            set_cell_margins(row_cells[i], top=80, bottom=80, left=100, right=100)
            p = row_cells[i].paragraphs[0]
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(8.5)
                
    for row in table.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            b = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/></w:tcBorders>')
            tcPr.append(b)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F9F9F9")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/><w:left w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/><w:right w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(code_text)
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(30, 30, 30)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

# ==================== COVER / HEADER ====================
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_top.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO — TRƯỜNG ĐẠI HỌC\nKHOA CÔNG NGHỆ THÔNG TIN\n***")
r.font.name = "Arial"
r.font.size = Pt(11)
r.font.color.rgb = RGBColor(80, 80, 80)
p_top.paragraph_format.space_after = Pt(25)

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_t = p_title.add_run("TÀI LIỆU THIẾT KẾ MOCKUP UI\nVÀ THIẾT KẾ XỬ LÝ GIAO DIỆN PHẦN MỀM")
r_t.font.name = "Arial"
r_t.font.size = Pt(18)
r_t.bold = True
r_t.font.color.rgb = RGBColor(20, 20, 20)
p_title.paragraph_format.space_after = Pt(10)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_s = p_sub.add_run("ĐỀ TÀI 2: HỆ THỐNG QUẢN LÝ KHÁCH SẠN (MESP HOTEL)")
r_s.font.name = "Arial"
r_s.font.size = Pt(13)
r_s.bold = True
r_s.font.color.rgb = RGBColor(70, 70, 70)
p_sub.paragraph_format.space_after = Pt(25)

# Metadata Box
tbl_meta = doc.add_table(rows=5, cols=2)
tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_info = [
    ("Học phần / Môn học:", "Công nghệ phần mềm (CNPM)"),
    ("Loại tài liệu:", "Thiết kế Giao diện (Mockup UI) & Thiết kế Xử lý (Processing Logic)"),
    ("Phương pháp phân tích:", "Hướng đối tượng kết hợp kiến trúc MVC (Model-View-Controller)"),
    ("Mô hình giao diện:", "Wireframe đơn sắc (Black & White Low-Fidelity), Responsive"),
    ("Nền tảng thực thi:", "Python Flask 2.x, Jinja2, SQLAlchemy ORM, MySQL (dbks)")
]
for idx, (lbl, val) in enumerate(meta_info):
    c0 = tbl_meta.cell(idx, 0)
    c1 = tbl_meta.cell(idx, 1)
    c0.width = Inches(2.2)
    c1.width = Inches(4.3)
    c0.text = lbl
    c1.text = val
    c0.paragraphs[0].runs[0].bold = True
    c0.paragraphs[0].runs[0].font.name = "Arial"
    c0.paragraphs[0].runs[0].font.size = Pt(9.5)
    c1.paragraphs[0].runs[0].font.name = "Arial"
    c1.paragraphs[0].runs[0].font.size = Pt(9.5)
    set_cell_background(c0, "F5F5F5")
    set_cell_background(c1, "FFFFFF")
    set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
    set_cell_margins(c1, top=60, bottom=60, left=100, right=100)

doc.add_page_break()

# ==================== PHẦN MỞ ĐẦU ====================
h1 = doc.add_heading("I. NGUYÊN TẮC THIẾT KẾ GIAO DIỆN VÀ THIẾT KẾ XỬ LÝ", level=1)
h1.paragraph_format.space_before = Pt(12)
h1.paragraph_format.space_after = Pt(6)

doc.add_paragraph(
    "Trong quy trình phát triển phần mềm chuẩn mực (Software Engineering Lifecycle), thiết kế giao diện (UI Design) và thiết kế xử lý (Processing Logic Design) là hai thành phần song hành không thể tách rời:"
)

bullets_intro = [
    ("Thiết kế giao diện (Mockup UI / Wireframe): ", "Trực quan hóa cấu trúc, bố cục, phân bố không gian và các thành phần nhập/xuất dữ liệu trên màn hình người dùng."),
    ("Thiết kế xử lý (Processing Specification): ", "Mô tả chi tiết các sự kiện/biến cố (Events), dữ liệu đầu vào (Inputs), quy trình kiểm tra tính hợp lệ (Validations), các bước thuật toán và các thay đổi dữ liệu trong CSDL tương ứng.")
]
for b_t, b_d in bullets_intro:
    bp = doc.add_paragraph(style='List Bullet')
    bp.paragraph_format.space_after = Pt(2)
    r1 = bp.add_run(b_t)
    r1.bold = True
    r1.font.name = "Arial"
    r2 = bp.add_run(b_d)
    r2.font.name = "Arial"

doc.add_paragraph(
    "Mỗi màn hình trong tài liệu dưới đây đều được cấu trúc chuẩn hóa thành 3 phần:\n"
    "1. Bản vẽ Mockup UI trắng đen (Wireframe).\n"
    "2. Bảng đặc tả các trường dữ liệu trên màn hình.\n"
    "3. Thiết kế xử lý chi tiết (Danh mục biến cố, thuật toán xử lý và quy tắc kiểm tra hợp lệ)."
)

# ==================== MÀN HÌNH 1: TRANG CHỦ ====================
doc.add_page_break()
h2 = doc.add_heading("II. MÀN HÌNH UI-01: GIAO DIỆN TRANG CHỦ (HOMEPAGE)", level=1)

# 1. Ảnh mockup
img1_path = "mockup_images/mockup_01_trang_chu.png"
if os.path.exists(img1_path):
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_img1 = doc.add_paragraph()
    p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(img1_path, width=Inches(6.0))
    p_cap1 = doc.add_paragraph()
    p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap1 = p_cap1.add_run("Hình 1. Bản vẽ Mockup Giao diện Trang chủ (UI-01)")
    r_cap1.italic = True
    r_cap1.font.size = Pt(9)

# 2. Đặc tả dữ liệu
p_t1 = doc.add_paragraph()
r1 = p_t1.add_run("1. Đặc tả thành phần dữ liệu giao diện Trang chủ")
r1.bold = True
r1.font.size = Pt(10.5)

tbl1 = doc.add_table(rows=6, cols=4)
tbl1_headers = ["Thành phần", "Loại điều khiển", "Dữ liệu / Nguồn cấp", "Mô tả hành vi tương tác"]
tbl1_data = [
    ["Thanh điều hướng (Navbar)", "Header Menu", "Hệ thống MESP Hotel", "Logo, menu Trang chủ, Loại phòng, Giỏ phòng [badge], Kênh Lễ tân, Đăng nhập/Đăng ký."],
    ["Thanh tìm kiếm từ khóa", "Input Text (kw)", "Người dùng nhập", "Tìm kiếm tương đối theo Số phòng hoặc Ghi chú tiện ích phòng."],
    ["Bộ lọc Loại phòng", "Select Dropdown", "Bảng LoaiPhong", "Lọc theo: Tất cả, Phòng Đơn, Phòng Đôi, Phòng VIP."],
    ["Bộ lọc Tình trạng", "Select Dropdown", "Phong.TinhTrang", "Lọc: Tất cả, Còn trống (FR), Đang thuê (IU)."],
    ["Thẻ hiển thị phòng (Card)", "Box Component", "Bảng Phong, LoaiPhong", "Hiển thị ảnh phòng, tên phòng, đơn giá/ngày, trạng thái, nút 'Chi tiết' và nút '+ Đặt phòng'."],
]
format_table(tbl1, [1.5, 1.3, 1.6, 2.1], tbl1_headers, tbl1_data)

# 3. THIẾT KẾ XỬ LÝ TRANG CHỦ
p_xl1 = doc.add_paragraph()
p_xl1.paragraph_format.space_before = Pt(8)
r_xl1 = p_xl1.add_run("2. Thiết kế xử lý cho màn hình Trang chủ (Processing Design)")
r_xl1.bold = True
r_xl1.font.size = Pt(10.5)

# Bảng biến cố UI 1
tbl_bc1 = doc.add_table(rows=4, cols=4)
tbl_bc1_headers = ["Tên biến cố / Sự kiện", "Đối tượng kích hoạt", "Dữ liệu đầu vào (Input)", "Hành động xử lý hệ thống"]
tbl_bc1_data = [
    ["Form_Load", "Trình duyệt (HTTP GET /)", "Session giỏ hàng, page=1", "Nạp danh mục loại phòng, đọc giỏ hàng, truy vấn 8 phòng đầu tiên và tính tổng số trang."],
    ["btnTimKiem_Click", "Nút 'TÌM KIẾM' (GET /)", "kw, MaLoaiPhong, TinhTrang", "Lọc dữ liệu phòng theo nhiều tiêu chí kết hợp, phân trang và render lại danh sách phòng."],
    ["btnDatPhong_Click", "Nút '+ Đặt phòng'", "MaPhong, MaLoaiPhong", "Thêm phòng vào Session['cart'], tăng số lượng giỏ phòng hoặc chuyển hướng sang Phiếu đặt phòng."]
]
format_table(tbl_bc1, [1.5, 1.4, 1.6, 2.0], tbl_bc1_headers, tbl_bc1_data)

doc.add_paragraph().paragraph_format.space_after = Pt(2)
doc.add_paragraph("Thuật toán xử lý tìm kiếm & lọc phòng (btnTimKiem_Click):").runs[0].bold = True

add_code_block(doc, 
"Bước 1: Tiếp nhận tham số kw, MaLoaiPhong, TinhTrang, page, page_size=8 từ HTTP GET.\n"
"Bước 2: Xây dựng câu truy vấn động:\n"
"        query = Phong.query.join(LoaiPhong)\n"
"        Nếu kw != rỗng: query = query.filter(Phong.MaPhong.like(%kw%) OR Phong.GhiChu.like(%kw%))\n"
"        Nếu MaLoaiPhong được chọn: query = query.filter(Phong.MaLoaiPhong == MaLoaiPhong)\n"
"        Nếu TinhTrang được chọn: query = query.filter(Phong.TinhTrang == TinhTrang)\n"
"Bước 3: Đếm tổng số bản ghi thỏa điều kiện: total = query.count()\n"
"        Tính số trang: total_pages = ceil(total / page_size)\n"
"Bước 4: Phân trang: results = query.slice((page-1)*page_size, page*page_size).all()\n"
"Bước 5: Render view 'home.html' truyền danh sách results và các tham số lọc."
)

add_callout(
    doc,
    "Quy định Yêu cầu 1: Hệ thống hỗ trợ tìm kiếm phòng theo nhiều tiêu chí (số phòng, loại phòng, tình trạng, khoảng giá). Thời điểm nhận phòng không quá 28 ngày kể từ ngày đặt phòng.",
    bold_title="RÀNG BUỘC YÊU CẦU 1: "
)

# ==================== MÀN HÌNH 2: ĐĂNG NHẬP ====================
doc.add_page_break()
h3 = doc.add_heading("III. MÀN HÌNH UI-02: GIAO DIỆN ĐĂNG NHẬP (LOGIN)", level=1)

img2_path = "mockup_images/mockup_02_dang_nhap.png"
if os.path.exists(img2_path):
    p_img2 = doc.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(img2_path, width=Inches(5.0))
    p_cap2 = doc.add_paragraph()
    p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap2 = p_cap2.add_run("Hình 2. Bản vẽ Mockup Giao diện Đăng nhập (UI-02)")
    r_cap2.italic = True
    r_cap2.font.size = Pt(9)

p_t2 = doc.add_paragraph()
r2 = p_t2.add_run("1. Đặc tả thành phần dữ liệu giao diện Đăng nhập")
r2.bold = True
r2.font.size = Pt(10.5)

tbl2 = doc.add_table(rows=4, cols=4)
tbl2_headers = ["Tên trường", "Kiểu nhập", "Ràng buộc dữ liệu", "Xử lý hệ thống"]
tbl2_data = [
    ["Tên đăng nhập (username)", "Text Box", "Bắt buộc, không dấu", "Đối soát trong cả 2 bảng TaiKhoanNhanVien và TaiKhoanKhach."],
    ["Mật khẩu (password)", "Password Box", "Bắt buộc", "Băm MD5 trước khi so khớp chuỗi mã hóa lưu trong CSDL."],
    ["Nút 'ĐĂNG NHẬP'", "Submit Button", "Click", "Kiểm tra hợp lệ, ghi session đăng nhập và tự động chuyển hướng theo Role."]
]
format_table(tbl2, [1.6, 1.2, 1.6, 2.1], tbl2_headers, tbl2_data)

# 3. THIẾT KẾ XỬ LÝ ĐĂNG NHẬP
p_xl2 = doc.add_paragraph()
p_xl2.paragraph_format.space_before = Pt(8)
r_xl2 = p_xl2.add_run("2. Thiết kế xử lý cho màn hình Đăng nhập (Processing Design)")
r_xl2.bold = True
r_xl2.font.size = Pt(10.5)

tbl_bc2 = doc.add_table(rows=3, cols=4)
tbl_bc2_headers = ["Tên biến cố / Sự kiện", "Đối tượng kích hoạt", "Dữ liệu đầu vào (Input)", "Hành động xử lý hệ thống"]
tbl_bc2_data = [
    ["Form_Load", "Trình duyệt (GET /dangnhap)", "current_user", "Nếu người dùng đã đăng nhập: kiểm tra role để redirect thẳng về /admin, /nhanvien hoặc /."],
    ["btnDangNhap_Click", "Nút 'ĐĂNG NHẬP' (POST /login)", "username, password", "Xác thực tài khoản, kiểm tra phân quyền 3 cấp (Admin / Lễ tân / Khách) và lưu session."]
]
format_table(tbl_bc2, [1.5, 1.5, 1.5, 2.0], tbl_bc2_headers, tbl_bc2_data)

doc.add_paragraph().paragraph_format.space_after = Pt(2)
doc.add_paragraph("Thuật toán xác thực & phân quyền tự động (btnDangNhap_Click):").runs[0].bold = True

add_code_block(doc,
"Bước 1: Tiếp nhận username và password từ Form submit.\n"
"Bước 2: Kiểm tra validation: nếu username rỗng hoặc password rỗng:\n"
"        Trả về thông báo lỗi: 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!'\n"
"Bước 3: Băm mật khẩu đầu vào: pwd_hash = MD5(password)\n"
"Bước 4: Kiểm tra tài khoản trong bảng TaiKhoanNhanVien (active == True):\n"
"        Nếu tìm thấy user_nv:\n"
"            login_user(user_nv)\n"
"            Kiểm tra TaiKhoanAdmin.query.filter_by(emp_id=user_nv.emp_id).first():\n"
"                Nếu có bản ghi Admin -> Chuyển hướng đến: /admin\n"
"                Nếu là Lễ tân thường -> Chuyển hướng đến: /nhanvien\n"
"Bước 5: Nếu không thuộc nhân viên, kiểm tra bảng TaiKhoanKhach:\n"
"        Nếu tìm thấy user_khach:\n"
"            login_user(user_khach)\n"
"            Chuyển hướng đến Trang chủ: /\n"
"Bước 6: Nếu không khớp bất kỳ tài khoản nào:\n"
"        Trả về thông báo lỗi: 'Tên đăng nhập hoặc mật khẩu không chính xác!'"
)

# ==================== MÀN HÌNH 3: ĐĂNG KÝ ====================
doc.add_page_break()
h4 = doc.add_heading("IV. MÀN HÌNH UI-03: GIAO DIỆN ĐĂNG KÝ TÀI KHOẢN (REGISTER)", level=1)

img3_path = "mockup_images/mockup_03_dang_ky.png"
if os.path.exists(img3_path):
    p_img3 = doc.add_paragraph()
    p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(img3_path, width=Inches(5.4))
    p_cap3 = doc.add_paragraph()
    p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap3 = p_cap3.add_run("Hình 3. Bản vẽ Mockup Giao diện Đăng ký tài khoản (UI-03)")
    r_cap3.italic = True
    r_cap3.font.size = Pt(9)

p_t3 = doc.add_paragraph()
r3 = p_t3.add_run("1. Đặc tả thành phần dữ liệu giao diện Đăng ký")
r3.bold = True
r3.font.size = Pt(10.5)

tbl3 = doc.add_table(rows=7, cols=4)
tbl3_headers = ["Trường thông tin", "Kiểu dữ liệu", "Bắt buộc", "Ghi chú nghiệp vụ"]
tbl3_data = [
    ["Họ và tên khách", "Varchar(100)", "Có (*)", "Họ tên đầy đủ của khách hàng."],
    ["Số CMND / CCCD", "Varchar(20)", "Có (*)", "Số định danh cá nhân (9 hoặc 12 số) hoặc số hộ chiếu."],
    ["Số điện thoại", "Varchar(20)", "Có (*)", "Dùng tra cứu lịch sử đặt phòng nhanh."],
    ["Loại khách hàng", "Dropdown Select", "Có (*)", "Nội địa (hệ số 1.0) hoặc Nước ngoài (hệ số 1.5)."],
    ["Địa chỉ liên lạc", "Varchar(255)", "Có (*)", "Địa chỉ cư trú của khách hàng."],
    ["Tên đăng nhập & Mật khẩu", "Varchar(100)", "Có (*)", "Username duy nhất (Unique), mật khẩu xác nhận trùng khớp."]
]
format_table(tbl3, [1.6, 1.2, 1.1, 2.6], tbl3_headers, tbl3_data)

# 3. THIẾT KẾ XỬ LÝ ĐĂNG KÝ
p_xl3 = doc.add_paragraph()
p_xl3.paragraph_format.space_before = Pt(8)
r_xl3 = p_xl3.add_run("2. Thiết kế xử lý cho màn hình Đăng ký (Processing Design)")
r_xl3.bold = True
r_xl3.font.size = Pt(10.5)

tbl_bc3 = doc.add_table(rows=2, cols=4)
tbl_bc3_headers = ["Tên biến cố / Sự kiện", "Đối tượng kích hoạt", "Dữ liệu đầu vào (Input)", "Hành động xử lý hệ thống"]
tbl_bc3_data = [
    ["btnDangKy_Click", "Nút 'TẠO TÀI KHOẢN' (POST /register)", "HoTen, CMND, SDT, DiaChi, LoaiKhach, username, password, confirm_password", "Kiểm tra tính hợp lệ dữ liệu, kiểm tra trùng lặp tài khoản, mở Transaction ghi vào bảng Khach và TaiKhoanKhach."]
]
format_table(tbl_bc3, [1.5, 1.5, 1.6, 1.9], tbl_bc3_headers, tbl_bc3_data)

doc.add_paragraph().paragraph_format.space_after = Pt(2)
doc.add_paragraph("Thuật toán đăng ký tài khoản khách hàng (btnDangKy_Click):").runs[0].bold = True

add_code_block(doc,
"Bước 1: Nhận toàn bộ trường dữ liệu từ form gửi lên.\n"
"Bước 2: Kiểm tra ràng buộc hợp lệ:\n"
"        - Nếu password != confirm_password: Báo lỗi 'Mật khẩu xác nhận không khớp!'\n"
"        - Nếu TaiKhoanKhach.query.filter_by(username=username).first():\n"
"            Báo lỗi 'Tên tài khoản đã tồn tại, vui lòng chọn tên khác!'\n"
"        - Nếu CMND hoặc SĐT không đúng định dạng chữ số: Báo lỗi định dạng.\n"
"Bước 3: Mở Transaction cơ sở dữ liệu (db.session.begin()):\n"
"        Tạo đối tượng Khach:\n"
"            new_khach = Khach(HoTen=ho_ten, CMND=cmnd, DiaChi=dia_chi, SDT=sdt, MaLoaiKhach=ma_loai)\n"
"            db.session.add(new_khach)\n"
"            db.session.flush() # Lấy MaKhach tự sinh\n"
"        Tạo đối tượng TaiKhoanKhach:\n"
"            new_tk = TaiKhoanKhach(MaKhach=new_khach.MaKhach, username=username, password=MD5(password))\n"
"            db.session.add(new_tk)\n"
"        db.session.commit() # Lưu vĩnh viễn vào CSDL\n"
"Bước 4: Chuyển hướng sang màn hình /dangnhap kèm thông báo thành công."
)

# ==================== MÀN HÌNH 4: PHIẾU THUÊ PHÒNG ====================
doc.add_page_break()
h5 = doc.add_heading("V. MÀN HÌNH UI-04: LẬP PHIẾU THUÊ PHÒNG (DÀNH CHO LỄ TÂN)", level=1)

img4_path = "mockup_images/mockup_04_phieu_thue_phong.png"
if os.path.exists(img4_path):
    p_img4 = doc.add_paragraph()
    p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(img4_path, width=Inches(6.0))
    p_cap4 = doc.add_paragraph()
    p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap4 = p_cap4.add_run("Hình 4. Bản vẽ Mockup Giao diện Lập phiếu thuê phòng (UI-04)")
    r_cap4.italic = True
    r_cap4.font.size = Pt(9)

p_t4 = doc.add_paragraph()
r4 = p_t4.add_run("1. Đặc tả thành phần dữ liệu Phiếu thuê phòng")
r4.bold = True
r4.font.size = Pt(10.5)

tbl4 = doc.add_table(rows=6, cols=4)
tbl4_headers = ["Thông tin", "Kiểu nhập", "Ràng buộc nghiệp vụ", "Hành động hệ thống"]
tbl4_data = [
    ["Tra cứu đặt phòng", "Search Input", "Họ tên / SĐT khách", "Tìm kiếm trong DatPhong; khi chọn sẽ tự động điền các trường bên dưới."],
    ["Chọn phòng thuê", "Select Dropdown", "Chỉ chọn phòng FR", "Chỉ nạp danh sách phòng có tình trạng Còn trống (FR) vào dropdown."],
    ["Số lượng khách ở", "Select Dropdown", "Tối đa 3 khách", "Khống chế tối đa 3 khách/phòng theo đúng quy định Yêu cầu 2."],
    ["Ngày nhận & Số ngày", "Date / Number", "Ngày nhận >= hiện tại", "Xác định khoảng thời gian lưu trú dự kiến."],
    ["Bảng danh sách khách", "Dynamic Table", "1 đến 3 khách", "Ghi nhận đầy đủ STT, Họ tên, Loại khách (Nội địa/Quốc tế), CMND, Địa chỉ của từng người ở."]
]
format_table(tbl4, [1.5, 1.2, 1.6, 2.2], tbl4_headers, tbl4_data)

# 3. THIẾT KẾ XỬ LÝ PHIẾU THUÊ PHÒNG
p_xl4 = doc.add_paragraph()
p_xl4.paragraph_format.space_before = Pt(8)
r_xl4 = p_xl4.add_run("2. Thiết kế xử lý cho màn hình Lập phiếu thuê phòng (Processing Design)")
r_xl4.bold = True
r_xl4.font.size = Pt(10.5)

tbl_bc4 = doc.add_table(rows=4, cols=4)
tbl_bc4_headers = ["Tên biến cố / Sự kiện", "Đối tượng kích hoạt", "Dữ liệu đầu vào (Input)", "Hành động xử lý hệ thống"]
tbl_bc4_data = [
    ["Form_Load", "Trình duyệt (GET /thuephong)", "None", "Truy vấn danh sách phòng trống Phong.filter_by(TinhTrang='FR') để nạp vào dropdown."],
    ["btnTraCuuDatPhong_Click", "Nút 'Tra cứu'", "kw (họ tên/SĐT)", "Truy vấn bảng DatPhong với DaNhanPhong==False, nạp thông tin phiếu đặt lên giao diện."],
    ["btnLapPhieuThue_Click", "Nút 'LẬP PHIẾU THUÊ' (POST /thuephong)", "ma_phong, so_luong, ngay_thue, so_ngay, danh_sach_khach[]", "Kiểm tra số khách <= 3, kiểm tra quốc tịch, lưu ChiTietThue, cập nhật Phong.TinhTrang='IU' và DatPhong.DaNhanPhong=True."]
]
format_table(tbl_bc4, [1.6, 1.4, 1.6, 1.9], tbl_bc4_headers, tbl_bc4_data)

doc.add_paragraph().paragraph_format.space_after = Pt(2)
doc.add_paragraph("Thuật toán kiểm tra & lập phiếu thuê phòng (btnLapPhieuThue_Click):").runs[0].bold = True

add_code_block(doc,
"Bước 1: Tiếp nhận dữ liệu phiếu thuê:\n"
"        ma_phong, ho_ten, cmnd, dia_chi, so_luong, ngay_bat_dau, so_ngay, danh_sach_khach[], ma_dat_phong.\n"
"Bước 2: Kiểm tra ràng buộc hợp lệ:\n"
"        - Nếu so_luong < 1 hoặc so_luong > 3: Báo lỗi 'Quy định mỗi phòng chỉ ở tối đa 3 khách!'\n"
"        - Phòng thuê phải tồn tại và có TinhTrang == 'FR' (Còn trống). Nếu đang 'IU' -> Báo lỗi.\n"
"        - Kiểm tra họ tên và CMND của khách đại diện không được để trống.\n"
"Bước 3: Xác định phòng có khách nước ngoài hay không:\n"
"        co_nuoc_ngoai = False\n"
"        Duyệt qua danh_sach_khach: nếu bất kỳ khách nào có loai_khach == 'Nước ngoài' (hoặc mã 2):\n"
"            co_nuoc_ngoai = True\n"
"Bước 4: Mở Transaction CSDL (Atomic Transaction):\n"
"        1. Tạo bản ghi ChiTietThue:\n"
"           ct = ChiTietThue(MaPhong=ma_phong, HoTen=ho_ten, CMND=cmnd, DiaChi=dia_chi,\n"
"                            NgayBatDau=ngay_bat_dau, SoNgayODuKien=so_ngay, SoLuong=so_luong,\n"
"                            CoKhachNuocNgoai=co_nuoc_ngoai, DanhSachKhach=json.dumps(danh_sach_khach),\n"
"                            MaDatPhong=ma_dat_phong)\n"
"           db.session.add(ct)\n"
"        2. Cập nhật trạng thái phòng: Phong.query.get(ma_phong).TinhTrang = 'IU' (Đang thuê)\n"
"        3. Nếu có ma_dat_phong: DatPhong.query.get(ma_dat_phong).DaNhanPhong = True\n"
"        4. db.session.commit()\n"
"Bước 5: Chuyển hướng đến trang in phiếu thuê: /phieuthuephong/{ct.MaHopDong}."
)

add_callout(
    doc,
    "Quy định Yêu cầu 2: Có 2 loại khách (nội địa và nước ngoài), mỗi phòng được ở tối đa 3 khách. "
    "Khi lập phiếu thuê phòng, hệ thống tự động khóa trạng thái phòng sang 'IU' để đảm bảo tính toàn vẹn dữ liệu, không cho phép phòng này xuất hiện trong danh sách phòng trống cho đến khi hoàn tất thanh toán hóa đơn.",
    bold_title="RÀNG BUỘC YÊU CẦU 2: "
)

# ==================== MÀN HÌNH 5: HÓA ĐƠN ====================
doc.add_page_break()
h6 = doc.add_heading("VI. MÀN HÌNH UI-05: HÓA ĐƠN THANH TOÁN (INVOICE)", level=1)

img5_path = "mockup_images/mockup_05_hoa_don.png"
if os.path.exists(img5_path):
    p_img5 = doc.add_paragraph()
    p_img5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(img5_path, width=Inches(6.0))
    p_cap5 = doc.add_paragraph()
    p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap5 = p_cap5.add_run("Hình 5. Bản vẽ Mockup Giao diện Hóa đơn thanh toán (UI-05)")
    r_cap5.italic = True
    r_cap5.font.size = Pt(9)

p_t5 = doc.add_paragraph()
r5 = p_t5.add_run("1. Đặc tả thành phần dữ liệu Hóa đơn thanh toán")
r5.bold = True
r5.font.size = Pt(10.5)

tbl5 = doc.add_table(rows=5, cols=4)
tbl5_headers = ["Khoản mục", "Cách tính", "Công thức mẫu", "Ý nghĩa nghiệp vụ"]
tbl5_data = [
    ["Tiền phòng cơ bản", "Đơn giá x Số ngày ở", "350.000 đ x 3 = 1.050.000 đ", "Đơn giá phòng tiêu chuẩn dành cho 2 người ở."],
    ["Phụ thu khách thứ 3", "+25% Đơn giá", "1.050.000 đ x 25% = +262.500 đ", "Áp dụng khi phòng có 3 khách lưu trú (khách thứ 3)."],
    ["Hệ số khách nước ngoài", "Nhân hệ số 1.5", "(1.050.000 + 262.500) x 1.5", "Áp dụng nếu trong phòng có ít nhất 1 khách là người nước ngoài."],
    ["TỔNG TIỀN PHẢI THU", "Thành tiền cuối cùng", "= 1.968.750 VNĐ", "Số tiền thực thu của khách, lưu vào bảng HoaDon."]
]
format_table(tbl5, [1.5, 1.4, 1.8, 1.8], tbl5_headers, tbl5_data)

# 3. THIẾT KẾ XỬ LÝ HÓA ĐƠN
p_xl5 = doc.add_paragraph()
p_xl5.paragraph_format.space_before = Pt(8)
r_xl5 = p_xl5.add_run("2. Thiết kế xử lý cho màn hình Hóa đơn thanh toán (Processing Design)")
r_xl5.bold = True
r_xl5.font.size = Pt(10.5)

tbl_bc5 = doc.add_table(rows=3, cols=4)
tbl_bc5_headers = ["Tên biến cố / Sự kiện", "Đối tượng kích hoạt", "Dữ liệu đầu vào (Input)", "Hành động xử lý hệ thống"]
tbl_bc5_data = [
    ["Page_Load_HoaDon", "Trình duyệt (GET /hoadon/<ma_hop_dong>)", "MaHopDong", "Truy vấn ChiTietThue, tính số ngày ở thực tế, kiểm tra phụ thu 25% (khách 3), kiểm tra hệ số 1.5 (khách nước ngoài), tính Thành tiền."],
    ["btnXacNhanThanhToan_Click", "Nút 'XÁC NHẬN ĐÃ THU TIỀN' (POST /hoadon/<ma_hop_dong>)", "MaHopDong, ThanhTien", "Tạo bản ghi HoaDon, đổi TinhTrang phòng từ 'IU' về lại 'FR' (Còn trống), hoàn tất chu trình thuê phòng."]
]
format_table(tbl_bc5, [1.6, 1.4, 1.6, 1.9], tbl_bc5_headers, tbl_bc5_data)

doc.add_paragraph().paragraph_format.space_after = Pt(2)
doc.add_paragraph("Thuật toán tính toán chi phí & xuất hóa đơn (Yêu cầu 3):").runs[0].bold = True

add_code_block(doc,
"Bước 1: Lấy hợp đồng thuê: ct = ChiTietThue.query.get(ma_hop_dong)\n"
"Bước 2: Lấy thông tin phòng và loại phòng:\n"
"        phong = Phong.query.get(ct.MaPhong)\n"
"        don_gia = phong.LoaiPhong.DonGia\n"
"Bước 3: Tính số ngày ở thực tế:\n"
"        ngay_tra = datetime.now().date()\n"
"        so_ngay_o = max(1, (ngay_tra - ct.NgayBatDau.date()).days)\n"
"Bước 4: Áp dụng quy tắc Phụ thu khách thứ 3:\n"
"        Nếu ct.SoLuong >= 3:\n"
"            ty_le_phu_thu = 0.25 (25%)\n"
"        Ngược lại: ty_le_phu_thu = 0.0\n"
"Bước 5: Áp dụng quy tắc Hệ số khách nước ngoài:\n"
"        Nếu ct.CoKhachNuocNgoai == True:\n"
"            he_so = 1.5\n"
"        Ngược lại: he_so = 1.0\n"
"Bước 6: Tính tổng tiền thanh toán theo công thức Yêu cầu 3:\n"
"        tien_phong = don_gia * so_ngay_o\n"
"        tien_sau_phu_thu = tien_phong * (1 + ty_le_phu_thu)\n"
"        thanh_tien = round(tien_sau_phu_thu * he_so)\n"
"Bước 7: Khi bấm 'XÁC NHẬN ĐÃ THU TIỀN':\n"
"        1. Tạo HoaDon(MaHopDong=ct.MaHopDong, NgayTraPhong=now(), SoNgayO=so_ngay_o,\n"
"                       DonGia=don_gia, TyLePhuThu=ty_le_phu_thu, HeSo=he_so, ThanhTien=thanh_tien)\n"
"        2. Cập nhật phòng: phong.TinhTrang = 'FR' (Giải phóng phòng về trạng thái trống)\n"
"        3. db.session.commit()\n"
"Bước 8: Chuyển hướng sang màn hình xem/in hóa đơn thanh toán thành công: /inhoadon/{ct.MaHopDong}."
)

add_callout(
    doc,
    "Công thức tính tiền theo Yêu cầu 3:\n"
    "Thành tiền = Đơn giá x Số ngày ở x (1 + Phụ thu khách thứ 3) x Hệ số loại khách\n"
    "Ví dụ thực tế: Phòng Đôi 350.000 đ/ngày, ở 3 ngày, 3 khách (phụ thu 25%), có khách nước ngoài (hệ số 1.5):\n"
    "Thành tiền = 350.000 x 3 x (1 + 0.25) x 1.5 = 1.968.750 VNĐ.",
    bold_title="CÔNG THỨC TOÁN HỌC YÊU CẦU 3: "
)

# ==================== KẾT LUẬN ====================
doc.add_page_break()
h7 = doc.add_heading("VII. TỔNG KẾT VÀ BẢN ĐỒ LUỒNG DỮ LIỆU TOÀN HỆ THỐNG", level=1)
h7.paragraph_format.space_before = Pt(12)
h7.paragraph_format.space_after = Pt(8)

doc.add_paragraph(
    "Toàn bộ 5 màn hình giao diện cùng với thiết kế xử lý đã hình thành nên một chu trình khép kín, an toàn và tối ưu cho hệ thống Quản lý khách sạn MESP Hotel:"
)

# Bảng tổng hợp luồng xử lý
tbl_sum = doc.add_table(rows=6, cols=4)
tbl_sum_headers = ["Màn hình giao diện", "Vai trò tương tác", "Xử lý nghiệp vụ chính", "Thay đổi trạng thái CSDL"]
tbl_sum_data = [
    ["UI-01: Trang chủ", "Khách hàng / Vãng lai", "Tra cứu phòng, lọc tiêu chí, thêm giỏ phòng", "Không thay đổi (Read-only)"],
    ["UI-02: Đăng nhập", "Mọi đối tượng", "Xác thực MD5, tự động phân quyền Admin / Lễ tân / Khách", "Ghi nhận User Session đăng nhập"],
    ["UI-03: Đăng ký", "Khách hàng mới", "Thu thập CCCD, SĐT, tạo tài khoản thành viên", "Insert bảng Khach, TaiKhoanKhach"],
    ["UI-04: Lập phiếu thuê", "Nhân viên Lễ tân", "Khống chế tối đa 3 khách, kiểm tra quốc tịch, lập hợp đồng", "Insert ChiTietThue, Cập nhật Phong TinhTrang 'FR' -> 'IU'"],
    ["UI-05: Hóa đơn thanh toán", "Nhân viên Lễ tân", "Tính phụ thu 25%, nhân hệ số 1.5, thu tiền", "Insert HoaDon, Giải phóng Phong TinhTrang 'IU' -> 'FR'"]
]
format_table(tbl_sum, [1.5, 1.4, 2.0, 1.6], tbl_sum_headers, tbl_sum_data)

doc.add_paragraph().paragraph_format.space_after = Pt(10)
p_end = doc.add_paragraph(
    "Tài liệu này hoàn toàn khớp với mã nguồn thực tế đã được lập trình và kiểm thử trong hệ thống. "
    "Sinh viên có thể sử dụng trọn vẹn nội dung này để đưa vào Báo cáo môn học Công nghệ phần mềm, phục vụ đánh giá đồ án và bảo vệ trước hội đồng chấm thi."
)
p_end.runs[0].font.name = "Arial"
p_end.runs[0].font.size = Pt(9.5)

out_file = "MOCKUP_UI_QUAN_LY_KHACH_SAN.docx"
doc.save(out_file)
print(f"Updated document with full processing design: {out_file}")
