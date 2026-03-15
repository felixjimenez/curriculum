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
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Architecture

Standard Django project with a single app (`core`) serving a one-page portfolio site.

**Project layout:** `curri/` is the Django project root (contains `manage.py`). Inside it, `curri/` is the settings package and `core/` is the sole app.

**Data models** (`core/models.py`):
- `Experiencia` — work experience entries with fields for title, company, logo, dates, country (`CL` or `VE`), and a current-job flag. Ordered by most recent first.
- `Educacion` — education entries with institution, degree title, logo, and graduation date. Ordered by most recent first.
- Both models use `django-imagekit` to auto-generate thumbnails from uploaded logos.

**Single view** (`core/views.py`): The `home()` view queries experiences filtered by country (Chile and Venezuela separately) plus all education records, and renders them to `core/templates/core/home.html`.

**Template** (`core/templates/core/home.html`): Bootstrap 5.3 + Font Awesome 6. Displays a profile header, sidebar with education logos, and experience cards grouped by country.

**Admin** (`core/admin.py`): `ExperienciaAdmin` (filterable by country and current status, searchable by title/company) and `EducacionAdmin` are registered for content management.

**Media files** are stored under `media/` (company/institution logos uploaded via admin). Imagekit caches processed thumbnails in `media/CACHE/`.

**Deployment:** Hosted on Render at `curriculum-66ml.onrender.com`. `DEBUG=True` is currently set in `settings.py` — change to `False` for production hardening.
