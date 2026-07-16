# TSAR-U - Team Search And Rescue Urban

🚨 Plataforma web para administración de grupos de rescate urbano.

## 🎯 Características

✅ **Autenticación segura** con Supabase Auth  
✅ **Gestión de integrantes** con perfiles personalizados  
✅ **Sistema de inventario** (personal y general)  
✅ **Biblioteca digital** de documentos  
✅ **Credenciales digitales** con código QR  
✅ **Dashboard intuitivo** con estadísticas  
✅ **Roles y permisos** (Coordinador y Rescatista)  
✅ **Diseño profesional** rojo, negro y gris  
✅ **Responsive** y optimizado para móvil  

## 🚀 Stack Tecnológico

- **Backend**: Python Flask
- **Base de datos**: Supabase PostgreSQL
- **Autenticación**: Supabase Auth
- **Almacenamiento**: Supabase Storage
- **Frontend**: HTML + CSS + JavaScript
- **Deploy**: Render

## 📁 Estructura del Proyecto

```
TSAR-U/
├── app.py                 # Aplicación principal Flask
├── database.py            # Funciones de base de datos
├── requirements.txt       # Dependencias Python
├── .env.example          # Variables de entorno (ejemplo)
├── .gitignore            # Archivos ignorados en Git
├── README.md             # Este archivo
│
├── templates/
│   ├── base.html         # Template base
│   ├── login.html        # Página de login
│   ├── dashboard.html    # Dashboard principal
│   ├── perfil.html       # Perfil del usuario
│   ├── integrantes.html  # Lista de integrantes
│   ├── credencial.html   # Credencial digital
│   ├── inventario.html   # Gestión de inventario
│   ├── documentos.html   # Biblioteca de documentos
│   ├── credencial_publica.html  # Credencial pública (QR)
│   └── error.html        # Página de error
│
└── static/
    ├── css/
    │   ├── style.css     # Estilos principales
    │   └── .gitkeep
    ├── js/
    │   ├── main.js       # JavaScript principal
    │   └── .gitkeep
    └── uploads/
        └── .gitkeep      # Directorio para uploads
```

## 🔧 Instalación y Setup

### Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes)
- Cuenta en Supabase
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/TSAR-U.git
cd TSAR-U
```

### Paso 2: Crear Entorno Virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

1. Copia `.env.example` a `.env`:

```bash
cp .env.example .env
```

2. Edita `.env` con tus credenciales de Supabase:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
FLASK_SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=development
APP_NAME=TSAR-U
```

### Paso 5: Configurar Supabase

#### Crear las tablas en Supabase:

Ve a tu proyecto Supabase → SQL Editor y ejecuta:

```sql
-- Tabla de integrantes
CREATE TABLE integrantes (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    email TEXT NOT NULL UNIQUE,
    nombre_completo TEXT NOT NULL,
    rol TEXT DEFAULT 'rescatista',
    cargo TEXT,
    especialidades TEXT,
    certificaciones TEXT,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado TEXT DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de inventario
CREATE TABLE inventario (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    cantidad INTEGER DEFAULT 0,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de asignaciones
CREATE TABLE asignaciones (
    id SERIAL PRIMARY KEY,
    integrante_id UUID REFERENCES integrantes(id),
    item_id INTEGER REFERENCES inventario(id),
    cantidad INTEGER DEFAULT 1,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de documentos
CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    url TEXT NOT NULL,
    tipo TEXT DEFAULT 'pdf',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📝 Uso

### Crear un Usuario

1. Ve a Supabase Auth
2. Crea un nuevo usuario con email y contraseña
3. El usuario se registrará automáticamente en la tabla `integrantes`

### Login

1. Accede a `http://localhost:5000/login`
2. Ingresa email y contraseña
3. Se abrirá el dashboard

### Navegación

- **Dashboard**: Resumen general
- **Integrantes**: Lista de rescatistas
- **Inventario**: Gestión de equipo
- **Documentos**: Biblioteca de archivos
- **Mi Perfil**: Editar información
- **Mi Credencial**: Ver credencial digital con QR

## 🔐 Seguridad

- ✅ Autenticación con Supabase Auth
- ✅ Sesiones Flask seguras
- ✅ Variables de entorno protegidas
- ✅ Protección de rutas con decoradores
- ✅ Validación de formularios

## 📦 Deploy en Render

### Paso 1: Preparar el Proyecto

```bash
# Crear archivo Procfile
echo "web: gunicorn app:app" > Procfile

# Crear archivo runtime.txt
echo "python-3.11.6" > runtime.txt
```

### Paso 2: Subir a GitHub

```bash
git add .
git commit -m "TSAR-U: Initial release"
git push origin main
```

### Paso 3: Deploy en Render

1. Ve a [Render.com](https://render.com)
2. Conecta tu repositorio GitHub
3. Crea un nuevo Web Service
4. Selecciona el repositorio `TSAR-U`
5. Configura las variables de entorno:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `FLASK_SECRET_KEY`
   - `FLASK_ENV=production`
6. Deploy

## 🛠️ Desarrollo

### Agregar una nueva ruta

```python
@app.route("/nueva-ruta")
@login_required
def nueva_funcion():
    return render_template("nueva.html")
```

### Conectarse a la base de datos

```python
from database import get_supabase_client

client = get_supabase_client()
response = client.table("integrantes").select("*").execute()
```

### Crear un nuevo template

```html
{% extends "base.html" %}

{% block title %}Mi Página{% endblock %}

{% block content %}
<h1>Contenido</h1>
{% endblock %}
```

## 🐛 Troubleshooting

### Error: "SUPABASE_URL no está configurado"

- Verifica que el archivo `.env` exista
- Comprueba que las variables estén correctas

### Error: "La conexión a la base de datos falló"

- Verifica tu conexión a internet
- Revisa que SUPABASE_URL y SUPABASE_KEY sean correctos
- Confirma que tu proyecto Supabase está activo

### Error 404 en rutas

- Asegúrate de que el template existe en `templates/`
- Verifica el nombre exacto del template

## 📚 Próximas Características

- [ ] Subida de fotos de perfil
- [ ] Reportes de incidentes
- [ ] Sistema de alertas
- [ ] Geolocalización
- [ ] Historial de actividades
- [ ] Admin panel avanzado

## 📄 Licencia

MIT License - Libre para usar y modificar

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama con tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte, abre un issue en el repositorio o contacta al equipo.

---

**TSAR-U** - Rescate Urbano en la Era Digital 🚨
