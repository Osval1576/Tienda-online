
from flask import Blueprint, request, jsonify
from models.db import get_connection

ordenes_historial_bp = Blueprint("ordenes_h", __name__)

@ordenes_historial_bp.route("/<int:usuario_id>", methods=["GET"])
def obtener_ordenes(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Validar usuario
    cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
    if not cursor.fetchone():
        return jsonify({"error": "Usuario no válido"}), 403

    # Obtener órdenes con detalles
    cursor.execute("""
        SELECT o.id AS orden_id, o.total, o.fecha, p.nombre, od.cantidad, od.precio_unitario
        FROM ordenes o
        JOIN orden_detalle od ON o.id = od.orden_id
        JOIN productos p ON p.id = od.producto_id
        WHERE o.usuario_id = %s
        ORDER BY o.fecha DESC
    """, (usuario_id,))

    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    # Agrupar productos por orden
    ordenes = {}
    for fila in datos:
        oid = fila["orden_id"]
        if oid not in ordenes:
            ordenes[oid] = {
                "orden_id": oid,
                "fecha": fila["fecha"],
                "total": fila["total"],
                "items": []
            }
        ordenes[oid]["items"].append({
            "nombre": fila["nombre"],
            "cantidad": fila["cantidad"],
            "precio_unitario": fila["precio_unitario"]
        })

    return jsonify(list(ordenes.values()))
