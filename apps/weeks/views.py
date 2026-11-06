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
    # Esta vista se implementará en una etapa futura
    context = {
        'week_number': week_number
    }
    return render(request, 'weeks/detail.html', context)