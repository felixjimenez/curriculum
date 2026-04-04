# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All commands run from the `curri/` subdirectory (where `manage.py` lives):

```bash
# Development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic

# Run tests
python manage.py test

# Production server
gunicorn curri.wsgi

# Subir logos locales a Cloudinary (usar cuando se agregan logos nuevos localmente)
python manage.py upload_to_cloudinary
```

Install dependencies:
```bash
pip install -r requirements.txt
```

> **Nota sobre el venv:** El venv fue creado en una ruta antigua. Usar siempre la ruta completa:
> `venv/bin/python3 manage.py <comando>`

---

## Architecture

Standard Django project with a single app (`core`) serving a one-page portfolio site.

**Project layout:** `curri/` is the Django project root (contains `manage.py`). Inside it, `curri/` is the settings package and `core/` is the sole app.

**Data models** (`core/models.py`):
- `Experiencia` — work experience entries with fields for title, company, logo (ImageField), dates, `pais` (`'CL'` or `'VE'`), and a current-job flag. Ordered by most recent first.
- `Educacion` — education entries with institution, degree title, logo (ImageField), and graduation date. Ordered by most recent first.

**Single view** (`core/views.py`): The `home()` view queries experiences filtered by country (Chile and Venezuela separately) plus all education records, and renders them to `core/templates/core/home.html`.

**Template** (`core/templates/core/home.html`): Bootstrap 5.3 + Font Awesome 6. Displays a profile header, sidebar with education logos, and experience cards grouped by country.

**Admin** (`core/admin.py`): `ExperienciaAdmin` (filterable by country and current status, searchable by title/company) and `EducacionAdmin` are registered for content management.

---

## Media Storage (Cloudinary)

### Cómo funciona

- **Local (DEBUG=True):** archivos en `media/`, URLs como `/media/logos_empresas/logo.png`
- **Producción (DEBUG=False):** archivos en Cloudinary, URLs como `https://res.cloudinary.com/dsdjqlaua/image/upload/logos_empresas/logo.png`

### Configuración correcta para Django 5.x

En `settings.py` se usa `STORAGES` (no `DEFAULT_FILE_STORAGE`, que está deprecado desde Django 4.2):

```python
import cloudinary
cloudinary.config(...)   # configuración explícita, obligatoria

if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    STATICFILES_STORAGE = 'whitenoise...'
else:
    STORAGES = {
        "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }
```

### Mecanismo de public_id en Cloudinary

El valor guardado en la DB (ej: `logos_empresas/logo-cc.jpg`) se usa para construir la URL de Cloudinary. Cloudinary separa el nombre de la extensión:
- DB value: `logos_empresas/logo-cc.jpg`
- Cloudinary public_id: `logos_empresas/logo-cc`
- URL resultante: `https://res.cloudinary.com/{cloud}/image/upload/logos_empresas/logo-cc.jpg`

Por eso al subir archivos manualmente, el `public_id` debe ser **sin extensión**:
```python
public_id, _ = os.path.splitext(field_value)
cloudinary.uploader.upload(archivo, public_id=public_id, overwrite=True)
```

### Variables de entorno requeridas (Render)

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta Django |
| `DEBUG` | `False` en producción |
| `DATABASE_URL` | URL de PostgreSQL (con guion bajo, no guion) |
| `CLOUDINARY_CLOUD_NAME` | Nombre del cloud (`dsdjqlaua`) |
| `CLOUDINARY_API_KEY` | API key de Cloudinary |
| `CLOUDINARY_API_SECRET` | API secret de Cloudinary |

> **Atención:** En Render, la variable debe llamarse `DATABASE_URL` (con guion bajo). Si se escribe `DATABASE-URL` (con guion), Django no la lee y cae a SQLite.

---

## Static files

Servidos via WhiteNoise (`CompressedManifestStaticFilesStorage`). Correr `collectstatic` antes de desplegar.

---

## Deployment (Render.com)

- URL: `curriculum-66ml.onrender.com`
- DB: PostgreSQL en producción via `DATABASE_URL`
- Media: Cloudinary (archivos persistentes)
- Static: WhiteNoise (empaquetados en el build)
- Auto-deploy activado desde rama `main` en GitHub

### Diagnóstico de imágenes rotas en producción

Si las imágenes aparecen rotas, revisar los logs de Render:

1. **Si las URLs son `/logos_empresas/...`** (sin dominio Cloudinary):
   - Cloudinary no está generando las URLs → verificar env vars y que `cloudinary.config()` esté en settings
   
2. **Si las URLs son `https://res.cloudinary.com/.../logos_empresas/...` pero dan 404**:
   - Los archivos no existen en Cloudinary → correr `python manage.py upload_to_cloudinary`

3. **Si `logo.url` devuelve rutas relativas pese a tener `STORAGES` bien configurado**:
   - Verificar que `cloudinary.config()` está llamado explícitamente en settings.py (no solo `CLOUDINARY_STORAGE`)

---

## Management Commands

### `upload_to_cloudinary`

Sube todos los logos locales a Cloudinary manteniendo los mismos paths que están en la DB.

```bash
python manage.py upload_to_cloudinary
```

Útil cuando:
- Se agrega un logo nuevo localmente y hay que subirlo a Cloudinary
- La DB de producción apunta a archivos que no existen en Cloudinary
- Se migra de almacenamiento local a Cloudinary
