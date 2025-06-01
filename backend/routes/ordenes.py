
from flask import Blueprint, request, jsonify
from models.db import get_connection

ordenes_bp = Blueprint("ordenes", __name__)

@ordenes_bp.route("/", methods=["POST"])
def crear_orden():
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    items = data.get("items", [])

    if not usuario_id or not items:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()
    if not usuario:
        return jsonify({"error": "Usuario inválido"}), 403

    total = sum(item["cantidad"] * item["precio_unitario"] for item in items)
    cursor.execute("INSERT INTO ordenes (usuario_id, total) VALUES (%s, %s)", (usuario_id, total))
    orden_id = cursor.lastrowid

    for item in items:
        cursor.execute("""
            INSERT INTO orden_detalle (orden_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (orden_id, item["producto_id"], item["cantidad"], item["precio_unitario"]))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Orden registrada correctamente"}), 201
