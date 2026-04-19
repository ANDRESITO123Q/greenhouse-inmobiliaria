# 🏡 Green House Inmobiliaria - Sistema Completo

## 📋 **CONTENIDO DEL PROYECTO**

Sistema web completo para Green House Inmobiliaria en Leganés, Madrid.

### **Incluye:**
- ✅ **Web profesional** con diseño moderno
- ✅ **Panel de administración** para gestionar propiedades
- ✅ **Backend Flask** con API REST
- ✅ **Sistema JSON** para almacenar propiedades
- ✅ **Fotos reales** de la oficina integradas
- ✅ **Calculadora de tasación** online
- ✅ **Formulario de contacto**
- ✅ **Búsqueda avanzada** de propiedades

---

## 🚀 **INSTALACIÓN RÁPIDA**

### **Paso 1: Instalar Python**
Asegúrate de tener Python 3.8 o superior:
```bash
python --version
```

### **Paso 2: Crear entorno virtual**
```bash
cd greenhouse
python -m venv venv
```

### **Paso 3: Activar entorno**
- **Windows:**
```bash
venv\Scripts\activate
```

- **Linux/Mac:**
```bash
source venv/bin/activate
```

### **Paso 4: Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **Paso 5: Arrancar servidor**
```bash
python app.py
```

**¡Listo!** Abre tu navegador en: `http://localhost:5000`

---

## 🎨 **CÓMO USAR EL PANEL ADMIN**

### **Acceso:**
1. Abre tu navegador
2. Ve a: `http://localhost:5000/admin`
3. Verás todas tus propiedades

### **Agregar nueva propiedad:**
1. Click en **"+ Nueva Propiedad"**
2. Rellena el formulario
3. Click en **"Guardar Propiedad"**
4. ¡La propiedad aparece automáticamente en la web!

### **Editar propiedad:**
1. Click en **"✏️ Editar"** en la tarjeta
2. Modifica lo que necesites
3. Click en **"Guardar Propiedad"**

### **Eliminar propiedad:**
1. Click en **"🗑️ Eliminar"**
2. Confirma la acción

---

## 💾 **3 FORMAS DE ACTUALIZAR PROPIEDADES**

#### **OPCIÓN 1: Panel Admin Web** (Recomendado ⭐)
- Más fácil
- No necesitas programar
- Interfaz visual
- Acceso: `http://localhost:5000/admin`

#### **OPCIÓN 2: Editar JSON directamente**
1. Abre `/data/propiedades.json` con Notepad
2. Agrega/edita propiedades
3. Guarda el archivo

#### **OPCIÓN 3: API REST** (Avanzado)
Usa curl o Postman para hacer llamadas a la API.

---

## 📂 **ESTRUCTURA DEL PROYECTO**

```
greenhouse/
├── app.py                     # Servidor Flask
├── requirements.txt           # Dependencias
│
├── data/
│   └── propiedades.json       # BASE DE DATOS
│
├── templates/
│   ├── index.html             # Web principal
│   ├── admin.html             # Panel admin
│   └── logo.png               # Logo
│
├── static/
│   └── images/
│       └── oficina/           # Fotos reales
│           ├── fachada.jpg
│           ├── oficina1.jpg
│           └── oficina2.jpg
│
└── routes/
    ├── propiedades.py         # API
    ├── contacto.py
    └── tasacion.py
```

---

## 📞 **INFORMACIÓN DE CONTACTO**

**Green House Inmobiliaria**
- 📍 C. de los Pedroches, 32, 28915 Leganés
- 📞 919 415 198
- 📱 693 009 436
- 💬 WhatsApp: https://wa.me/34693009436

---

## 🎓 **TUTORIAL: AGREGAR TU PRIMERA PROPIEDAD**

1. Inicia: `python app.py`
2. Abre: `http://localhost:5000/admin`
3. Click "+ Nueva Propiedad"
4. Rellena datos
5. Guardar
6. ¡Listo! Aparece en la web

---

**¡Listo para vender propiedades! 🚀**

*Green House Inmobiliaria - Leganés, Madrid*
