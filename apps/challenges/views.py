from django.shortcuts import render

def detail(request, challenge_id):
    """Página de detalle de un reto específico."""
    # Datos específicos para el Reto 1 - ahora en Semana 2
    if challenge_id == 1:
        challenge_data = {
            'id': 1,
            'numero': 1,
            'titulo': 'Entradas no válidas en aplicaciones web',
            'semana_numero': 2,
            'estado': 'Pendiente',  # Valor de demostración
            'objetivo': 'Demostrar cómo el sistema acepta entradas no válidas y cómo el navegador de la víctima las ejecuta.',
            'contexto': {
                'de': 'Dirección de Ciberseguridad – AlphaHealth Corp.',
                'para': 'Equipo de Respuesta a Incidentes (Tú)',
                'asunto': 'Urgente: Posible compromiso de cuentas de médicos y fuga de datos en el portal clínico',
                'situacion': 'Trabajas para AlphaHealth Corp., una multinacional que gestiona hospitales y clínicas privadas. Hace tres meses, la empresa lanzó "AlphaPortal", una plataforma web interna donde los médicos, enfermeros y pacientes interactúan. A través de este portal, los médicos pueden ver el historial clínico de los pacientes y dejar notas de evolución médica. Por ejemplo: "Paciente presenta mejoría tras cambiar dosis de Omeprazol".',
                'incidente': 'La crisis: Ayer por la tarde, el Director de Oncología reportó un comportamiento anómalo. Tras iniciar sesión en el portal y revisar la ficha de un paciente específico, su navegador se redirigió automáticamente a una página externa de inicio de sesión falsa. Pensando que su sesión había caducado, introdujo sus credenciales corporativas. Hace dos horas, los sistemas de monitoreo detectaron que la cuenta de este director fue utilizada desde una IP en el extranjero para descargar masivamente expedientes médicos confidenciales.',
                'hipotesis': 'Los desarrolladores aseguran que la base de datos está encriptada y que el formulario de inicio de sesión es seguro. Sin embargo, el equipo de seguridad sospecha de una vulnerabilidad de XSS Almacenado (Stored XSS) en el sistema de comentarios médicos. La hipótesis es que un atacante introdujo código malicioso en una nota médica. Cuando el Director de Oncología abrió la ficha para revisar el historial, su navegador ejecutó el contenido introducido en la aplicación. Como consecuencia, se habría producido el compromiso de su sesión corporativa.'
            },
            'instrucciones': [
                {
                    'paso': 1,
                    'titulo': 'Autenticación y navegación',
                    'contenido': 'Desde el menú principal, acceda al Panel del Paciente. Localice la sección o formulario titulado "Notas Médicas".'
                },
                {
                    'paso': 2,
                    'titulo': 'Preparación de la prueba',
                    'contenido': 'Copie la siguiente prueba de concepto:<br><pre class="bg-light p-3 rounded"><code>&lt;script&gt;alert("Hola Mundo")&lt;/script&gt;</code></pre><br>Opcional — Variante avanzada: <br><pre class="bg-light p-3 rounded"><code>&lt;script&gt;alert(document.cookie)&lt;/script&gt;</code></pre>'
                },
                {
                    'paso': 3,
                    'titulo': 'Inyección de la entrada no válida',
                    'contenido': 'En el campo "Notas Médicas", pegue el contenido de prueba indicado en el paso anterior. No modifique el resto del formulario. Deje los demás campos con valores válidos. Haga clic en Guardar o Enviar.'
                },
                {
                    'paso': 4,
                    'titulo': 'Verificación de la persistencia',
                    'contenido': 'Una vez guardada la nota, recargue la página. También puede navegar nuevamente a la vista donde se muestran las notas médicas. Observe si el navegador procesa automáticamente el contenido introducido al mostrar la nota.'
                },
                {
                    'paso': 5,
                    'titulo': 'Captura de evidencia',
                    'contenido': 'Debe tomar una captura de pantalla. La evidencia debe mostrar: La alerta del navegador. La URL del laboratorio. Para la variante avanzada opcional, puede repetir el procedimiento con la segunda prueba de concepto y registrar la evidencia correspondiente.'
                }
            ]
        }
    else:
        # Datos genéricos para otros retos
        challenge_data = {
            'id': challenge_id,
            'numero': challenge_id,
            'titulo': f'Reto {challenge_id}',
            'semana_numero': 1,
            'estado': 'Pendiente'
        }
    
    context = {
        'challenge': challenge_data
    }
    return render(request, 'challenges/detail.html', context)