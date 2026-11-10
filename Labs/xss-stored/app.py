from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# ⚠️ CLAVE SECRETA - Necesaria para sesiones
# En producción esto debe ser una cadena aleatoria larga y segura
app.secret_key = 'clave_secreta_de_laboratorio_no_usar_en_produccion_12345'

# Configuración de sesión
app.config['SESSION_COOKIE_NAME'] = 'sesion_paciente'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 1 día
# ⚠️ SOLO PARA LABORATORIO - En producción debe ser True
app.config['SESSION_COOKIE_HTTPONLY'] = False

# Función para conectar a la base de datos
def get_db():
    conn = sqlite3.connect('notas.db')
    conn.row_factory = sqlite3.Row
    return conn

# Función para inicializar la base de datos
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas_medicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT NOT NULL,
            nota TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Ruta principal - Formulario
@app.route('/')
def index():
    # Simulamos un "login" creando una sesión con datos del usuario
    if 'usuario_id' not in session:
        session['usuario_id'] = 1001
        session['usuario_nombre'] = 'Dr. García'
        session['rol'] = 'medico'
    
    return render_template('index.html', usuario=session.get('usuario_nombre'))

# Ruta para guardar la nota
@app.route('/guardar', methods=['POST'])
def guardar():
    paciente = request.form.get('paciente')
    nota = request.form.get('nota')
    
    if paciente and nota:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO notas_medicas (paciente, nota) VALUES (?, ?)',
            (paciente, nota)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('listar'))
    
    return redirect(url_for('index'))

# Ruta para listar las notas (AQUÍ ESTÁ LA VULNERABILIDAD)
@app.route('/listar')
def listar():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notas_medicas ORDER BY fecha_creacion DESC')
    notas = cursor.fetchall()
    conn.close()
    return render_template('listar.html', notas=notas)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)