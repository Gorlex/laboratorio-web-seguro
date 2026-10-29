# Laboratorios Web Seguros

Plataforma de entrenamiento práctico en seguridad de aplicaciones web.

## Descripción

Aprende seguridad web practicando con laboratorios que contienen vulnerabilidades intencionales en un entorno aislado y controlado.

## Requisitos

- Python 3.12+
- Docker y Docker Compose (recomendado)

## Instalación

### Opción 1: Con Docker (recomendado)

```bash
docker-compose up --build
```

### Opción 2: Local

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python manage.py runserver
```

## Estructura del proyecto

```
laboratorios-web-seguros/
├── config/           # Configuración Django
├── apps/             # Aplicaciones
│   └── dashboard/    # Panel de progreso
├── templates/        # Plantillas HTML
├── static/           # Archivos estáticos
└── docs/             # Documentación
```

## Documentación

- [Arquitectura](docs/architecture.md)
- [Setup](docs/setup.md)
