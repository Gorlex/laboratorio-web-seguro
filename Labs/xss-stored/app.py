from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# ⚠️ CLAVE SECRETA - Necesaria para sesiones
app.secret_key = 'clave_secreta_de_laboratorio_no_usar_en_produccion_12345'

# Configuración de sesión
app.config['SESSION_COOKIE_NAME'] = 'sesion_paciente'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 1 día
app.config['SESSION_COOKIE_HTTPONLY'] = False  # ⚠️ SOLO PARA LABORATORIO

# Función para conectar a la base de datos
def get_db():
    conn = sqlite3.connect('notas.db')
    conn.row_factory = sqlite3.Row
    return conn

# Función para inicializar la base de datos
# Función para inicializar la base de datos con datos ficticios
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas_medicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT NOT NULL,
            nota TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Verificar si ya hay datos (para no duplicar al reiniciar)
    cursor.execute('SELECT COUNT(*) FROM notas_medicas')
    if cursor.fetchone()[0] == 0:
        # Datos ficticios precargados
        notas_iniciales = [
            {
                'paciente': 'Roberto Sánchez López',
                'nota': 'Paciente masculino de 58 años acude a consulta por dolor torácico de 3 días de evolución. Se realiza electrocardiograma sin alteraciones agudas. Se indica reposo relativo y se programa ecocardiograma para la próxima semana. Tensión arterial: 140/90 mmHg.'
            },
            {
                'paciente': 'Lucía Martínez Ruiz',
                'nota': 'Paciente femenina de 32 años, gestante de 24 semanas. Control prenatal rutinario sin complicaciones. Peso: 68 kg, tensión arterial: 110/70 mmHg. Fetocardia presente y regular. Se solicitan análisis de laboratorio de segundo trimestre.'
            },
            {
                'paciente': 'Miguel Ángel Torres',
                'nota': 'Paciente masculino de 45 años con antecedente de diabetes mellitus tipo 2. Hemoglobina glicosilada: 7.8%. Se ajusta dosis de metformina a 1000 mg cada 12 horas. Se refuerza educación sobre dieta y ejercicio. Próximo control en 3 meses.'
            },
            {
                'paciente': 'Carmen Elena Vega',
                'nota': 'Paciente femenina de 67 años con diagnóstico de hipertensión arterial sistémica. Actualmente en tratamiento con losartán 50 mg/día. Tensión arterial en consultorio: 135/85 mmHg. Sin síntomas asociados. Se mantiene esquema actual.'
            }
           
        ]
        
        for nota in notas_iniciales:
            cursor.execute(
                'INSERT INTO notas_medicas (paciente, nota) VALUES (?, ?)',
                (nota['paciente'], nota['nota'])
            )
        
        conn.commit()
        print("✅ Base de datos inicializada con 5 notas ficticias (incluyendo 1 con XSS inyectado)")
    else:
        print("ℹ️  La base de datos ya contiene datos, no se insertaron registros nuevos.")
    
    conn.close()

# Datos ficticios de médicos
MEDICOS = [
    {
        'id': 1,
        'nombre': 'Dra. María Elena Rodríguez',
        'especialidad': 'Cardiología',
        'semblanza': 'Especialista en cardiología clínica e intervencionista con más de 15 años de experiencia en el diagnóstico y tratamiento de enfermedades cardiovasculares. Graduada con honores de la Universidad Nacional.',
        'certificaciones': [
            'Consejo Colombiano de Cardiología A.C.',
            'American Heart Association',
            'Sociedad Interamericana de Cardiología'
        ],
        'servicios': [
            'Electrocardiograma',
            'Ecocardiograma',
            'Prueba de esfuerzo',
            'Holter de ritmo',
            'Monitoreo ambulatorio de presión arterial'
        ],
        'enfermedades': [
            'Hipertensión arterial',
            'Arritmias cardiacas',
            'Insuficiencia cardiaca',
            'Enfermedad coronaria',
            'Cardiopatías congénitas'
        ],
        'horarios': [
            'Lunes a Viernes: 9:00 AM - 2:00 PM',
            'Sábados: 9:00 AM - 1:00 PM'
        ],
        'imagen': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop'
    },
    {
        'id': 2,
        'nombre': 'Dr. Carlos Alberto Mendoza',
        'especialidad': 'Pediatría',
        'semblanza': 'Pediatra con subespecialidad en neonatología. Dedicado al cuidado integral de la salud infantil desde el nacimiento hasta la adolescencia. Enfoque en medicina preventiva y desarrollo infantil.',
        'certificaciones': [
            'Consejo Colombiano de Pediatría A.C.',
            'Academia Americana de Pediatría',
            'Sociedad Latinoamericana de Pediatría'
        ],
        'servicios': [
            'Consulta pediátrica general',
            'Control de niño sano',
            'Vacunación',
            'Evaluación del desarrollo',
            'Atención de urgencias pediátricas'
        ],
        'enfermedades': [
            'Infecciones respiratorias',
            'Asma infantil',
            'Alergias alimentarias',
            'Enfermedades infecciosas',
            'Problemas de crecimiento'
        ],
        'horarios': [
            'Lunes a Viernes: 10:00 AM - 3:00 PM',
            'Urgencias: 24/7'
        ],
        'imagen': 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop'
    },
    {
        'id': 3,
        'nombre': 'Dra. Ana Lucía Fernández',
        'especialidad': 'Dermatología',
        'semblanza': 'Dermatóloga clínica y estética con amplia experiencia en el tratamiento de enfermedades de la piel, cabello y uñas. Especializada en dermatología cosmética y procedimientos láser.',
        'certificaciones': [
            'Consejo Mexicano de Dermatología A.C.',
            'American Academy of Dermatology',
            'Sociedad Española de Dermatología'
        ],
        'servicios': [
            'Consulta dermatológica',
            'Dermatoscopia digital',
            'Biopsias de piel',
            'Tratamientos láser',
            'Peelings químicos',
            'Crioterapia'
        ],
        'enfermedades': [
            'Acné',
            'Psoriasis',
            'Dermatitis atópica',
            'Cáncer de piel',
            'Alopecia',
            'Rosácea'
        ],
        'horarios': [
            'Lunes a Viernes: 8:00 AM - 1:00 PM y 4:00 PM - 7:00 PM',
            'Sábados: 9:00 AM - 2:00 PM'
        ],
        'imagen': 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=300&h=300&fit=crop'
    }
]

# Ruta principal - Dashboard de médicos
@app.route('/')
def dashboard():
    # Simulamos un "login" creando una sesión con datos del usuario
    if 'usuario_id' not in session:
        session['usuario_id'] = 1001
        session['usuario_nombre'] = 'Dr. García'
        session['rol'] = 'medico'
    
    return render_template('dashboard.html', 
                         medicos=MEDICOS, 
                         usuario=session.get('usuario_nombre'))

# Ruta para formulario de notas médicas
@app.route('/notas')
def index():
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
    return render_template('listar.html', notas=notas, usuario=session.get('usuario_nombre'))

if __name__ == '__main__':
    init_db()
    # Cambiar el host a 0.0.0.0 para que sea accesible desde Docker
    app.run(debug=True, host='0.0.0.0', port=5000)
