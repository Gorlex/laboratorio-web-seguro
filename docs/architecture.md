# Arquitectura: Laboratorios Web Seguros

> Documento de referencia único para humanos y asistentes de IA.
> Si algo aquí contradice una instrucción puntual, se consulta antes de actuar.
> Última actualización: 2026-10-28

## 1. Propósito

Plataforma de entrenamiento práctico en seguridad de aplicaciones web. El usuario avanza por semanas y retos, y practica sobre laboratorios con vulnerabilidades intencionales dentro de un entorno aislado.

## 2. Alcance actual (MVP)

- Dashboard con progreso semanal y tarjetas de retos.
- Datos simulados (`mock_data.py`), sin base de datos real todavía.
- Sin autenticación ni laboratorios vulnerables en esta fase.

**Fuera de alcance por ahora:** login, puntajes persistentes, laboratorios ejecutables, panel de administración.

## 3. Stack

| Capa | Tecnología |
|------|------------|
| Backend | Python 3.12 + Django |
| Frontend | Plantillas Django + HTML/CSS/JS plano + React|
| Contenedores | Docker + docker-compose |
| Base de datos (MVP) | SQLite; PostgreSQL al pasar a producción |

> Ajustar versiones si difieren de las reales del proyecto.

## 4. Estructura de carpetas

```
laboratorios-web-seguros/
├── manage.py
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── config/                 # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                   # Apps de la plataforma (código seguro)
│   └── dashboard/
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── services.py
│       └── mock_data.py
├── templates/
│   ├── base.html
│   └── dashboard/
│       ├── index.html
│       └── components/     # nav, week_progress, challenge_card
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── labs/                   # (futuro) laboratorios vulnerables, aislados
└── docs/
    ├── architecture.md
    └── setup.md
```

## 5. Responsabilidades por capa

- **views.py:** recibe la petición, llama a `services`, devuelve la respuesta. Sin lógica de negocio.
- **services.py:** lógica de negocio (calcular progreso, filtrar retos). No depende de HTTP.
- **models.py:** estructura de datos persistente.
- **mock_data.py:** datos de ejemplo temporales. Se reemplazará por modelos; `services.py` debe ser el único consumidor, para que el cambio no afecte a las vistas.
- **templates/:** solo presentación. Los componentes reutilizables viven en `components/`.
- **static/:** recursos del frontend, sin lógica de negocio.

## 6. Convenciones

- Nombres de código en inglés (`challenge`, `week_progress`); textos visibles al usuario en español.
- Una app Django por dominio funcional (`dashboard`, `accounts`, `challenges`...).
- Funciones pequeñas, con nombre descriptivo y docstring breve.
- Estilo Python: PEP 8; formateo con `black` y revisión con `flake8` (cuando se incorporen).
- Plantillas: herencia desde `base.html`, sin CSS ni JS en línea.
- Commits pequeños y descriptivos (`feat:`, `fix:`, `docs:`, `refactor:`).

## 7. Reglas de seguridad (críticas)

1. **La plataforma principal debe ser segura.** Solo los laboratorios contienen vulnerabilidades intencionales.
2. **Los laboratorios vulnerables viven en `labs/`**, en contenedores propios, con base de datos y credenciales independientes de la plataforma.
3. **Nunca exponer laboratorios vulnerables a internet** sin aislamiento de red.
4. **Ningún secreto en el código.** `SECRET_KEY`, contraseñas y tokens se leen desde variables de entorno; `.env` está en `.gitignore` y se documenta `.env.example`.
5. `DEBUG=False` en producción.
6. Cada vulnerabilidad intencional debe estar **marcada con un comentario** `# VULNERABLE (intencional): <tipo>` para evitar que se confunda con un error real.
7. No ejecutar comandos del sistema ni acceder al sistema de archivos del host desde los laboratorios.

## 8. Reglas para asistentes de IA

- Leer este documento antes de proponer o modificar código.
- No crear carpetas ni archivos fuera de la estructura de la sección 4 sin proponerlo primero.
- No agregar dependencias sin indicarlo y justificarlo en `requirements.txt`.
- No mezclar código vulnerable con el de la plataforma principal.
- Entregar cambios pequeños y verificables: indicar qué archivos toca cada cambio.
- Si hay duda de diseño, preguntar o proponer opciones en lugar de decidir en silencio.
- Al terminar un cambio relevante, sugerir la actualización de la sección 10 (Decisiones).

## 9. Roadmap

| Fase | Contenido |
|------|-----------|
| 1 | Dashboard con datos simulados (actual) |
| 2 | Modelos reales: semanas, retos, progreso |
| 3 | Autenticación de usuarios |
| 4 | Primer laboratorio aislado (por ejemplo XSS) en `labs/` |
| 5 | Puntajes, validación de retos, más laboratorios |
| 6 | Settings por entorno (`base`, `dev`, `prod`) y despliegue |

## 10. Registro de decisiones

| Fecha | Decisión | Motivo |
|-------|----------|--------|
| 2026-10-28 | Apps de la plataforma bajo `apps/` | Escalar al agregar dominios |
| 2026-10-28 | Plantillas y estáticos centralizados en la raíz | Simplicidad en el MVP |
| 2026-10-28 | Laboratorios vulnerables separados en `labs/` | Aislamiento de seguridad |
| 2026-10-28 | Datos simulados detrás de `services.py` | Facilitar el paso a modelos reales |

## 11. Definición de "terminado"

Un cambio se considera terminado cuando:

- [ ] Respeta la estructura y las convenciones de este documento.
- [ ] Se puede ejecutar con `docker-compose up` sin pasos manuales ocultos.
- [ ] No introduce secretos ni vulnerabilidades fuera de `labs/`.
- [ ] Está documentado en `README.md` o `docs/setup.md` si cambia la forma de ejecutarlo.
