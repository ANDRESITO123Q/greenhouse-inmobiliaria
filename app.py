"""
Green House Inmobiliaria – Entry Point Flask
Ejecutar: python app.py  (dev)  |  gunicorn app:app  (prod)
"""

from flask import Flask, render_template
from flask_cors import CORS
from config import config
from routes import propiedades, contacto, tasacion, admin
import os

def create_app(env=None):
    app = Flask(__name__)
    env = env or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    # Secret key para sesiones
    app.secret_key = app.config['SECRET_KEY']

    # CORS – permite peticiones del frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar blueprints
    app.register_blueprint(propiedades.bp)
    app.register_blueprint(contacto.bp)
    app.register_blueprint(tasacion.bp)
    app.register_blueprint(admin.bp)

    # Rutas de vistas HTML
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/admin')
    def admin():
        return render_template('admin.html')

    # Manejo de errores JSON
    @app.errorhandler(404)
    def not_found(e):
        from flask import jsonify
        return jsonify({"status": "error", "message": "Recurso no encontrado", "data": None}), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import jsonify
        return jsonify({"status": "error", "message": "Error interno del servidor", "data": None}), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
