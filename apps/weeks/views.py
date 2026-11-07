from django.shortcuts import render

def index(request):
    """Página principal de semanas y contenidos."""
    semanas = [
        {
            'numero': 1,
            'titulo': 'Principales amenazas de las aplicaciones web',
            'retos_completados': 3,
            'total_retos': 3,
            'porcentaje': 100,
            'estado': 'Completada'
        },
        {
            'numero': 2,
            'titulo': 'Entradas no validas y manipulación de formularios',
            'retos_completados': 1,
            'total_retos': 4,
            'porcentaje': 25,
            'estado': 'En progreso'
        },
        {
            'numero': 3,
            'titulo': 'Ataques de inyección SQL',
            'retos_completados': 0,
            'total_retos': 3,
            'porcentaje': 0,
            'estado': 'Pendiente'
        }
    ]
    
    context = {
        'semanas': semanas
    }
    
    return render(request, 'weeks/index.html', context)

def detail(request, week_number):
    """Página de detalle de una semana específica."""
    # Datos específicos para cada semana - solo Semana 1 tiene contenido definido
    if week_number == 1:
        semana_data = {
            'numero': 1,
            'titulo': 'Principales amenazas de las aplicaciones web',
            'retos_completados': 3,
            'total_retos': 3,
            'porcentaje': 100,
            'estado': 'Completada',
            'objetivo_aprendizaje': 'Planifica exámenes técnicos para la identificación de las vulnerabilidades existentes en las aplicaciones web e infraestructura tecnológica de una organización empresarial a partir de aplicaciones de análisis de vulnerabilidades.',
            'retos': [
                {'nombre': 'Reto 1', 'completado': True},
                {'nombre': 'Reto 2', 'completado': True},
                {'nombre': 'Reto 3', 'completado': True}
            ]
        }
    else:
        # Para las demás semanas, usamos datos genéricos
        semana_data = {
            'numero': week_number,
            'titulo': f'Semana {week_number}',
            'retos_completados': 0,
            'total_retos': 3,
            'porcentaje': 0,
            'estado': 'Pendiente',
            'objetivo_aprendizaje': 'Contenido de la semana pendiente por desarrollar.',
            'retos': [
                {'nombre': 'Reto 1', 'completado': False},
                {'nombre': 'Reto 2', 'completado': False},
                {'nombre': 'Reto 3', 'completado': False}
            ]
        }
    
    context = {
        'week_number': week_number,
        'semana': semana_data
    }
    return render(request, 'weeks/detail.html', context)