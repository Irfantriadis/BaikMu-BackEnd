import sqlite3
import subprocess
from flask import Flask, make_response, jsonify, render_template, session, request, redirect, url_for, send_file
from flask_restx import Resource, Api, reqparse
from flask_cors import  CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt, os,random
from flask_mail import Mail, Message

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1:3306/appkesmental"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'whateveryouwant'
# mail env config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "appkesehatanmental@gmail.com"
app.config['MAIL_PASSWORD'] = "kaqbvmmemgmvrler"
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
mail = Mail(app)
# mail env config
db = SQLAlchemy(app)

class Users(db.Model):
    id       = db.Column(db.Integer(), primary_key=True, nullable=False)
    nama     = db.Column(db.String(30), nullable=False)
    email    = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean(),nullable=False)
    createdAt = db.Column(db.Date)
    updatedAt = db.Column(db.Date)

SECRET_KEY      = "WhatEverYouWant"
ISSUER          = "myFlaskWebservice"
AUDIENCE_MOBILE = "myMobileApp"

import functools
import operator

#parserRegister
regParser = reqparse.RequestParser()
regParser.add_argument('nama', type=str, help='nama', location='json', required=True)
regParser.add_argument('email', type=str, help='Email', location='json', required=True)
regParser.add_argument('password', type=str, help='Password', location='json', required=True)
regParser.add_argument('confirm_password', type=str, help='Confirm Password', location='json', required=True)

@api.route('/register')
class Registration(Resource):
    @api.expect(regParser)
    def post(self):
        # BEGIN: Get request parameters.
        args        = regParser.parse_args()
        nama        = args['nama']
        email       = args['email']
        password    = args['password']
        password2   = args['confirm_password']
        is_verified = True

        # cek confirm password
        if password != password2:
            return {
                'messege': 'Password tidak cocok'
            }, 400

        #cek email sudah terdaftar
        user = db.session.execute(db.select(Users).filter_by(email=email)).first()
        if user:
            return "Email sudah terpakai silahkan coba lagi menggunakan email lain"
        user          = Users()
        user.nama     = nama
        user.email    = email
        user.password = generate_password_hash(password)
        user.is_verified = is_verified
        db.session.add(user)
        db.session.commit()
        return {'message':
            'Registrasi Berhasil. Silahkan login.'}, 200
        
logParser = reqparse.RequestParser()
logParser.add_argument('email', type=str, help='Email', location='json', required=True)
logParser.add_argument('password', type=str, help='Password', location='json', required=True)

@api.route('/login')
class LogIn(Resource):
    @api.expect(logParser)
    def post(self):
        args        = logParser.parse_args()
        email       = args['email']
        password    = args['password']
        # cek jika kolom email dan password tidak terisi
        if not email or not password:
            return {
                'message': 'Email Dan Password Harus Diisi'
            }, 400
        #cek email sudah ada
        user = db.session.execute(
            db.select(Users).filter_by(email=email)).first()
        if not user:
            return {
                'message': 'Email / Password Salah'
            }, 400
        else:
            user = user[0]
        #cek password
        if check_password_hash(user.password, password):
            if user.is_verified == True:
                token= jwt.encode({
                        "user_id":user.id,
                        "user_email":user.email,
                        "exp": datetime.utcnow() + timedelta(hours= 1)
                },app.config['SECRET_KEY'],algorithm="HS256")
                # Set session variables
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['token'] = token
                tup = email,":",password
                #toString
                data = functools.reduce(operator.add, tup)
                byte_msg = data.encode('ascii')
                base64_val = base64.b64encode(byte_msg)
                code = base64_val.decode('ascii')
                msg = Message(subject='Verification OTP', recipients=[user.email])
                session['email'] = user.email
                session['token'] = str(token)
                msg.html = render_template('verify_email.html', token=token)
                mail.send(msg)
                return {'message' : 'Login Berhasil',
                        'token' : token,
                        'code' : code
                        },200
            else:
                return {'message' : 'Email Belum Diverifikasi ,Silahka verifikasikan terlebih dahulu '},401
        else:
            return {
                'message': 'Email / Password Salah'
            }, 400

@app.route('/logout')
def logout():
    # Remove session variables
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('token', None)

    # Your other code here
    return redirect(url_for('login'))

