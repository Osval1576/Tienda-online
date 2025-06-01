
from flask import Flask
from flask_cors import CORS

from routes.productos import productos_bp
from routes.usuarios import usuarios_bp
from routes.carrito import carrito_bp
from routes.ordenes import ordenes_bp
from routes.ordenes_historial import ordenes_historial_bp as ordenes_historial_bp

app = Flask(__name__)
CORS(app)

# Registrar blueprints
app.register_blueprint(productos_bp, url_prefix="/api/productos")
app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
app.register_blueprint(carrito_bp, url_prefix="/api/carrito")
app.register_blueprint(ordenes_bp, url_prefix="/api/ordenes")
app.register_blueprint(ordenes_historial_bp, url_prefix="/api/ordenes_h")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
