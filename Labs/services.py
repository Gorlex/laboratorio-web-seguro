import subprocess

from .registry import LABORATORIOS


def iniciar_laboratorio(lab_id):
    """
    Inicia un laboratorio autorizado mediante Docker Compose.
    """

    if lab_id not in LABORATORIOS:
        raise ValueError("Laboratorio no autorizado")

    laboratorio = LABORATORIOS[lab_id]

    resultado = subprocess.run(
        [
            "docker",
            "compose",
            "up",
            "-d",
        ],
        cwd=str(laboratorio["compose_dir"]),
        capture_output=True,
        text=True,
        check=False,
    )

    return {
        "success": resultado.returncode == 0,
        "stdout": resultado.stdout,
        "stderr": resultado.stderr,
    }