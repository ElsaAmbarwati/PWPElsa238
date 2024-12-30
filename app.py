from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Konfigurasi log
logging.basicConfig(level=logging.DEBUG)

# Inisialisasi Flask dan database
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/manajemen_pengguna'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

# Buat tabel database
def create_tables():
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            admin_user = User(
                username="admin",
                role="superadmin",
                email="admin@example.com",
                password_hash=generate_password_hash("admin123", method='pbkdf2:sha256')
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created: admin@example.com / admin123")
        else:
            print("Admin user already exists.")

# Rute Halaman Utama
@app.route('/')
def index():
    return render_template('index.html')

# Rute Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Selamat datang, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login gagal. Periksa email dan kata sandi Anda.', 'error')
    return render_template('login.html')

# Rute Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['data-username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, role=role, email=email, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Registrasi gagal. Email atau username sudah digunakan.', 'error')

    return render_template('register.html')

# Rute Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Anda harus login terlebih dahulu.', 'warning')
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('dashboard.html', users=users)

# Rute Tambah Pengguna
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if 'user_id' not in session:
        flash('Anda harus login terlebih dahulu.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, role=role, email=email, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Pengguna berhasil ditambahkan.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Gagal menambahkan pengguna. Email atau username sudah digunakan.', 'error')

    return render_template('tambah.html')

# Rute Edit Pengguna
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        flash('Anda harus login terlebih dahulu.', 'warning')
        return redirect(url_for('login'))

    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.role = request.form['role']
        user.email = request.form['email']

        try:
            db.session.commit()
            flash('Pengguna berhasil diperbarui.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Gagal memperbarui pengguna.', 'error')

    return render_template('edit.html', user=user)

# Rute Hapus
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    if 'user_id' not in session or session['role'] != 'superadmin':
        flash('Anda tidak memiliki izin untuk menghapus pengguna.', 'error')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Pengguna berhasil dihapus.', 'success')
    except Exception as e:
        flash('Gagal menghapus pengguna.', 'error')

    return redirect(url_for('dashboard'))

# Rute Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('index'))

# Main Program
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)