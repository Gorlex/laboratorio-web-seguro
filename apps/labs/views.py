from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.db import DatabaseError
from django.utils import timezone
from .registry import LABORATORIOS
from .services import iniciar_laboratorio, finalizar_laboratorio
from .models import LaboratorioActivo

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
        # Registrar la excepción y devolver error 500
        print(f"Error al iniciar laboratorio: {e}")
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
        # Registrar la excepción y devolver error 500
        print(f"Error al finalizar laboratorio: {e}")
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


@require_POST
@csrf_protect
def registrar_actividad_view(request, lab_id):
    """
    Registra la última actividad de un laboratorio activo.
    """
    # Verificar que el laboratorio esté en la lista blanca
    if lab_id not in LABORATORIOS:
        return JsonResponse({
            "success": False,
            "message": "Laboratorio no autorizado"
        }, status=404)

    try:
        # Obtener la hora actual
        ahora = timezone.now()

        # Actualizar únicamente el campo ultima_actividad de un registro activo
        actualizados = LaboratorioActivo.objects.filter(
            lab_id=lab_id,
            activo=True
        ).update(
            ultima_actividad=ahora
        )

        # Si no se actualizó ningún registro, el laboratorio no está activo
        if actualizados == 0:
            return JsonResponse({
                "success": False,
                "message": "El laboratorio no se encuentra activo"
            }, status=409)

        # Si se actualizó correctamente
        return JsonResponse({
            "success": True,
            "message": "Actividad registrada correctamente",
            "lab_id": lab_id,
            "ultima_actividad": ahora.isoformat()
        })

    except DatabaseError as db_error:
        # Registrar el error pero devolver respuesta genérica al cliente
        print(f"Error de base de datos al registrar actividad: {db_error}")
        return JsonResponse({
            "success": False,
            "message": "No fue posible registrar la actividad del laboratorio"
        }, status=500)