otpparser = reqparse.RequestParser()
otpparser.add_argument('otp', type=str, help='otp', location='json', required=True)
@api.route('/verify')
class Verify(Resource):
    @api.expect(otpparser)
    def post(self):
        args = otpparser.parse_args()
        otp = args['otp']
        if 'token' in session:
            sesion = session['token']
            if otp == sesion:
                email = session['email']

                user = Users.query.filter_by(email=email).first()
                user.is_verified = True
                db.session.commit()
                session.pop('token',None)
                return {'message' : 'Email berhasil diverifikasi'}, 200
            else:
                return {'message' : 'Kode Otp Salah'},400
        else:
            return {'message' : 'Kode Otp Salah'},400
        
def decodetoken(jwtToken):
    decode_result = jwt.decode(
               jwtToken,
               app.config['SECRET_KEY'],
               algorithms = ['HS256'],
            )
    return decode_result

authParser = reqparse.RequestParser()
authParser.add_argument('Authorization', type=str, help='Authorization', location='headers', required=True)
@api.route('/bearer-auth')
class DetailUser(Resource):
       @api.expect(authParser)
       def get(self):
        args = authParser.parse_args()
        bearerAuth  = args['Authorization']
        try:
            jwtToken    = bearerAuth[7:]
            token = decodetoken(jwtToken)
            user =  db.session.execute(db.select(Users).filter_by(email=token['user_email'])).first()
            user = user[0]
            data = {
                'nama' : user.nama,
                'email' : user.email
            }
        except:
            return {
                'message' : 'Token Tidak valid,Silahkan Login Terlebih Dahulu!'
            }, 401

        return data, 200

import base64
parser4Basic = reqparse.RequestParser()
parser4Basic.add_argument('Authorization', type=str,
    location='headers', required=True, 
    help='Please, read https://swagger.io/docs/specification/authentication/basic-authentication/')
      
@api.route('/basic-auth')
class BasicAuth(Resource):
    @api.expect(parser4Basic)
    def post(self):
        args        = parser4Basic.parse_args()
        basicAuth   = args['Authorization']
        # basicAuth is "Basic bWlyemEuYWxpbS5tQGdtYWlsLmNvbTp0aGlzSXNNeVBhc3N3b3Jk"
        base64Str   = basicAuth[6:] # Remove first-6 digits (remove "Basic ")
        # base64Str is "bWlyemEuYWxpbS5tQGdtYWlsLmNvbTp0aGlzSXNNeVBhc3N3b3Jk"
        base64Bytes = base64Str.encode('ascii')
        msgBytes    = base64.b64decode(base64Bytes)
        pair        = msgBytes.decode('ascii')
        # pair is mirza.alim.m@gmail.com:thisIsMyPassword
        email, password = pair.split(':')
        # email is mirza.alim.m@gmail.com, password is thisIsMyPassword
        return {'email': email, 'password': password}

editParser = reqparse.RequestParser()
editParser.add_argument('nama', type=str, help='nama', location='json', required=True)
editParser.add_argument('Authorization', type=str, help='Authorization', location='headers', required=True)
@api.route('/edit-user')
class EditUser(Resource):
       @api.expect(editParser)
       def put(self):
        args = editParser.parse_args()
        bearerAuth  = args['Authorization']
        nama = args['nama']
        datenow =  datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        try:
            jwtToken    = bearerAuth[7:]
            token = decodetoken(jwtToken)
            user = Users.query.filter_by(email=token.get('user_email')).first()
            user.nama = nama
            user.updatedAt = datenow
            db.session.commit()
        except:
            return {
                'message' : 'Token Tidak valid,Silahkan Login Terlebih Dahulu!'
            }, 400
        return {'message' : 'Update User Sukses'}, 200


verifyParser = reqparse.RequestParser()
verifyParser.add_argument(
    'otp', type=str, help='OTP', location='json', required=True)

