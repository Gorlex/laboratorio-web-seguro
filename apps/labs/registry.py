import os
from pathlib import Path
from django.conf import settings

# Registro de laboratorios autorizados
LABORATORIOS = {
    "xss-stored": {
        "nombre": "AlphaPortal - XSS Almacenado",
        "compose_dir": (
            Path(settings.BASE_DIR)
            / "Labs"
            / "xss-stored"
        ),
        "service": "lab-xss",
        "url": "http://127.0.0.1:8081",
    }
}