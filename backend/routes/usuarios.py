from flask import Blueprint, request, jsonify
from models.db import get_connection
import hashlib

usuarios_bp = Blueprint("usuarios", __name__)

# Utilidad para encriptar contraseña (hash simple con SHA-256)
def encriptar_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

# Registrar un nuevo usuario
@usuarios_bp.route("/registro", methods=["POST"])
def registrar_usuario():
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    clave = encriptar_clave(data.get("clave"))
    direccion = data.get("direccion")
    telefono = data.get("telefono")

    conn = get_connection()
    cursor = conn.cursor()

    # Validar si el correo ya existe
    cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
    if cursor.fetchone():
        return jsonify({"error": "Correo ya registrado"}), 400

    cursor.execute("""
        INSERT INTO usuarios (nombre, correo, clave, direccion, telefono)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, correo, clave, direccion, telefono))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

# Iniciar sesión
@usuarios_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    clave = encriptar_clave(data.get("clave"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nombre, correo, direccion, telefono
        FROM usuarios
        WHERE correo = %s AND clave = %s
    """, (correo, clave))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401
