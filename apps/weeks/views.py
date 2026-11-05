from django.shortcuts import render

def index(request):
    """Página principal de semanas y contenidos."""
    semanas = [
        {
            'numero': 1,
            'titulo': 'Fundamentos de Seguridad Web',
            'retos_completados': 3,
            'total_retos': 3,
            'porcentaje': 100,
            'estado': 'Completada'
        },
        {
            'numero': 2,
            'titulo': 'Inyección SQL y Validación',
            'retos_completados': 1,
            'total_retos': 4,
            'porcentaje': 25,
            'estado': 'En progreso'
        },
        {
            'numero': 3,
            'titulo': 'Cross-Site Scripting (XSS)',
            'retos_completados': 0,
            'total_retos': 3,
            'porcentaje': 0,
            'estado': 'Pendiente'
        },
        {
            'numero': 4,
            'titulo': 'Autenticación y Sesiones',
            'retos_completados': 0,
            'total_retos': 3,
            'porcentaje': 0,
            'estado': 'Pendiente'
        },
        {
            'numero': 5,
            'titulo': 'Ataques de Seguridad',
            'retos_completados': 0,
            'total_retos': 3,
            'porcentaje': 0,
            'estado': 'Pendiente'
        },
        {
            'numero': 6,
            'titulo': 'Protección de Datos',
            'retos_completados': 0,
            'total_retos': 3,
            'porcentaje': 0,
            'estado': 'Pendiente'
        },
        {
            'numero': 7,
            'titulo': 'Pruebas de Seguridad',
            'retos_completados': 0,
            'total_retos': 3,
            'porcentaje': 0,
            'estado': 'Pendiente'
        },
        {
            'numero': 8,
            'titulo': 'Evaluación Final',
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