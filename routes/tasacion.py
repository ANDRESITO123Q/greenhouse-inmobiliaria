"""
routes/tasacion.py
Lógica de tasación estimada de inmuebles en Leganés

Metodología:
  Precio base por m² según tipo de inmueble
  × Factor de zona (zonas más céntricas valen más)
  × Factor de planta
  × Factor de extras (ascensor, terraza, piscina, garaje, jardín)
  ± Ajuste de mercado actual
"""
import re
from flask import Blueprint, jsonify, request
from datetime import datetime

bp = Blueprint('tasacion', __name__)

# ─────────────────────────────────────────────
# TABLAS DE REFERENCIA (valores estimados Leganés 2025)
# ─────────────────────────────────────────────
PRECIO_BASE_M2 = {
    "piso":    2100,
    "casa":    2650,
    "chalet":  2800,
    "atico":   2400,
    "estudio": 2000,
    "local":   1400,
    "garaje":   600,
    "otro":    1800
}

FACTOR_ZONA = {
    "centro":          1.12,
    "zarzaquemada":    1.07,
    "fortuna":         1.03,
    "arroyo_culebro":  0.97,
    "carrascal":       0.93,
    "poligono_europa": 0.89,
    "canaveral":       0.91,
    "valdepelayos":    0.88,
    "butarque":        0.95,
    "los_olivos":      0.98,
    "otro":            1.00
}

FACTOR_PLANTA = {
    # Planta: factor
    -1: 0.85,   # Sótano
    0:  0.90,   # Planta baja
    1:  0.95,
    2:  0.98,
    3:  1.00,
    4:  1.03,
    5:  1.05,
    6:  1.07,
    7:  1.08,
    8:  1.10,   # Ático / plantas altas
}

VALOR_EXTRAS = {
    "ascensor":   3500,
    "terraza":    7000,
    "garaje":    12000,
    "piscina":   15000,
    "jardin":    10000,
    "trastero":   3000,
    "amueblado":  4000,
    "reformado":  8000,
    "domótica":   5000,
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def ok(data, message="OK"):
    return jsonify({"status": "success", "message": message, "data": data})

def err(message, code=400):
    return jsonify({"status": "error", "message": message, "data": None}), code

def _calcular_precio(tipo, m2, zona, planta, extras):
    """Calcula el precio estimado con margen de ±8%."""
    base_m2   = PRECIO_BASE_M2.get(tipo.lower(), 1800)
    f_zona    = FACTOR_ZONA.get(zona.lower().replace(' ', '_'), 1.0)
    f_planta  = FACTOR_PLANTA.get(min(max(planta, -1), 8), 1.0)

    precio_base = base_m2 * m2 * f_zona * f_planta

    # Añadir valor de extras
    valor_extras = sum(VALOR_EXTRAS.get(e.lower(), 0) for e in extras)

    precio_total = precio_base + valor_extras

    # Redondear al millar más cercano
    precio_total = round(precio_total / 1000) * 1000

    return {
        "precio_estimado": int(precio_total),
        "rango_minimo": int(precio_total * 0.92),
        "rango_maximo": int(precio_total * 1.08),
        "precio_m2": int(base_m2 * f_zona * f_planta),
        "desglose": {
            "precio_base_m2": base_m2,
            "factor_zona": round(f_zona, 2),
            "factor_planta": round(f_planta, 2),
            "valor_extras": int(valor_extras),
        }
    }

# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@bp.route('/api/tasacion', methods=['POST'])
def tasacion():
    """
    Calcular tasación estimada de un inmueble.
    
    Body JSON:
      tipo     (str)  : piso | casa | chalet | atico | estudio | local | garaje
      m2       (int)  : superficie en metros cuadrados
      zona     (str)  : zona de Leganés
      planta   (int)  : número de planta (0 = baja, -1 = sótano)
      extras   (list) : ["ascensor", "terraza", "garaje", ...]
      nombre   (str)  : nombre del solicitante
      email    (str)  : email de contacto
      telefono (str)  : teléfono (opcional)
    """
    body = request.get_json(silent=True) or {}

    tipo     = (body.get('tipo') or '').strip().lower()
    m2       = body.get('m2')
    zona     = (body.get('zona') or 'otro').strip()
    planta   = body.get('planta', 3)
    extras   = body.get('extras', [])
    nombre   = (body.get('nombre') or '').strip()
    email    = (body.get('email') or '').strip()
    telefono = (body.get('telefono') or '').strip()

    # Validaciones
    errores = []
    if not tipo or tipo not in PRECIO_BASE_M2:
        errores.append(f"Tipo de inmueble no válido. Opciones: {', '.join(PRECIO_BASE_M2.keys())}.")
    try:
        m2 = int(m2)
        if m2 < 10 or m2 > 10000:
            errores.append("Los m² deben estar entre 10 y 10.000.")
    except (TypeError, ValueError):
        errores.append("Los m² deben ser un número entero.")
    if not nombre or len(nombre) < 2:
        errores.append("El nombre debe tener al menos 2 caracteres.")
    if not email or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        errores.append("El email no tiene un formato válido.")

    if errores:
        return err("; ".join(errores))

    # Calcular
    resultado = _calcular_precio(tipo, m2, zona, planta, extras)

    # Log de tasación (para seguimiento comercial)
    log = {
        "id": datetime.now().strftime('%Y%m%d%H%M%S'),
        "fecha": datetime.now().isoformat(),
        "cliente": {"nombre": nombre, "email": email, "telefono": telefono},
        "inmueble": {"tipo": tipo, "m2": m2, "zona": zona, "planta": planta, "extras": extras},
        "resultado": resultado
    }

    return ok({
        **resultado,
        "ref_tasacion": log["id"],
        "zona": zona,
        "tipo": tipo,
        "m2": m2
    }, f"Tasación calculada para tu {tipo} de {m2}m² en {zona}.")
