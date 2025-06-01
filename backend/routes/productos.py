
from flask import Blueprint, jsonify, request
from models.db import get_connection

productos_bp = Blueprint("productos", __name__)

# Obtener todos los productos
@productos_bp.route("/", methods=["GET"])
def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)

# Obtener producto por ID
@productos_bp.route("/<int:id>", methods=["GET"])
def obtener_producto(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado:
        return jsonify(resultado)
    return jsonify({"error": "Producto no encontrado"}), 404

# Crear nuevo producto (solo admin)
@productos_bp.route("/", methods=["POST"])
def crear_producto():
    data = request.get_json()
    usuario_id = data.get("usuario_id")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verificar si es admin
    cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()

    if not usuario or usuario["rol"] != "admin":
        cursor.close()
        conn.close()
        return jsonify({"error": "Acceso no autorizado"}), 403

    nombre = data.get("nombre")
    valor = data.get("valor")
    existencia = data.get("existencia")
    urlImagen = data.get("urlImagen")

    cursor.execute(
        "INSERT INTO productos (nombre, valor, existencia, urlImagen) VALUES (%s, %s, %s, %s)",
        (nombre, valor, existencia, urlImagen)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Producto creado correctamente"}), 201

# Eliminar producto (opcional)
@productos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Producto eliminado correctamente"})
