from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import os

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"  # Cambiar por una segura

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Usuario de ejemplo
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = f"User{id}"
        self.email = f"user{id}@example.com"

# Formas
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Registrarse")

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Rutas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(id=1)
        login_user(user)
        return redirect(url_for("dashboard"))
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(id=2)
        login_user(user)
        return redirect(url_for("dashboard"))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/my_businesses")
@login_required
def my_businesses():
    return render_template("my_businesses.html")

@app.route("/marketplace")
@login_required
def marketplace():
    return render_template("marketplace.html")

@app.route("/job_offers")
@login_required
def job_offers():
    return render_template("job_offers.html")

# Render deployment: host y puerto
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
