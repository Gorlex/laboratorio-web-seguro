import subprocess
from django.utils import timezone
from .registry import LABORATORIOS
from .models import LaboratorioActivo
from uuid import uuid4

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
    
    # Construir el comando Docker Compose para verificar si el contenedor ya está corriendo
    comando_ps = [
        "docker",
        "compose",
        "-f",
        str(compose_file),
        "ps",
        "--status",
        "running",
        "-q",
        laboratorio["service"],
    ]
    
    try:
        # Verificar el estado actual del contenedor
        resultado_ps = subprocess.run(
            comando_ps,
            cwd=str(compose_dir),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        
        # Si el comando falla, devolver error
        if resultado_ps.returncode != 0:
            return {
                "success": False,
                "message": f"Error al verificar estado del contenedor: {resultado_ps.stderr}",
                "stdout": resultado_ps.stdout,
                "stderr": resultado_ps.stderr,
            }
        
        # Determinar si hay contenedor activo
        container_running = bool(resultado_ps.stdout.strip())
        
        # Obtener el registro actual del laboratorio antes de ejecutar Docker
        try:
            lab_registro = LaboratorioActivo.objects.get(lab_id=lab_id)
        except LaboratorioActivo.DoesNotExist:
            lab_registro = None
        
        # Verificar combinaciones inconsistentes antes de ejecutar Docker
        if (     container_running     and lab_registro     and lab_registro.activo     and lab_registro.execution_id is not None ):
            # El contenedor está corriendo y el registro indica activo con execution_id - continuar ejecución
            # Conservar execution_id y fecha_inicio, solo actualizar ultima_actividad
            lab_registro.ultima_actividad = timezone.now()
            lab_registro.save()
            return {
                "success": True,
                "message": "Laboratorio ya está en ejecución",
                "stdout": resultado_ps.stdout,
                "stderr": resultado_ps.stderr,
            }
        elif not container_running and lab_registro and lab_registro.activo:
            # El contenedor no está corriendo pero el registro indica activo - inconsistencia
            return {
                "success": False,
                "message": "Inconsistencia detectada: el registro indica que el laboratorio está activo, pero no se encuentra contenedor en ejecución",
            }
        elif container_running and lab_registro and not lab_registro.activo:
            # El contenedor está corriendo pero el registro indica inactivo - inconsistencia
            return {
                "success": False,
                "message": "Inconsistencia detectada: se encontró contenedor en ejecución, pero el registro indica que no está activo",
            }
        elif not container_running and lab_registro and not lab_registro.activo:
            # El contenedor no está corriendo y el registro indica inactivo
            # Verificar si tiene execution_id (puede ser válido)
            if lab_registro.execution_id is None:
                # Registro inactivo sin execution_id - nueva ejecución
                pass  # Continuar con la lógica de nueva ejecución
            else:
                # Registro inactivo con execution_id - continuar ejecución
                pass  # Continuar con la lógica de nueva ejecución
        elif lab_registro is None and not container_running:
            # No existe registro y no hay contenedor activo - nueva ejecución
            pass  # Continuar con la lógica de nueva ejecución
        else:
            # Otra combinación inconsistente
            return {
                "success": False,
                "message": "Combinación de estados inconsistente",
            }
        
        # Construir el comando Docker Compose para iniciar
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
            # Crear o actualizar el registro del laboratorio
            if lab_registro is None:
                # Es una nueva ejecución
                execution_id = uuid4()
                LaboratorioActivo.objects.create(
                    lab_id=lab_id,
                    execution_id=execution_id,
                    activo=True,
                    fecha_inicio=timezone.now(),
                    ultima_actividad=timezone.now(),
                    fecha_finalizacion=None
                )
            else:
                # Registrar una nueva ejecución
                ahora = timezone.now()
                lab_registro.execution_id = uuid4()
                lab_registro.activo = True
                lab_registro.fecha_inicio = ahora
                lab_registro.ultima_actividad = ahora
                lab_registro.fecha_finalizacion = None
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
