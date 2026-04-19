"""
routes/propiedades.py
CRUD de propiedades con backend JSON – Green House Inmobiliaria
"""

from flask import Blueprint, jsonify, request
import json
import os

bp = Blueprint('propiedades', __name__)

# Ruta al archivo JSON
JSON_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'propiedades.json')

def _load_propiedades():
    """Carga propiedades desde JSON."""
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('propiedades', [])
    except:
        return []

def _save_propiedades(propiedades):
    """Guarda propiedades en JSON."""
    try:
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump({'propiedades': propiedades}, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

_ZONAS = [
    {"id": "centro", "nombre": "Centro", "propiedades": 87},
    {"id": "zarzaquemada", "nombre": "Zarzaquemada", "propiedades": 62},
    {"id": "fortuna", "nombre": "La Fortuna", "propiedades": 54},
    {"id": "arroyo", "nombre": "Arroyo Culebro", "propiedades": 41},
    {"id": "carrascal", "nombre": "El Carrascal", "propiedades": 38},
    {"id": "valdepelayos", "nombre": "Valdepelayos", "propiedades": 22},
    {"id": "butarque", "nombre": "Butarque", "propiedades": 45},
]

def ok(data, message="OK"):
    return jsonify({"status": "success", "message": message, "data": data})

def err(message, code=400):
    return jsonify({"status": "error", "message": message, "data": None}), code

def _apply_filters(props, params):
    """Aplica filtros sobre propiedades."""
    tipo = params.get('tipo', '').lower()
    operacion = params.get('operacion', '').lower()
    zona = params.get('zona', '').lower()
    precio_min = params.get('precio_min', type=int, default=0)
    precio_max = params.get('precio_max', type=int, default=9_999_999)
    m2_min = params.get('m2_min', type=int, default=0)
    hab = params.get('habitaciones', type=int, default=0)
    
    filtered = []
    for p in props:
        if not p.get('activo', True):
            continue
        if tipo and p.get('tipo', '').lower() != tipo:
            continue
        if operacion and p.get('operacion', '').lower() != operacion:
            continue
        if zona and zona not in p.get('zona', '').lower():
            continue
        if not (precio_min <= p.get('precio', 0) <= precio_max):
            continue
        if p.get('m2', 0) < m2_min:
            continue
        if hab and p.get('habitaciones', 0) < hab:
            continue
        filtered.append(p)
    return filtered

@bp.route('/api/propiedades', methods=['GET'])
def get_propiedades():
    """Listar propiedades con filtros."""
    props = _load_propiedades()
    filtradas = _apply_filters(props, request.args)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    paginadas = filtradas[start:end]

    return ok({
        "propiedades": paginadas,
        "total": len(filtradas),
        "page": page,
        "per_page": per_page,
        "pages": max(1, -(-len(filtradas) // per_page))
    })

@bp.route('/api/propiedades/<int:prop_id>', methods=['GET'])
def get_propiedad(prop_id):
    """Detalle de una propiedad."""
    props = _load_propiedades()
    prop = next((p for p in props if p.get('id') == prop_id), None)
    if not prop:
        return err(f"Propiedad #{prop_id} no encontrada", 404)
    return ok(prop)

@bp.route('/api/buscar', methods=['POST'])
def buscar():
    """Búsqueda avanzada."""
    body = request.get_json(silent=True) or {}
    props = _load_propiedades()
    
    class _Params:
        def get(self, key, default=None, type=None):
            val = body.get(key, default)
            if val is None:
                return default
            if type is int:
                try: return int(val)
                except: return default
            return val
    
    filtradas = _apply_filters(props, _Params())
    return ok({"propiedades": filtradas, "total": len(filtradas)})

@bp.route('/api/zonas', methods=['GET'])
def get_zonas():
    """Listar zonas."""
    return ok(_ZONAS)

@bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Estadísticas."""
    props = _load_propiedades()
    ventas = [p for p in props if p.get('operacion') == 'venta' and p.get('activo')]
    alquileres = [p for p in props if p.get('operacion') == 'alquiler' and p.get('activo')]
    
    return ok({
        "total_propiedades": 500,
        "en_venta": len(ventas),
        "en_alquiler": len(alquileres),
        "anos_experiencia": 10,
        "clientes_satisfechos": 1200,
        "satisfaccion_pct": 98,
        "zonas_activas": len(_ZONAS),
        "precio_medio_venta": round(sum(p.get('precio', 0) for p in ventas) / max(len(ventas), 1)),
        "precio_medio_alquiler": round(sum(p.get('precio', 0) for p in alquileres) / max(len(alquileres), 1))
    })

# ═══════════════════════════════════════════════════════════
# PANEL ADMIN - Gestión de propiedades
# ═══════════════════════════════════════════════════════════

@bp.route('/api/admin/propiedades', methods=['POST'])
def admin_crear_propiedad():
    """Crear nueva propiedad (ADMIN)."""
    body = request.get_json(silent=True) or {}
    
    props = _load_propiedades()
    nuevo_id = max([p.get('id', 0) for p in props], default=0) + 1
    
    nueva = {
        "id": nuevo_id,
        "tipo": body.get('tipo', 'piso'),
        "operacion": body.get('operacion', 'venta'),
        "titulo": body.get('titulo', ''),
        "descripcion": body.get('descripcion', ''),
        "zona": body.get('zona', ''),
        "precio": int(body.get('precio', 0)),
        "m2": int(body.get('m2', 0)),
        "habitaciones": int(body.get('habitaciones', 0)),
        "banos": int(body.get('banos', 1)),
        "extras": body.get('extras', []),
        "imagen": body.get('imagen', ''),
        "destacado": body.get('destacado', False),
        "activo": True
    }
    
    props.append(nueva)
    if _save_propiedades(props):
        return ok(nueva, "Propiedad creada exitosamente")
    return err("Error al guardar propiedad", 500)

@bp.route('/api/admin/propiedades/<int:prop_id>', methods=['PUT'])
def admin_actualizar_propiedad(prop_id):
    """Actualizar propiedad (ADMIN)."""
    body = request.get_json(silent=True) or {}
    props = _load_propiedades()
    
    prop = next((p for p in props if p.get('id') == prop_id), None)
    if not prop:
        return err("Propiedad no encontrada", 404)
    
    # Actualizar campos
    for key in ['tipo', 'operacion', 'titulo', 'descripcion', 'zona', 'precio', 'm2', 'habitaciones', 'banos', 'extras', 'imagen', 'destacado', 'activo']:
        if key in body:
            prop[key] = body[key]
    
    if _save_propiedades(props):
        return ok(prop, "Propiedad actualizada")
    return err("Error al guardar", 500)

@bp.route('/api/admin/propiedades/<int:prop_id>', methods=['DELETE'])
def admin_eliminar_propiedad(prop_id):
    """Eliminar propiedad (ADMIN)."""
    props = _load_propiedades()
    prop = next((p for p in props if p.get('id') == prop_id), None)
    
    if not prop:
        return err("Propiedad no encontrada", 404)
    
    # Marcar como inactivo en lugar de eliminar
    prop['activo'] = False
    
    if _save_propiedades(props):
        return ok({"id": prop_id}, "Propiedad eliminada")
    return err("Error al eliminar", 500)
