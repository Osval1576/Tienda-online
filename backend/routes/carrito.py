
from flask import Blueprint, jsonify, request
from models.db import get_connection

carrito_bp = Blueprint("carrito", __name__)

@carrito_bp.route("/<int:usuario_id>", methods=["GET"])
def obtener_carrito(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
    existe = cursor.fetchone()
    if not existe:
        return jsonify({"error": "Usuario no válido"}), 403

    cursor.execute("""
        SELECT c.id, c.producto_id, p.nombre, p.valor AS precio, p.urlImagen, c.cantidad
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
    """, (usuario_id,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)

@carrito_bp.route("/", methods=["POST"])
def agregar_al_carrito():
    data = request.get_json()
    usuario_id = data["usuario_id"]
    producto_id = data["producto_id"]
    cantidad = data.get("cantidad", 1)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cantidad FROM carrito 
        WHERE usuario_id = %s AND producto_id = %s
    """, (usuario_id, producto_id))
    resultado = cursor.fetchone()

    if resultado:
        nueva_cantidad = resultado[0] + cantidad
        cursor.execute("""
            UPDATE carrito SET cantidad = %s 
            WHERE usuario_id = %s AND producto_id = %s
        """, (nueva_cantidad, usuario_id, producto_id))
    else:
        cursor.execute("""
            INSERT INTO carrito (usuario_id, producto_id, cantidad)
            VALUES (%s, %s, %s)
        """, (usuario_id, producto_id, cantidad))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Producto agregado al carrito"}), 201

@carrito_bp.route("/<int:carrito_id>", methods=["DELETE"])
def eliminar_del_carrito(carrito_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carrito WHERE id = %s", (carrito_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Producto eliminado del carrito"}), 200

@carrito_bp.route("/vaciar/<int:usuario_id>", methods=["DELETE"])
def vaciar_carrito(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Carrito vaciado"}), 200
