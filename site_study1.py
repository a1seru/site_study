from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder="D:\\site_study\\static")

app.secret_key = 'секретный_ключ'  # Защита сессий

# Подключение базы SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Создаем базу при первом запуске
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index_study.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))  # если юзер уже залогинен, не отправлять его на login
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # проверяем данные
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash("Неверные данные, попробуйте снова.", "error")

    return render_template('index_study.html')  # отрисовываем страницу логина

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            # Проверяем, существует ли уже пользователь с таким именем
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Пользователь с таким именем уже существует!", "error")
                return redirect(url_for("register"))

            # Если пользователя нет, создаем нового
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Регистрация успешна!", "success")
            return redirect(url_for("login"))  # Перенаправление на страницу входа

    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Войдите в систему!", "error")
        return redirect(url_for('login'))  # если не залогинен — отправляем на вход
    
    user = User.query.get(session['user_id'])  # получаем пользователя из БД
    return render_template("dashboard.html", username=user.username)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) # python site_study1.py
