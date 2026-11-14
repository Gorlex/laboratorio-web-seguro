from pathlib import Path
from django.conf import settings


LABORATORIOS = {
    "xss-stored": {
        "nombre": "Reto 1 - XSS Almacenado",
        "compose_dir": (
            Path(settings.BASE_DIR)
            / "Labs"
            / "xss-stored"
        ),
        "service": "lab-xss",
        "url": "http://127.0.0.1:8081",
    }
}