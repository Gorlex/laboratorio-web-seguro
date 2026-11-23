from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .registry import LABORATORIOS
from .services import iniciar_laboratorio, finalizar_laboratorio

@require_POST
@csrf_protect
def iniciar_laboratorio_view(request, lab_id):
    """
    Inicia un laboratorio autorizado mediante Docker Compose.
    """
    # Verificar que el laboratorio esté en la lista blanca
    if lab_id not in LABORATORIOS:
        return JsonResponse({
                "success": False,
            "message": "Laboratorio no autorizado"
        }, status=404)

    # Iniciar el laboratorio usando el servicio existente
    try:
        resultado = iniciar_laboratorio(lab_id)
    except Exception as e:
        # Capturar cualquier excepción inesperada
        return JsonResponse({
            "success": False,
            "message": "Error interno al iniciar el laboratorio"
        }, status=500)

    # Devolver la respuesta JSON
    if resultado["success"]:
        return JsonResponse({
            "success": True,
            "message": "Laboratorio iniciado correctamente"
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "No fue posible iniciar el laboratorio"
        }, status=503)


@require_POST
@csrf_protect
def finalizar_laboratorio_view(request, lab_id):
    """
    Finaliza un laboratorio autorizado mediante Docker Compose.
    """
    # Verificar que el laboratorio esté en la lista blanca
    if lab_id not in LABORATORIOS:
        return JsonResponse({
            "success": False,
            "message": "Laboratorio no autorizado"
        }, status=404)

    # Finalizar el laboratorio usando el servicio existente
    try:
        resultado = finalizar_laboratorio(lab_id)
    except Exception as e:
        # Capturar cualquier excepción inesperada
        return JsonResponse({
            "success": False,
            "message": "Error interno al finalizar el laboratorio"
        }, status=500)

    # Devolver la respuesta JSON
    if resultado["success"]:
        return JsonResponse({
            "success": True,
            "message": "Laboratorio finalizado correctamente"
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "No fue posible finalizar el laboratorio"
        }, status=503)

