"""
routes/admin.py
Panel de administración para gestionar propiedades
"""
import json
import os
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Credenciales simples (cambiar en producción)
ADMIN_USER = 'admin'
ADMIN_PASS = 'greenhouse2025'  # ⚠️ CAMBIAR ESTO EN PRODUCCIÓN

PROPIEDADES_FILE = 'propiedades.json'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

def cargar_propiedades():
    """Carga propiedades desde JSON"""
    if os.path.exists(PROPIEDADES_FILE):
        with open(PROPIEDADES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"propiedades": []}

def guardar_propiedades(data):
    """Guarda propiedades en JSON"""
    with open(PROPIEDADES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/login.html', error='Usuario o contraseña incorrectos')
    
    return render_template('admin/login.html')

@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin.login'))

@bp.route('/')
@login_required
def dashboard():
    data = cargar_propiedades()
    return render_template('admin/dashboard.html', 
                         propiedades=data['propiedades'],
                         total=len(data['propiedades']))

@bp.route('/propiedad/nueva', methods=['GET', 'POST'])
@login_required
def nueva_propiedad():
    if request.method == 'POST':
        data = cargar_propiedades()
        
        # Generar nuevo ID
        nuevo_id = max([p['id'] for p in data['propiedades']], default=0) + 1
        
        nueva = {
            'id': nuevo_id,
            'tipo': request.form.get('tipo'),
            'operacion': request.form.get('operacion'),
            'titulo': request.form.get('titulo'),
            'descripcion': request.form.get('descripcion'),
            'zona': request.form.get('zona'),
            'precio': int(request.form.get('precio')),
            'm2': int(request.form.get('m2')),
            'habitaciones': int(request.form.get('habitaciones')),
            'banos': int(request.form.get('banos')),
            'extras': request.form.getlist('extras'),
            'imagen': request.form.get('imagen'),
            'destacado': request.form.get('destacado') == 'on',
            'ref': f"GH-{nuevo_id:03d}"
        }
        
        data['propiedades'].append(nueva)
        guardar_propiedades(data)
        
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/form_propiedad.html', propiedad=None)

@bp.route('/propiedad/editar/<int:prop_id>', methods=['GET', 'POST'])
@login_required
def editar_propiedad(prop_id):
    data = cargar_propiedades()
    propiedad = next((p for p in data['propiedades'] if p['id'] == prop_id), None)
    
    if not propiedad:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        propiedad.update({
            'tipo': request.form.get('tipo'),
            'operacion': request.form.get('operacion'),
            'titulo': request.form.get('titulo'),
            'descripcion': request.form.get('descripcion'),
            'zona': request.form.get('zona'),
            'precio': int(request.form.get('precio')),
            'm2': int(request.form.get('m2')),
            'habitaciones': int(request.form.get('habitaciones')),
            'banos': int(request.form.get('banos')),
            'extras': request.form.getlist('extras'),
            'imagen': request.form.get('imagen'),
            'destacado': request.form.get('destacado') == 'on'
        })
        
        guardar_propiedades(data)
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/form_propiedad.html', propiedad=propiedad)

@bp.route('/propiedad/eliminar/<int:prop_id>', methods=['POST'])
@login_required
def eliminar_propiedad(prop_id):
    data = cargar_propiedades()
    data['propiedades'] = [p for p in data['propiedades'] if p['id'] != prop_id]
    guardar_propiedades(data)
    return redirect(url_for('admin.dashboard'))
