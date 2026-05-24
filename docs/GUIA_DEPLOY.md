# Guía: Correr y publicar el portfolio Django

## Correr la aplicación localmente

### Ubicación del proyecto

```
/home/fjimenez/proyectos/activos/02portafoliof/
├── venv/          ← virtualenv con todas las dependencias
└── curri/         ← raíz del proyecto Django (aquí está manage.py)
```

### Comandos

Usar el Python del virtualenv directamente (sin necesidad de activarlo):

```bash
# Aplicar migraciones
/home/fjimenez/proyectos/activos/02portafoliof/venv/bin/python \
  /home/fjimenez/proyectos/activos/02portafoliof/curri/manage.py migrate

# Levantar servidor de desarrollo
/home/fjimenez/proyectos/activos/02portafoliof/venv/bin/python \
  /home/fjimenez/proyectos/activos/02portafoliof/curri/manage.py runserver
```

- Sitio: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

### Archivo .env (ya existe y está configurado)

Ubicación: `/home/fjimenez/proyectos/activos/02portafoliof/curri/.env`

```
SECRET_KEY=...              ← ya generada
DEBUG=True                  ← modo desarrollo
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

---

## Publicar en Render.com

### Requisitos previos

- Código subido a GitHub (repositorio público o privado)
- Cuenta en [cloudinary.com](https://cloudinary.com) con Cloud Name, API Key y API Secret
- Cuenta en [render.com](https://render.com)

### Paso 1 — Crear la base de datos PostgreSQL en Render

1. **New → PostgreSQL**
2. Nombre: `curriculum-db`, Plan: **Free**
3. Clic en **Create Database**
4. Copiar la **Internal Database URL**

### Paso 2 — Crear el Web Service en Render

1. **New → Web Service**
2. Conectar el repositorio de GitHub
3. Completar la configuración:

| Campo | Valor |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate` |
| Start Command | `gunicorn curri.wsgi` |
| Plan | Free |

> **Importante:** copiar el Build Command tal cual para evitar errores de tipeo.

### Paso 3 — Variables de entorno en Render

En la sección **Environment** del Web Service agregar:

| Variable | Valor |
|---|---|
| `SECRET_KEY` | (misma que en `.env` local) |
| `DEBUG` | `False` |
| `DATABASE_URL` | Internal Database URL del paso 1 |
| `CLOUDINARY_CLOUD_NAME` | (de tu cuenta Cloudinary) |
| `CLOUDINARY_API_KEY` | (de tu cuenta Cloudinary) |
| `CLOUDINARY_API_SECRET` | (de tu cuenta Cloudinary) |
| `PYTHON_VERSION` | `3.11.0` |

> `PYTHON_VERSION=3.11.0` evita que Render use Python 3.14 por defecto, que puede causar incompatibilidades.

### Paso 4 — Crear superusuario en producción

Una vez desplegado, abrir la **Shell** del Web Service en Render y ejecutar:

```bash
python manage.py createsuperuser
```

### Paso 5 — Actualizaciones futuras

```bash
git add .
git commit -m "descripción del cambio"
git push origin main
```

Render detecta el push y redespliega automáticamente.

---

## Errores encontrados y sus soluciones

| Error | Causa | Solución |
|---|---|---|
| `unrecognized arguments: -o-input` | `--no-input` escrito como `-o-input` en el Build Command | Corregir el typo |
| `bash: ip: command not found` | `pip install` escrito como `ip install` en el Build Command | Corregir el typo |
| `ModuleNotFoundError: No module named 'django'` | Virtualenv no activado | Usar la ruta absoluta al Python del venv |

---

## Notas

- En producción (`DEBUG=False`) los logos se guardan en Cloudinary, no en el servidor.
- El plan gratuito de Render se "duerme" tras 15 minutos de inactividad (primera visita tarda ~30 segundos).
- Si Render asigna una URL diferente a `curriculum-66ml.onrender.com`, agregarla en `ALLOWED_HOSTS` dentro de `curri/settings.py`.
