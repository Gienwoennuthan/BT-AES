from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Padding chuẩn PKCS7
def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Sai padding")
    return data[:-pad_len]

# Tạo khóa AES 256-bit từ mật khẩu
def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

# Hàm mã hóa file
def encrypt_file(key, in_filename, out_filename):
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    with open(in_filename, 'rb') as infile:
        data = infile.read()
    padded = pad(data)
    with open(out_filename, 'wb') as outfile:
        outfile.write(iv + encryptor.encrypt(padded))

# Hàm giải mã file
def decrypt_file(key, in_filename, out_filename):
    with open(in_filename, 'rb') as infile:
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        data = infile.read()
        decrypted = decryptor.decrypt(data)
        try:
            unpadded = unpad(decrypted)
        except Exception:
            raise ValueError("Sai mật khẩu hoặc file không hợp lệ")
    with open(out_filename, 'wb') as outfile:
        outfile.write(unpadded)

# Giao diện chính
@app.route('/')
def index():
    return render_template('web.html')

# Mã hóa
@app.route('/encrypt', methods=['POST'])
def encrypt():
    password = request.form['password']
    file = request.files['file']

    if not file or not password:
        return "Vui lòng chọn file và nhập khóa bảo mật.", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    out_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'encrypted_{filename}')
    encrypt_file(get_key(password), filepath, out_filename)

    return send_file(out_filename, as_attachment=True, download_name=f'encrypted_{filename}')

# Giải mã
@app.route('/decrypt', methods=['POST'])
def decrypt():
    password = request.form['password']
    file = request.files['file']

    if not file or not password:
        return "Vui lòng chọn file và nhập khóa bảo mật.", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    out_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'decrypted_{filename}')
    try:
        decrypt_file(get_key(password), filepath, out_filename)
    except Exception:
        return "Sai mật khẩu hoặc file không hợp lệ.", 400

    return send_file(out_filename, as_attachment=True, download_name=f'decrypted_{filename}')

if __name__ == '__main__':
    app.run(debug=True)
