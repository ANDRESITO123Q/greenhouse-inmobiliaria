"""
routes/contacto.py
Formulario de contacto y publicación de inmuebles
"""
import re
from flask import Blueprint, jsonify, request
from datetime import datetime

bp = Blueprint('contacto', __name__)

# Almacén en memoria (reemplazar por DB en producción)
_MENSAJES = []

def ok(data, message="OK"):
    return jsonify({"status": "success", "message": message, "data": data})

def err(message, code=400):
    return jsonify({"status": "error", "message": message, "data": None}), code

def _validar_email(email):
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email or ''))

def _validar_telefono(tel):
    # Acepta formatos españoles: 6XXXXXXXX, 7XXXXXXXX, 8XXXXXXXX, 9XXXXXXXX
    return bool(re.match(r'^[6-9]\d{8}$', (tel or '').replace(' ', '').replace('-', '')))


@bp.route('/api/contacto', methods=['POST'])
def contacto():
    """Guardar y opcionalmente enviar mensaje de contacto."""
    body = request.get_json(silent=True) or {}

    nombre  = (body.get('nombre') or '').strip()
    email   = (body.get('email') or '').strip()
    telefono = (body.get('telefono') or '').strip()
    asunto  = (body.get('asunto') or '').strip()
    mensaje = (body.get('mensaje') or '').strip()

    # Validaciones
    errores = []
    if not nombre or len(nombre) < 2:
        errores.append("El nombre debe tener al menos 2 caracteres.")
    if not _validar_email(email):
        errores.append("El email no tiene un formato válido.")
    if telefono and not _validar_telefono(telefono):
        errores.append("El teléfono debe ser un número español válido (9 dígitos).")
    if not asunto:
        errores.append("El asunto es obligatorio.")

    if errores:
        return err("; ".join(errores))

    # Guardar
    registro = {
        "id": len(_MENSAJES) + 1,
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "asunto": asunto,
        "mensaje": mensaje,
        "fecha": datetime.now().isoformat(),
        "leido": False
    }
    _MENSAJES.append(registro)

    # Aquí iría el envío de email en producción
    # send_email(...)

    return ok(
        {"id": registro["id"]},
        f"Gracias {nombre}, hemos recibido tu mensaje. Te contactaremos en menos de 24 horas."
    )


@bp.route('/api/contacto/mensajes', methods=['GET'])
def get_mensajes():
    """[Admin] Listar todos los mensajes recibidos."""
    # En producción esto requeriría autenticación
    return ok({"mensajes": _MENSAJES, "total": len(_MENSAJES)})
