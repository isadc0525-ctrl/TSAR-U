import os
from supabase import create_client, Client

# Initializar cliente de Supabase
def get_supabase_client() -> Client:
    """Crea y retorna cliente de Supabase"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL y SUPABASE_KEY no están configuradas")
    
    return create_client(url, key)


def init_db():
    """
    Inicializa las tablas en Supabase.
    Ejecutar una sola vez al inicio.
    """
    client = get_supabase_client()
    
    # Las tablas se crean directamente en Supabase.
    # Este es un placeholder para futuras migraciones.
    print("Base de datos iniciada")


# ============ USUARIOS ============

def create_user(email: str, password: str, full_name: str, role: str = "rescatista"):
    """Crear nuevo usuario en Supabase Auth y tabla integrantes"""
    client = get_supabase_client()
    
    try:
        # Crear usuario en Auth
        user = client.auth.sign_up({
            "email": email,
            "password": password
        })
        
        # Crear registro en tabla integrantes
        if user.user:
            client.table("integrantes").insert({
                "id": user.user.id,
                "email": email,
                "nombre_completo": full_name,
                "rol": role,
                "estado": "activo"
            }).execute()
        
        return user
    except Exception as e:
        print(f"Error creando usuario: {e}")
        return None


def get_user_profile(user_id: str):
    """Obtener perfil del usuario"""
    client = get_supabase_client()
    
    try:
        response = client.table("integrantes").select("*").eq("id", user_id).single().execute()
        return response.data
    except Exception as e:
        print(f"Error obteniendo perfil: {e}")
        return None


def update_user_profile(user_id: str, data: dict):
    """Actualizar perfil del usuario"""
    client = get_supabase_client()
    
    try:
        response = client.table("integrantes").update(data).eq("id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error actualizando perfil: {e}")
        return None


def get_all_users(role: str = None):
    """Obtener todos los usuarios o filtrar por rol"""
    client = get_supabase_client()
    
    try:
        query = client.table("integrantes").select("*")
        if role:
            query = query.eq("rol", role)
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Error obteniendo usuarios: {e}")
        return []


# ============ INVENTARIO ============

def get_inventory_items(tipo: str = None):
    """Obtener items de inventario, filtrar por tipo (personal/general)"""
    client = get_supabase_client()
    
    try:
        query = client.table("inventario").select("*")
        if tipo:
            query = query.eq("tipo", tipo)
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Error obteniendo inventario: {e}")
        return []


def create_inventory_item(nombre: str, tipo: str, cantidad: int, descripcion: str = ""):
    """Crear nuevo item de inventario"""
    client = get_supabase_client()
    
    try:
        response = client.table("inventario").insert({
            "nombre": nombre,
            "tipo": tipo,
            "cantidad": cantidad,
            "descripcion": descripcion
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error creando item: {e}")
        return None


def assign_equipment(integrante_id: str, item_id: int, cantidad: int = 1):
    """Asignar equipo a un integrante"""
    client = get_supabase_client()
    
    try:
        response = client.table("asignaciones").insert({
            "integrante_id": integrante_id,
            "item_id": item_id,
            "cantidad": cantidad
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error asignando equipo: {e}")
        return None


def get_user_equipment(integrante_id: str):
    """Obtener equipos asignados a un usuario"""
    client = get_supabase_client()
    
    try:
        response = client.table("asignaciones").select("*, inventario(*)").eq("integrante_id", integrante_id).execute()
        return response.data
    except Exception as e:
        print(f"Error obteniendo equipo: {e}")
        return []


# ============ DOCUMENTOS ============

def get_documents():
    """Obtener todos los documentos"""
    client = get_supabase_client()
    
    try:
        response = client.table("documentos").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error obteniendo documentos: {e}")
        return []


def create_document(titulo: str, url: str, tipo: str = "pdf"):
    """Crear nuevo documento"""
    client = get_supabase_client()
    
    try:
        response = client.table("documentos").insert({
            "titulo": titulo,
            "url": url,
            "tipo": tipo
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error creando documento: {e}")
        return None
