from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static'))

app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index_study.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.password == password: 
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash("Неверные данные, попробуйте снова.", "error")

    return render_template('index_study.html') 
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Пользователь с таким именем уже существует!", "error")
                return redirect(url_for("register"))
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Регистрация успешна!", "success")
            return redirect(url_for("login")) 

    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Войдите в систему!", "error")
        return redirect(url_for('login'))  
    
    user = User.query.get(session['user_id']) 
    return render_template("dashboard.html", username=user.username)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
