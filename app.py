import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from database import (
    get_supabase_client, get_user_profile, update_user_profile,
    get_all_users, get_documents, get_user_equipment
)
from functools import wraps

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key-change-in-production")

# Variables globales
APP_NAME = os.getenv("APP_NAME", "TSAR-U")
SUPABASE_CLIENT = get_supabase_client()


# ============ DECORADORES ============

def login_required(f):
    """Verificar que el usuario esté autenticado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def coordinador_required(f):
    """Verificar que el usuario sea coordinador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        
        # Obtener rol del usuario
        user_profile = get_user_profile(session["user_id"])
        if not user_profile or user_profile.get("rol") != "coordinador":
            return redirect(url_for("dashboard"))
        
        return f(*args, **kwargs)
    return decorated_function


# ============ RUTAS PÚBLICAS ============

@app.route("/")
def index():
    """Página de inicio"""
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Página de login"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        try:
            # Autenticar con Supabase
            response = SUPABASE_CLIENT.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                session["user_id"] = response.user.id
                session["email"] = response.user.email
                return redirect(url_for("dashboard"))
            else:
                return render_template("login.html", error="Credenciales inválidas")
        
        except Exception as e:
            print(f"Error en login: {e}")
            return render_template("login.html", error="Error en la autenticación")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Cerrar sesión"""
    try:
        SUPABASE_CLIENT.auth.sign_out()
    except:
        pass
    
    session.clear()
    return redirect(url_for("login"))


# ============ CREDENCIAL PÚBLICA ============

@app.route("/credencial/<user_id>")
def credencial_publica(user_id):
    """Página pública de credencial (escaneable por QR)"""
    try:
        user = get_user_profile(user_id)
        if not user:
            return "Credencial no encontrada", 404
        
        return render_template("credencial_publica.html", user=user)
    except Exception as e:
        print(f"Error obteniendo credencial: {e}")
        return "Error", 500


# ============ RUTAS PROTEGIDAS ============

@app.route("/dashboard")
@login_required
def dashboard():
    """Dashboard principal"""
    try:
        user = get_user_profile(session["user_id"])
        total_integrantes = len(get_all_users())
        documentos = get_documents()
        equipo_usuario = get_user_equipment(session["user_id"])
        
        return render_template("dashboard.html", 
                             user=user,
                             total_integrantes=total_integrantes,
                             documentos=documentos,
                             equipo_usuario=equipo_usuario)
    except Exception as e:
        print(f"Error en dashboard: {e}")
        return render_template("error.html", mensaje="Error cargando el dashboard"), 500


@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    """Perfil del usuario"""
    try:
        user = get_user_profile(session["user_id"])
        
        if request.method == "POST":
            # Actualizar perfil
            data = {
                "nombre_completo": request.form.get("nombre_completo"),
                "especialidades": request.form.get("especialidades"),
                "certificaciones": request.form.get("certificaciones"),
            }
            
            update_user_profile(session["user_id"], data)
            user = get_user_profile(session["user_id"])
            
            return render_template("perfil.html", user=user, success="Perfil actualizado")
        
        return render_template("perfil.html", user=user)
    except Exception as e:
        print(f"Error en perfil: {e}")
        return render_template("error.html", mensaje="Error cargando el perfil"), 500


@app.route("/integrantes")
@login_required
def integrantes():
    """Lista de integrantes"""
    try:
        integrantes = get_all_users()
        user = get_user_profile(session["user_id"])
        
        return render_template("integrantes.html", integrantes=integrantes, user=user)
    except Exception as e:
        print(f"Error obteniendo integrantes: {e}")
        return render_template("error.html", mensaje="Error cargando integrantes"), 500


@app.route("/documentos")
@login_required
def documentos():
    """Biblioteca de documentos"""
    try:
        docs = get_documents()
        user = get_user_profile(session["user_id"])
        
        return render_template("documentos.html", documentos=docs, user=user)
    except Exception as e:
        print(f"Error obteniendo documentos: {e}")
        return render_template("error.html", mensaje="Error cargando documentos"), 500


@app.route("/inventario")
@login_required
def inventario():
    """Gestión de inventario"""
    try:
        user = get_user_profile(session["user_id"])
        
        return render_template("inventario.html", user=user)
    except Exception as e:
        print(f"Error en inventario: {e}")
        return render_template("error.html", mensaje="Error cargando inventario"), 500


@app.route("/credencial")
@login_required
def credencial():
    """Credencial digital del usuario"""
    try:
        user = get_user_profile(session["user_id"])
        
        return render_template("credencial.html", user=user)
    except Exception as e:
        print(f"Error en credencial: {e}")
        return render_template("error.html", mensaje="Error cargando credencial"), 500


# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def pagina_no_encontrada(error):
    """Página 404"""
    return render_template("error.html", mensaje="Página no encontrada"), 404


@app.errorhandler(500)
def error_servidor(error):
    """Página 500"""
    return render_template("error.html", mensaje="Error del servidor"), 500


# ============ CONTEXT PROCESSORS ============

@app.context_processor
def inject_app_name():
    """Inyectar variables globales en templates"""
    return {
        "app_name": APP_NAME,
        "user_id": session.get("user_id"),
        "email": session.get("email")
    }


# ============ MAIN ============

if __name__ == "__main__":
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=5000)
