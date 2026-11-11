function addToCart(maPhong, maLoaiPhong) {
    fetch("/api/add-item-cart", {
        method: "POST",
        body: JSON.stringify({
            "MaPhong": maPhong,
            "MaLoaiPhong": maLoaiPhong
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if (data.error_code === 200) {
            let counter = document.getElementById("cartCounter");
            if (counter) {
                counter.innerText = data.cart_stats.total_quantity;
            }
            alert("Đã thêm phòng vào giỏ thành công!");
        } else {
            alert(data.message || "Phòng không khả dụng!");
        }
    }).catch(err => {
        alert("Lỗi kết nối máy chủ!");
    });
}

function updateCartItem(maPhong, ngayBatDau, quantity, soLuong) {
    fetch("/api/update-cart-item", {
        method: "PUT",
        body: JSON.stringify({
            "MaPhong": maPhong,
            "NgayBatDau": String(ngayBatDau),
            "quantity": parseInt(quantity),
            "SoLuong": parseInt(soLuong)
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if (data.error_code === 200) {
            location.reload();
        } else {
            alert("Cập nhật thất bại!");
        }
    });
}

function deleteCartItem(maPhong) {
    if (confirm("Bạn có chắc chắn muốn xóa phòng này khỏi giỏ?")) {
        fetch("/api/delete-cart-item/" + maPhong, {
            method: "DELETE"
        }).then(res => res.json()).then(data => {
            if (data.error_code === 200) {
                location.reload();
            } else {
                alert("Xóa thất bại!");
            }
        });
    }
}
