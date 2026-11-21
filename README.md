# HỆ THỐNG QUẢN LÝ KHÁCH SẠN (MESP HOTEL)

> **Báo cáo đồ án môn học: Công nghệ phần mềm (CNPM)**  
> **Trường Đại học Mở Thành phố Hồ Chí Minh (OU)**  
> **Sinh viên thực hiện:** Lê Thị Ngọc Quỳnh  
> **MSSV:** 2151010317  

---

## 📌 Giới thiệu đề tài
Hệ thống website **Quản lý khách sạn (MESP Hotel)** được xây dựng nhằm tin học hóa toàn diện quy trình vận hành khách sạn, bao gồm:
1. **Đặt phòng trực tuyến:** Tra cứu phòng theo nhiều tiêu chí (số phòng, loại phòng Đơn/Đôi/VIP, tình trạng, khoảng giá); khống chế thời gian nhận phòng không quá 28 ngày kể từ thời điểm đặt.
2. **Lập phiếu thuê phòng (Check-in):** Lập phiếu thuê cho khách vãng lai hoặc khách đã hẹn trước; hỗ trợ tối đa 3 khách/phòng và phân biệt khách nội địa / nước ngoài.
3. **Thanh toán tiền phòng (Check-out):** Tự động tính tiền phòng theo số ngày ở thực tế, phụ thu 25% cho khách thứ 3 và áp dụng hệ số 1.5 nếu phòng có khách quốc tế.
4. **Báo cáo thống kê:** Biểu đồ doanh thu theo tháng và mật độ sử dụng phòng trực quan (sử dụng Chart.js).
5. **Thay đổi quy định:** Cho phép Quản trị viên thay đổi số lượng, đơn giá các loại phòng, hệ số khách, tỷ lệ phụ thu và quản lý danh mục phòng.

---

## 🛠️ Công nghệ sử dụng (Tech Stack)
* **Backend:** Python 3.12, Flask Framework, Flask-SQLAlchemy, Flask-Login, Flask-Admin
* **Database:** MySQL (Database: `dbks`)
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, FontAwesome 6, Chart.js
* **Kiến trúc:** Model - View - Controller (MVC)

---

## 🚀 Hướng dẫn cài đặt & Khởi chạy

### 1. Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

### 2. Cấu hình cơ sở dữ liệu MySQL:
Mở MySQL và khởi tạo cơ sở dữ liệu mẫu:
```bash
python init_db.py
```

### 3. Chạy ứng dụng web:
```bash
python my_app/index.py
```
Truy cập hệ thống tại trình duyệt: **`http://127.0.0.1:2000`**

---

## 🔑 Tài khoản mẫu kiểm thử hệ thống

| Vai trò (Role) | Tên đăng nhập (Username) | Mật khẩu (Password) | Trang đích sau khi đăng nhập |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin` | `123` | `/admin` (Quản trị hệ thống & Báo cáo) |
| **Nhân viên (Lễ tân)** | `nhanvien` | `123` | `/nhanvien` (Bàn làm việc Lễ tân) |
| **Khách hàng** | `khachhang` | `123` | `/` (Trang chủ & Đặt phòng trực tuyến) |

---

## 📄 Tài liệu đính kèm
* Bản vẽ Mockup UI trắng đen & Đặc tả xử lý giao diện: `MOCKUP_UI_QUAN_LY_KHACH_SAN.docx`
* Bản vẽ giao diện trực quan tương tác: `http://127.0.0.1:2000/mockup` (file `mockup_ui.html`)
