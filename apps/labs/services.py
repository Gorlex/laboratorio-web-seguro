import subprocess
from .registry import LABORATORIOS

def iniciar_laboratorio(lab_id):
    """Inicia un laboratorio autorizado mediante Docker Compose."""
    
    # Verificar que el laboratorio esté en la lista blanca
    if lab_id not in LABORATORIOS:
        return {
            'success': False,
            'error': f'Laboratorio {lab_id} no autorizado',
            'message': 'El laboratorio solicitado no está en la lista blanca'
        }
    
    laboratorio = LABORATORIOS[lab_id]
    
    # Verificar que el directorio del laboratorio existe
    compose_dir = laboratorio['compose_dir']
    if not compose_dir.exists():
        return {
            'success': False,
            'error': f'Directorio no encontrado: {compose_dir}',
            'message': f'No se encontró el directorio del laboratorio: {compose_dir}'
        }
    
    try:
        # Ejecutar docker compose up -d desde el directorio del laboratorio
        result = subprocess.run(
            [
                'docker',
                'compose',
                'up',
                '-d'
            ],
            cwd=str(compose_dir),
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            return {
                'success': True,
                'message': f'Laboratorio {lab_id} iniciado correctamente',
                'stdout': result.stdout,
                'stderr': result.stderr,
                'service': laboratorio['service']
            }
        else:
            return {
                'success': False,
                'error': 'Error al iniciar el laboratorio',
                'message': f'Error: {result.stderr}',
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': 'Excepción al ejecutar Docker',
            'message': str(e)
        }