#editpasswordParser
editPasswordParser =  reqparse.RequestParser()
editPasswordParser.add_argument('current_password', type=str, help='current_password',location='json', required=True)
editPasswordParser.add_argument('new_password', type=str, help='new_password',location='json', required=True)
@api.route('/edit-password')
class Password(Resource):
    @api.expect(authParser,editPasswordParser)
    def put(self):
        args = editPasswordParser.parse_args()
        argss = authParser.parse_args()
        bearerAuth  = argss['Authorization']
        cu_password = args['current_password']
        newpassword = args['new_password']
        try:
            jwtToken    = bearerAuth[7:]
            token = decodetoken(jwtToken)
            user = Users.query.filter_by(id=token.get('user_id')).first()
            if check_password_hash(user.password, cu_password):
                user.password = generate_password_hash(newpassword)
                db.session.commit()
            else:
                return {'message' : 'Password Lama Salah'},400
        except:
            return {
                'message' : 'Token Tidak valid! Silahkan, Sign in!'
            }, 401
        return {'message' : 'Password Berhasil Diubah'}, 200

from flask import Flask, jsonify, render_template, request
# from flaskext.mysql import MySQL  # Import Flask-MySQL
# import os

# # MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'appkesmental'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Change to your MySQL host if needed
# app.config['UPLOAD_FOLDER'] = 'upload'

# # Initialize the MySQL extension
# mysql = SQLAlchemy(app)

