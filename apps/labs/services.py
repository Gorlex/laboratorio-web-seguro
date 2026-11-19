import subprocess
from .registry import LABORATORIOS

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
        
        return {
            "success": resultado.returncode == 0,
            "message": (
                "Comando Docker Compose ejecutado correctamente"
                if resultado.returncode == 0
                else "No fue posible iniciar el laboratorio"
            ),
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
