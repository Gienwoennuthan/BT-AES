# Công chúa AES

Ứng dụng web mã hóa và giải mã file sử dụng thuật toán AES-256 (CBC, PKCS7 padding) với Flask.

## Tính năng

- Mã hóa file với mật khẩu bí mật, xuất file đã mã hóa.
- Giải mã file đã mã hóa với đúng mật khẩu, xuất file gốc.
- Giao diện web thân thiện, dễ sử dụng.

## Yêu cầu

- Python 3.x
- Flask
- pycryptodome
- werkzeug

Cài đặt nhanh các thư viện:
```sh
pip install flask pycryptodome werkzeug
```

## Cách sử dụng

1. Chạy ứng dụng:
    ```sh
    python AES.py
    ```
2. Mở trình duyệt và truy cập: [http://127.0.0.1:5000](http://127.0.0.1:5000)
3. Chọn file, nhập mật khẩu và nhấn "Mã hóa" hoặc "Giải mã" để tải về file kết quả.

## Cấu trúc thư mục

```
AES.py
templates/
    web.html
uploads/
    (chứa file upload, file mã hóa/giải mã)
```

## Lưu ý

- Mật khẩu dùng để tạo khóa AES-256, hãy giữ bí mật.
- Không chia sẻ file mã hóa nếu không muốn lộ nội dung.

---

**Chúc bạn sử dụng vui vẻ! 👑**!
[image](https://github.com/user-attachments/assets/27e26aed-be47-457f-8f3e-4fb9ffbf8cae)
