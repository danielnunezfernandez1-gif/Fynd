from flask import Flask, render_template, request, redirect, url_for
import os

# Configurar carpeta de templates y static
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesaria para formularios y sesiones

# ------------------------------
# Rutas principales
# ------------------------------

# Página de bienvenida / informativa
@app.route("/")
def index():
    return render_template("index.html")

# Dashboard después del login
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Perfil del usuario
@app.route("/profile")
def profile():
    return render_template("profile.html")

# Mis empresas
@app.route("/my_businesses")
def my_businesses():
    return render_template("my_businesses.html")

# Marketplace / Centro comercial
@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")

# Ofertas de trabajo
@app.route("/job_offers")
def job_offers():
    return render_template("job_offers.html")

# ------------------------------
# Rutas de autenticación
# ------------------------------

# Login
@app.route("/login")
def login():
    return render_template("login.html")

# Register / Crear cuenta
@app.route("/register")
def register():
    return render_template("register.html")

# ------------------------------
# Ejecutar la app
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)

