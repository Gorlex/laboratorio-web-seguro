"""
Mock data for the dashboard.

Temporary data to be replaced by real models later.
"""

WEEKS = [
    {
        'week': 1,
        'title': 'Introducción a XSS',
        'challenges': [
            {
                'id': 1,
                'title': 'XSS Reflejado Básico',
                'description': 'Encuentra y explota una vulnerabilidad XSS reflejado en el formulario de búsqueda.',
                'difficulty': 'Fácil',
                'status': 'completed',
            },
            {
                'id': 2,
                'title': 'XSS en Parámetros URL',
                'description': 'Identifica un punto de entrada XSS a través de parámetros de URL.',
                'difficulty': 'Fácil',
                'status': 'completed',
            },
            {
                'id': 3,
                'title': 'Prevención de XSS',
                'description': 'Aplica las medidas correctas para prevenir ataques XSS.',
                'difficulty': 'Medio',
                'status': 'in_progress',
            },
        ],
    },
    {
        'week': 2,
        'title': 'SQL Injection',
        'challenges': [
            {
                'id': 4,
                'title': 'SQL Injection Básico',
                'description': 'Explota una vulnerabilidad de inyección SQL en el login.',
                'difficulty': 'Fácil',
                'status': 'pending',
            },
            {
                'id': 5,
                'title': 'Unión-Based SQLi',
                'description': 'Usa UNION para extraer datos de otras tablas.',
                'difficulty': 'Medio',
                'status': 'pending',
            },
            {
                'id': 6,
                'title': 'Prevención de SQLi',
                'description': 'Implementa consultas parametrizadas para prevenir inyecciones.',
                'difficulty': 'Medio',
                'status': 'pending',
            },
        ],
    },
    {
        'week': 3,
        'title': 'Autenticación y Sesiones',
        'challenges': [
            {
                'id': 7,
                'title': 'Fuerza Bruta en Login',
                'description': 'Practica técnicas de fuerza bruta contra un formulario de autenticación.',
                'difficulty': 'Fácil',
                'status': 'pending',
            },
            {
                'id': 8,
                'title': 'Secuestro de Sesión',
                'description': 'Explota una vulnerabilidad de gestión de sesiones.',
                'difficulty': 'Difícil',
                'status': 'pending',
            },
        ],
    },
]
