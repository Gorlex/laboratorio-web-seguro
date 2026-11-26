import subprocess
from django.utils import timezone
from .registry import LABORATORIOS
from .models import LaboratorioActivo

def iniciar_laboratorio(lab_id):
    """Inicia un laboratorio autorizado mediante Docker Compose."""
    
    # Verificar que el laboratorio esté en la lista blanca
    if lab_id not in LABORATORIOS:
        return {
            "success": False,
            "message": "Laboratorio no autorizado",
        }
    
    laboratorio = LABORATORIOS[lab_id]
    
    # Obtener la ruta del archivo docker-compose.yml
    compose_dir = laboratorio["compose_dir"]
    compose_file = compose_dir / "docker-compose.yml"
    
    # Verificar que el archivo docker-compose.yml exista
    if not compose_file.is_file():
        return {
            "success": False,
            "message": "No se encontró docker-compose.yml",
        }
    
    # Construir el comando Docker Compose
    comando = [
        "docker",
        "compose",
        "-f",
        str(compose_file),
        "up",
        "-d",
        "--no-deps",
        laboratorio["service"],
    ]
    
    try:
        # Ejecutar el comando con timeout de 120 segundos
        resultado = subprocess.run(
            comando,
            cwd=str(compose_dir),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        
        # Si el comando falla, devolver error
        if resultado.returncode != 0:
            return {
                "success": False,
                "message": f"No fue posible iniciar el laboratorio: {resultado.stderr}",
                "stdout": resultado.stdout,
                "stderr": resultado.stderr,
            }
        
        # Si el comando tiene éxito, registrar en la base de datos
        try:
            # Obtener o crear el registro del laboratorio
            lab_registro, creado = LaboratorioActivo.objects.update_or_create(
                lab_id=lab_id,
                defaults={
                    'activo': True,
                    'fecha_inicio': timezone.now(),
                    'ultima_actividad': timezone.now(),
                    'fecha_finalizacion': None
                }
            )
            
            # Si el registro ya existía y estaba activo, no modificamos las fechas de inicio
            # Solo actualizamos la última actividad
            if not creado and lab_registro.activo:
                # El contenedor ya estaba ejecutándose, solo actualizamos la última actividad
                lab_registro.ultima_actividad = timezone.now()
                lab_registro.save()
            
        except Exception as db_error:
            # Registrar el error pero no fallar la operación de Docker
            print(f"Error al registrar en base de datos: {db_error}")
            return {
                "success": True,  # Docker ejecutó correctamente
                "message": "Laboratorio iniciado correctamente, pero no se pudo registrar en la base de datos",
                "stdout": resultado.stdout,
                "stderr": resultado.stderr,
            }
        
        return {
            "success": True,
            "message": "Laboratorio iniciado correctamente",
            "stdout": resultado.stdout,
            "stderr": resultado.stderr,
        }
        
    except FileNotFoundError:
        return {
            "success": False,
            "message": "No se encontró el ejecutable Docker",
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Se agotó el tiempo de espera de Docker Compose",
        }
    except OSError as error:
        return {
            "success": False,
            "message": f"Error al ejecutar Docker: {error}",
        }


def finalizar_laboratorio(lab_id):
    """Finaliza y elimina un laboratorio autorizado mediante Docker Compose."""
    
    # Verificar que el laboratorio esté en la lista blanca
    if lab_id not in LABORATORIOS:
        return {
            "success": False,
            "message": "Laboratorio no autorizado",
        }
    
    laboratorio = LABORATORIOS[lab_id]
    
    # Obtener la ruta del archivo docker-compose.yml
    compose_dir = laboratorio["compose_dir"]
    compose_file = compose_dir / "docker-compose.yml"
    
    # Verificar que el archivo docker-compose.yml exista
    if not compose_file.is_file():
        return {
            "success": False,
            "message": "No se encontró docker-compose.yml",
        }
    
    try:
        # Primero detener el contenedor
        comando_stop = [
            "docker",
            "compose",
            "-f",
            str(compose_file),
            "stop",
            laboratorio["service"],
        ]
        
        resultado_stop = subprocess.run(
            comando_stop,
            cwd=str(compose_dir),
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        
        # Si el stop falla, no continuar con el rm
        if resultado_stop.returncode != 0:
            return {
                "success": False,
                "message": f"Error al detener el contenedor: {resultado_stop.stderr}",
                "stdout": resultado_stop.stdout,
                "stderr": resultado_stop.stderr,
            }
        
        # Luego eliminar el contenedor
        comando_rm = [
            "docker",
            "compose",
            "-f",
            str(compose_file),
            "rm",
            "-f",
            "-s",
            laboratorio["service"],
        ]
        
        resultado_rm = subprocess.run(
            comando_rm,
            cwd=str(compose_dir),
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        
        # Verificar que ambos comandos fueron exitosos
        if resultado_rm.returncode == 0:
            # Si la finalización fue exitosa, registrar en la base de datos
            try:
                # Obtener el registro del laboratorio
                try:
                    lab_registro = LaboratorioActivo.objects.get(lab_id=lab_id)
                    # Actualizar el registro a inactivo
                    lab_registro.activo = False
                    lab_registro.fecha_finalizacion = timezone.now()
                    lab_registro.save()
                except LaboratorioActivo.DoesNotExist:
                    # Si no existe el registro, crear uno nuevo inactivo
                    LaboratorioActivo.objects.create(
                        lab_id=lab_id,
                        activo=False,
                        fecha_inicio=None,
                        ultima_actividad=None,
                        fecha_finalizacion=timezone.now()
                    )
                    
            except Exception as db_error:
                # Registrar el error pero no fallar la operación de Docker
                print(f"Error al registrar en base de datos: {db_error}")
                return {
                    "success": True,  # Docker ejecutó correctamente
                    "message": "Laboratorio finalizado correctamente, pero no se pudo actualizar el registro en la base de datos",
                    "stdout": resultado_stop.stdout + resultado_rm.stdout,
                    "stderr": resultado_stop.stderr + resultado_rm.stderr,
                }
            
            return {
                "success": True,
                "message": "Laboratorio finalizado y contenedor eliminado correctamente",
                "stdout": resultado_stop.stdout + resultado_rm.stdout,
                "stderr": resultado_stop.stderr + resultado_rm.stderr,
            }
        else:
            return {
                "success": False,
                "message": f"Error al eliminar el contenedor: {resultado_rm.stderr}",
                "stdout": resultado_stop.stdout + resultado_rm.stdout,
                "stderr": resultado_stop.stderr + resultado_rm.stderr,
            }
        
    except FileNotFoundError:
        return {
            "success": False,
            "message": "No se encontró el ejecutable Docker",
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Se agotó el tiempo de espera de Docker Compose",
        }
    except OSError as error:
        return {
            "success": False,
            "message": f"Error al ejecutar Docker: {error}",
        }
