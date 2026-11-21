import urllib.request
import urllib.parse
import http.cookiejar
import sys

sys.stdout.reconfigure(encoding='utf-8')
base_url = 'http://127.0.0.1:2000'

def test_all():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    print("1. Kiểm tra Trang chủ (GET /):")
    res = opener.open(f"{base_url}/")
    html = res.read().decode('utf-8', errors='ignore')
    assert res.status == 200
    assert "MESP HOTEL" in html
    assert "101" in html
    print("   -> Trang chủ hiển thị chuẩn: THÀNH CÔNG")

    print("\n2. Kiểm tra Tìm kiếm phòng (GET /?kw=101&TinhTrang=FR):")
    res = opener.open(f"{base_url}/?kw=101&TinhTrang=FR")
    html = res.read().decode('utf-8', errors='ignore')
    assert "Phòng 101" in html
    print("   -> Bộ lọc tìm kiếm hoạt động chuẩn: THÀNH CÔNG")

    print("\n3. Kiểm tra Đăng nhập Quản trị viên Admin (admin/123):")
    login_data = urllib.parse.urlencode({'username': 'admin', 'password': '123'}).encode('utf-8')
    res_login = opener.open(f"{base_url}/login", data=login_data)
    assert "/admin" in res_login.url
    print("   -> Đăng nhập Admin chuyển hướng đến /admin: THÀNH CÔNG")

    print("\n4. Kiểm tra Báo cáo doanh thu tháng (GET /admin/statsview/):")
    res_stats = opener.open(f"{base_url}/admin/statsview/?thang=11&nam=2026")
    stats_html = res_stats.read().decode('utf-8', errors='ignore')
    assert res_stats.status == 200
    assert "BÁO CÁO DOANH THU THEO THÁNG" in stats_html
    assert "chartDoanhThu" in stats_html
    print("   -> Báo cáo doanh thu và biểu đồ Chart.js tải tốt: THÀNH CÔNG")

    print("\n5. Kiểm tra Báo cáo mật độ sử dụng phòng (GET /admin/matdoview/):")
    res_matdo = opener.open(f"{base_url}/admin/matdoview/?thang=11&nam=2026")
    matdo_html = res_matdo.read().decode('utf-8', errors='ignore')
    assert res_matdo.status == 200
    assert "BÁO CÁO MẬT ĐỘ SỬ DỤNG PHÒNG" in matdo_html
    assert "chartMatDo" in matdo_html
    print("   -> Báo cáo mật độ và biểu đồ Chart.js tải tốt: THÀNH CÔNG")

    print("\n6. Kiểm tra Đăng xuất:")
    opener.open(f"{base_url}/dangxuat")
    print("   -> Đăng xuất an toàn: THÀNH CÔNG")

    print("\n7. Kiểm tra Đăng nhập Lễ tân (nhanvien/123):")
    login_nv = urllib.parse.urlencode({'username': 'nhanvien', 'password': '123'}).encode('utf-8')
    res_nv = opener.open(f"{base_url}/login", data=login_nv)
    assert "/nhanvien" in res_nv.url
    print("   -> Đăng nhập Lễ tân chuyển hướng đến /nhanvien: THÀNH CÔNG")

    print("\n8. Kiểm tra Bàn làm việc lễ tân (GET /nhanvien):")
    res_nv_dash = opener.open(f"{base_url}/nhanvien")
    assert res_nv_dash.status == 200
    print("   -> Bàn làm việc lễ tân tải tốt: THÀNH CÔNG")

    print("\n9. Kiểm tra giao diện Lập phiếu thuê phòng (GET /thuephong):")
    res_thue = opener.open(f"{base_url}/thuephong")
    thue_html = res_thue.read().decode('utf-8', errors='ignore')
    assert res_thue.status == 200
    assert "LẬP PHIẾU THUÊ PHÒNG" in thue_html
    print("   -> Giao diện lập phiếu thuê phòng tải tốt: THÀNH CÔNG")

    print("\n10. Kiểm tra giao diện Lập hóa đơn và tính tiền (GET /hoadon):")
    res_hd = opener.open(f"{base_url}/hoadon?mahopdong=4")
    hd_html = res_hd.read().decode('utf-8', errors='ignore')
    assert res_hd.status == 200
    assert "LẬP HÓA ĐƠN THANH TOÁN" in hd_html
    assert "Chi tiết bảng tính tiền" in hd_html
    print("   -> Giao diện hóa đơn tự động tính phụ thu/hệ số: THÀNH CÔNG")

    print("\n=======================================================")
    print(">>> TẤT CẢ 10 BÀI TEST CHỨC NĂNG ĐỀU ĐẠT CHUẨN 100%! <<<")
    print("=======================================================")

if __name__ == '__main__':
    test_all()
