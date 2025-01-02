from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dữ liệu mẫu (có thể thay bằng cơ sở dữ liệu thực tế)
users = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            return f"Chào mừng, {username}!"
        return "Đăng nhập thất bại!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if username in users:
            return "Tài khoản đã tồn tại!"
        
        if password != confirm_password:
            return "Mật khẩu xác nhận không khớp!"
        
        # Lưu thông tin người dùng
        users[username] = {
            'email': email,
            'phone': phone,
            'gender': gender,
            'address': address,
            'password': password
        }
        
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)