@app.route('/delete_doctors/<int:doctors_id>', methods=['GET'])
def delete_psikolog(doctors_id):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    try:
        # Hapus artikel berdasarkan ID
        cursor.execute("DELETE FROM doctors WHERE id=%s", (doctors_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect kembali ke halaman "articles" setelah berhasil menghapus
        return redirect(url_for('get_doctors'))
    except Exception as e:
        return jsonify({'message': f'Gagal menghapus artikel: {str(e)}'}), 500
    
@app.route('/doctors', methods=['GET'])
def get_doctors():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    cur.execute('SELECT id, name, speciality, detail, google_maps_link FROM doctors')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('doctors.html', doctors=data)

@app.route('/doctors_mobile', methods=['GET'])
def get_doctors_mobile():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    cur.execute('SELECT id, name, speciality, detail, google_maps_link FROM doctors')
    data = cur.fetchall()
    doctors = []
    for row in data:
        doctor = {
            'id': row['id'],
            'name': row['name'],
            'speciality': row['speciality'],
            'detail': row['detail'],
            'google_maps_link': row['google_maps_link']
        }
        doctors.append(doctor)
    cur.close()
    return jsonify(doctors)

@app.route('/post-psikolog')
def post_doctors():
    return render_template('post-doctors.html')

@app.route('/post-doctors', methods=['POST'])
def add_doctor():
    if not request.is_json:
        return jsonify({'error': 'Request content-type must be application/json'}), 400
    
    data = request.get_json()
    
    required_fields = ['name', 'speciality', 'detail', 'google_maps_link']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='appkesmental',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        
        sql = """
        INSERT INTO doctors (name, speciality, detail, google_maps_link)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (data['name'], data['speciality'], data['detail'], data['google_maps_link']))
        conn.commit()
        
        new_doctor_id = cur.lastrowid
        
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Doctor added successfully',
            'id': new_doctor_id
        }), 201
    
    except pymysql.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


# Endpoint untuk mendapatkan semua artikel
@app.route('/articles', methods=['GET'])
def articles():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()

    # Convert the fetched data into a list of dictionaries (to match the current data structure)
    article_list = [{'id': row['id'], 'title': row['title'], 'content': row['content'], 'category': row['category'], 'link': row['link']} for row in articles]

    cursor.close()
    conn.close()

    return render_template('articles.html', articles=article_list)

# Endpoint untuk mendapatkan semua artikel
@app.route('/articlesmobile', methods=['GET'])
def get_articles():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    
    # Convert the fetched data into a list of dictionaries (to match the current data structure)
    article_list = [{'id': row['id'], 'title': row['title'], 'content': row['content'], 'category': row['category'], 'link': row['link']} for row in articles]
    
    cursor.close()
    conn.close()

    return jsonify(article_list)

@app.route('/articlesmobilebaru', methods=['GET'])
def get_articlesbaru():
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='appkesmental',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM articles ORDER BY id DESC")
        articles = cursor.fetchall()
        
        # Convert the fetched data into a list of dictionaries (to match the current data structure)
        article_list = [{'id': row['id'], 'title': row['title'], 'content': row['content'], 'category': row['category'], 'link': row['link']} for row in articles]
        
        cursor.close()
        conn.close()

        return jsonify(article_list)
    except Exception as e:
        return str(e), 500  


@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    try:
        if request.method == 'POST':
            # Proses perubahan artikel di sini
            title = request.form.get('title')
            content = request.form.get('content')
            category = request.form.get('category')
            link = request.form.get('link')

            cursor.execute("UPDATE articles SET title=%s, content=%s, category=%s, link=%s WHERE id=%s",
                           (title, content, category, link, article_id))
            conn.commit()

            # Redirect kembali ke halaman "articles" setelah berhasil mengedit
            return redirect(url_for('articles'))
        else:
            # Tampilkan halaman edit artikel
            cursor.execute("SELECT * FROM articles WHERE id=%s", (article_id,))
            article = cursor.fetchone()

            if not article:
                return jsonify({'message': 'Artikel tidak ditemukan'}), 404

            return render_template('edit-article.html', article=article)
    except Exception as e:
        return jsonify({'message': f'Gagal mengedit artikel: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()
        
@app.route('/delete_article/<int:article_id>', methods=['GET'])
def delete_article(article_id):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    try:
        # Hapus artikel berdasarkan ID
        cursor.execute("DELETE FROM articles WHERE id=%s", (article_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect kembali ke halaman "articles" setelah berhasil menghapus
        return redirect(url_for('articles'))
    except Exception as e:
        return jsonify({'message': f'Gagal menghapus artikel: {str(e)}'}), 500

# Endpoint untuk mendapatkan artikel berdasarkan ID
@app.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
        article = cursor.fetchone()
        
        if article:
            return jsonify({
                'id': article['id'],
                'title': article['title'],
                'content': article['content'],
                'category': article['category'],
                'link': article['link']
            })
        return jsonify({'message': 'Artikel tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'message': f'Gagal mengambil artikel: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/dashboard')
def dashboard():
    article_count = get_article_count()  # Dapatkan jumlah artikel
    return render_template('dashboard.html', article_count=article_count)


from flask import Flask, redirect, render_template

# Endpoint untuk Swagger/OpenAPI
@app.route('/swagger')
def swagger():
    # Logika untuk menampilkan dokumen Swagger/OpenAPI
    return "Dokumen Swagger/OpenAPI"

# Pengalihan langsung ke '/landing'
@app.route('/')
def index():
    return redirect('/landing')

@app.route('/landing')
def landing():
    return render_template('landing.html')


# visitor_count = 0

# @app.route('/home')
# def landing():
#     global visitor_count  # Gunakan variabel global

#     # Tambahkan 1 ke jumlah pengunjung
#     visitor_count += 1

#     return render_template('landing.html', visitor_count=visitor_count)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/post-article')
def postarticle():
    return render_template('post-article.html')

def get_article_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='appkesmental',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM articles")
        count = cursor.fetchone()[0]

        return count
    except Exception as e:
        print(f'Error in get_article_count: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

@app.route('/post_article', methods=['POST'])
def post_article():
    # Mendapatkan data dari formulir
    title = request.form.get('title')
    content = request.form.get('content')
    category = request.form.get('category')
    link = request.form.get('link')

    # Validasi data
    if not title or not content:
        return jsonify({'message': 'Judul dan konten artikel diperlukan'}), 400

    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    try:
        # Menyimpan artikel baru ke database
        cursor.execute("INSERT INTO articles (title, content, category, link) VALUES (%s, %s, %s, %s)",
                       (title, content, category, link))
        conn.commit()

        # Menutup kursor dan koneksi
        cursor.close()
        conn.close()

        # Mengarahkan kembali ke halaman HTML indeks setelah posting berhasil
        return redirect(url_for('articles'))
    except Exception as e:
        return jsonify({'message': f'Gagal memposting artikel: {str(e)}'}), 500


##RESET PASSWORD# atau modul lain sesuai dengan database Anda
from flask import request

# Fungsi untuk menyimpan token reset password ke dalam database
def save_reset_token(user_id, reset_token):
    # Membuat koneksi ke server MySQL
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    # Membuat kursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()

    # Eksekusi perintah SQL untuk menyimpan token reset ke dalam tabel reset_tokens
    cursor.execute(
        "INSERT INTO reset_tokens (user_id, token) VALUES (%s, %s)",
        (user_id, reset_token)
    )

    # Commit perubahan ke database
    conn.commit()

    # Tutup kursor dan koneksi
    cursor.close()
    conn.close()

# Endpoint baru untuk lupa password
import pymysql

def establish_db_connection():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        # Establish MySQL connection
        connection = establish_db_connection()
        cursor = connection.cursor()

        # Cek apakah email ada dalam database
        cursor.execute("SELECT * FROM Users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            # Generate token untuk reset password (dapat dienkripsi)
            reset_token = generate_reset_token(user['id'])
            # Simpan token di database
            save_reset_token(user['id'], reset_token)

            # Kirim email dengan tautan untuk reset password
            send_password_reset_email(user['email'], reset_token)

            # Tutup kursor dan koneksi
            cursor.close()
            connection.close()

            return render_template('forgot_password.html', message='Email pemulihan telah dikirim')
        else:
            # Tutup kursor dan koneksi
            cursor.close()
            connection.close()

            return render_template('forgot_password.html', error='Email tidak ditemukan')

    return render_template('forgot_password.html')

def send_password_reset_email(email, reset_token):
    reset_link = f"http://192.168.62.221:5000/reset-password?token={reset_token}"
    msg = Message(
        subject='Reset Password',
        sender=os.environ.get("MAIL_USERNAME"),
        recipients=[email]
    )
    msg.html = render_template('reset_password_email.html', reset_link=reset_link)
    mail.send(msg)

def generate_reset_token(user_id):
    return jwt.encode({
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token kadaluarsa dalam 1 jam
    }, app.config['SECRET_KEY'], algorithm="HS256")

@app.route('/reset-password', methods=['GET'])
def reset_password():
    token = request.args.get('token')

    if is_valid_reset_token(token):
        return render_template('reset_password.html', token=token)
    else:
        return "Invalid or expired token", 400
    
def is_valid_reset_token(token):
    if token_exists_in_database(token):
        if not token_expired(token):
            return True
    return False

import pymysql

def token_exists_in_database(token):
    # Membuat koneksi ke server MySQL
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    # Membuat kursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()

    # Eksekusi kueri untuk memeriksa apakah token ada dalam tabel reset_tokens
    cursor.execute("SELECT token FROM reset_tokens WHERE token = %s", (token,))
    token_entry = cursor.fetchone()

    # Tutup kursor dan koneksi
    cursor.close()
    conn.close()

    # Mengembalikan True jika token_entry tidak None, dan False jika None
    return token_entry is not None

def token_expired(token):
    return False

from flask import request, render_template, redirect, url_for, flash
import jwt
from datetime import datetime, timedelta
import pymysql
from werkzeug.security import generate_password_hash

# Fungsi untuk mengubah password
@app.route('/change-password', methods=['POST'])
def change_password():
    token = request.form.get('token')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Periksa kecocokan password
    if password != confirm_password:
        flash('Password and Confirm Password do not match', 'error')
        return redirect(url_for('reset_password', token=token))

    # Periksa kevalidan token
    if not is_valid_reset_token(token):
        flash('Invalid or expired token', 'error')
        return redirect(url_for('forgot_password'))

    # Decode token untuk mendapatkan user_id
    user_id = decode_reset_token(token)

    # Ubah password dalam database
    if update_password(user_id, password):
        flash('Password successfully changed', 'success')
    else:
        flash('Failed to change password. Please try again', 'error')

    return redirect(url_for('login'))  # Redirect ke halaman login setelah mengubah password

# Fungsi untuk mengubah password dalam database
def update_password(user_id, password):
    try:
        connection = establish_db_connection()
        cursor = connection.cursor()

        # Enkripsi password
        hashed_password = generate_password_hash(password)

        # Eksekusi perintah SQL untuk mengubah password
        cursor.execute("UPDATE Users SET password=%s WHERE id=%s", (hashed_password, user_id))
        connection.commit()

        cursor.close()
        connection.close()
        
        return True
    except Exception as e:
        print("Error updating password:", e)
        return False

# Fungsi untuk mendekode token dan mendapatkan user_id
def decode_reset_token(token):
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded.get('user_id')
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

@app.route('/post-video-meditasi')
def postmeditasi():
    return render_template('post-meditasi.html')

@app.route('/add_videos_meditasi', methods=['POST'])
def add_video_meditasi():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    title = request.form.get('title')
    channel_name = request.form.get('channel_name')
    video_id = request.form.get('video_id')
    thumbnail = request.form.get('thumbnail')
    
    # Membuat koneksi ke database
    cursor = conn.cursor()

    # Menjalankan query untuk menambahkan data video ke database
    sql = "INSERT INTO video_meditasi (title, channel_name, video_id, thumbnail) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (title, channel_name, video_id, thumbnail))
    
    # Commit perubahan ke database
    conn.commit()

    # Menutup koneksi ke database
    cursor.close()
    conn.close()

    return render_template('videos_meditasi.html')

@app.route('/videos_meditasi', methods=['GET'])
def videos_meditasi():
    # Membuat koneksi ke database
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # Menjalankan query untuk mendapatkan semua data video dari database
    cursor.execute("SELECT * FROM video_meditasi")
    videos = cursor.fetchall()

    # Convert the fetched data into a list of dictionaries (to match the current data structure)
    videos_list = [{'id': row['id'], 'title': row['title'], 'channel_name': row['channel_name'], 'video_id': row['video_id'], 'thumbnail': row['thumbnail']} for row in videos]

    # Menutup koneksi ke database
    cursor.close()
    conn.close()

    return render_template('videos_meditasi.html', videos=videos_list)

from flask import redirect, url_for

@app.route('/delete_video_meditasi/<int:video_id>', methods=['GET'])
def delete_video_meditasi(video_id):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    try:
        # Hapus video berdasarkan ID
        cursor.execute("DELETE FROM video_meditasi WHERE id=%s", (video_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect kembali ke halaman "videos_meditasi" setelah berhasil menghapus
        return redirect(url_for('videos_meditasi'))
    except Exception as e:
        return jsonify({'message': f'Gagal menghapus video: {str(e)}'}), 500

@app.route('/post-video-musik')
def postmusik():
    return render_template('post-musik.html')

@app.route('/add_videos_musik', methods=['POST'])
def add_video_musik():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    title = request.form.get('title')
    channel_name = request.form.get('channel_name')
    video_id = request.form.get('video_id')
    thumbnail = request.form.get('thumbnail')
    
    # Membuat koneksi ke database
    cursor = conn.cursor()

    # Menjalankan query untuk menambahkan data video ke database
    sql = "INSERT INTO video_musik (title, channel_name, video_id, thumbnail) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (title, channel_name, video_id, thumbnail))
    
    # Commit perubahan ke database
    conn.commit()

    # Menutup koneksi ke database
    cursor.close()
    conn.close()

    return render_template('videos_musik.html')

@app.route('/videos_musik', methods=['GET'])
def videos_musik():
    # Membuat koneksi ke database
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # Menjalankan query untuk mendapatkan semua data video dari database
    cursor.execute("SELECT * FROM video_musik")
    videos = cursor.fetchall()

    # Convert the fetched data into a list of dictionaries (to match the current data structure)
    videos_list = [{'id': row['id'], 'title': row['title'], 'channel_name': row['channel_name'], 'video_id': row['video_id'], 'thumbnail': row['thumbnail']} for row in videos]

    # Menutup koneksi ke database
    cursor.close()
    conn.close()

    return render_template('videos_musik.html', videos=videos_list)

@app.route('/delete_video_musik/<int:video_id>', methods=['GET'])
def delete_video_musik(video_id):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    try:
        # Hapus video berdasarkan ID
        cursor.execute("DELETE FROM video_musik WHERE id=%s", (video_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect kembali ke halaman "videos_meditasi" setelah berhasil menghapus
        return redirect(url_for('videos_musik'))
    except Exception as e:
        return jsonify({'message': f'Gagal menghapus video: {str(e)}'}), 500
    
@app.route('/videos_musik_mobile', methods=['GET'])
def videos_musik_mobile():
    # Membuat koneksi ke database
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # Menjalankan query untuk mendapatkan semua data video dari database
    cursor.execute("SELECT * FROM video_musik")
    videos = cursor.fetchall()

    # Menutup koneksi ke database
    cursor.close()
    conn.close()

    return jsonify(videos)
    
@app.route('/videos_meditasi_mobile', methods=['GET'])
def videos_meditasi_mobile():
    # Membuat koneksi ke database
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='appkesmental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # Menjalankan query untuk mendapatkan semua data video dari database
    cursor.execute("SELECT * FROM video_meditasi")
    videos = cursor.fetchall()

    # Menutup koneksi ke database
    cursor.close()
    conn.close()

    return jsonify(videos)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)