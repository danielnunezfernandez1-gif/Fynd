from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, Email
import sqlite3
import os

# ---------------------------------------------------------
# CONFIGURACIÓN BASE
# ---------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

DB_NAME = "fynd.db"


# ---------------------------------------------------------
# BASE DE DATOS — CREACIÓN AUTOMÁTICA
# ---------------------------------------------------------
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT,
            bio TEXT
        )""")

        conn.commit()
        conn.close()


init_db()


# ---------------------------------------------------------
# SISTEMA DE LOGIN
# ---------------------------------------------------------
class User(UserMixin):
    def __init__(self, id_, username, email, password, bio):
        self.id = id_
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return User(*row)
    return None


# ---------------------------------------------------------
# FORMULARIOS
# ---------------------------------------------------------
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=30)])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class EditProfileForm(FlaskForm):
    bio = TextAreaField("Biography")
    submit = SubmitField("Save Changes")


# ---------------------------------------------------------
# RUTAS
# ---------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("INSERT INTO users (username, email, password, bio) VALUES (?, ?, ?, '')",
                  (form.username.data, form.email.data, form.password.data))

        conn.commit()
        conn.close()

        flash("Account created!", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email=? AND password=?", 
                  (form.email.data, form.password.data))

        row = c.fetchone()
        conn.close()

        if row:
            user = User(*row)
            login_user(user)
            return redirect(url_for("profile"))
        else:
            flash("Incorrect email or password", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("UPDATE users SET bio=? WHERE id=?", (form.bio.data, current_user.id))
        conn.commit()
        conn.close()

        flash("Profile updated!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", form=form)


# ---------------------------------------------------------
# OTRAS SECCIONES (solo visual — botones sin funcionalidad)
# ---------------------------------------------------------
@app.route("/my_businesses")
@login_required
def my_businesses():
    return render_template("my_businesses.html")


@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")


@app.route("/job_offers")
def job_offers():
    return render_template("job_offers.html")


# ---------------------------------------------------------
# INICIO
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
