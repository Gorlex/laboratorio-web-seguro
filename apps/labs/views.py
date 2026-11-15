
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .registry import LABORATORIOS
from .services import iniciar_laboratorio


@require_POST
def iniciar_laboratorio_view(request, lab_id):
    # Verificar que el laboratorio esté autorizado
    if lab_id not in LABORATORIOS:
        return JsonResponse(
            {
                "success": False,
                "message": "Laboratorio no autorizado",
            },
            status=404,
        )

    # Iniciar el laboratorio mediante el servicio existente
    try:
        resultado = iniciar_laboratorio(lab_id)
    except Exception:
        return JsonResponse(
            {
                "success": False,
                "message": "Error interno al iniciar el laboratorio",
            },
            status=500,
        )

    if resultado["success"]:
        return JsonResponse(
            {
                "success": True,
                "message": "Laboratorio iniciado correctamente",
            },
            status=200,
        )

    return JsonResponse(
        {
            "success": False,
            "message": "No fue posible iniciar el laboratorio",
        },
        status=503,
    )
