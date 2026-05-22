"""
Pobla los iconos (icono_clase + icono_color) del modelo Habilidad para las que
deben aparecer en el header tipo "sistema solar".

Idempotente: usa get_or_create por nombre. Solo actualiza icono_clase, icono_color
y url_doc cuando vienen vacíos (no pisa cambios que Felix haga desde admin).
Categoría y orden solo se setean al crear filas nuevas.

Uso:
    python manage.py poblar_iconos_habilidades              # solo añadir/actualizar vacíos
    python manage.py poblar_iconos_habilidades --forzar    # sobreescribe icono_clase/color/url
"""

from django.core.management.base import BaseCommand
from core.models import Habilidad


# (nombre, categoria, icono_clase, icono_color, url_doc)
# El campo "nombre" se usa como clave única para upsert.
HABILIDADES_SOLAR = [
    # backend
    ("Python 3",            "backend",         "devicon-python-original colored", "",     "https://docs.python.org/es/3/"),
    ("Django 5",            "backend",         "devicon-django-plain colored", "#44B78B", "https://docs.djangoproject.com/es/5.2/"),
    ("Flask 3",             "backend",         "devicon-flask-original",       "#333333", "https://flask.palletsprojects.com/en/stable/"),
    # infraestructura
    ("Linux (Debian 12/13)","infraestructura", "devicon-debian-plain colored", "",        "https://www.debian.org/doc/"),
    ("Docker",              "infraestructura", "devicon-docker-plain colored", "",        "https://docs.docker.com/"),
    ("Git",                 "infraestructura", "devicon-git-plain colored",    "",        "https://git-scm.com/doc"),
    ("Gitea (self-hosted)", "infraestructura", "fab fa-git-alt",               "#609926", "https://docs.gitea.com/"),
    ("VPS Hetzner",         "infraestructura", "fas fa-server",                "#d50c2d", "https://docs.hetzner.com/cloud/"),
    ("Caddy Server",        "infraestructura", "fas fa-shield-alt",            "#1f88c0", "https://caddyserver.com/docs/"),
    # base_datos
    ("PostgreSQL",          "base_datos",      "devicon-postgresql-plain colored", "",    "https://www.postgresql.org/docs/"),
    ("SQLite",              "base_datos",      "devicon-sqlite-plain colored", "",        "https://www.sqlite.org/docs.html"),
    # ia_vision
    ("OpenCV",              "ia_vision",       "devicon-opencv-plain colored", "",        "https://docs.opencv.org/4.x/"),
    ("scikit-learn",        "ia_vision",       "devicon-scikitlearn-plain colored", "",   "https://scikit-learn.org/stable/"),
    # web
    ("Bootstrap 5",         "web",             "devicon-bootstrap-plain colored", "",     "https://getbootstrap.com/docs/5.3/"),
    # extras (sin devicon disponible — usar FontAwesome)
    ("NSD (DNS autoritativo)", "infraestructura", "fas fa-network-wired",      "#2c3e50", "https://nsd.docs.nlnetlabs.nl/"),
    ("MkDocs Material",     "web",             "fas fa-book",                  "#526cfe", "https://squidfunk.github.io/mkdocs-material/"),
    ("Claude Code",         "ia_vision",       "fas fa-robot",                 "#d97757", "https://claude.com/claude-code"),
    ("Bash",                "infraestructura", "devicon-bash-plain colored",   "#4eaa25", "https://www.gnu.org/software/bash/manual/"),
    ("Antigravity",         "ia_vision",       "antigravity-logo",             "#4f46e5", "https://github.com/google-deepmind"),
]


class Command(BaseCommand):
    help = "Pobla icono_clase, icono_color y url_doc del modelo Habilidad para el header sistema solar."

    def add_arguments(self, parser):
        parser.add_argument(
            "--forzar",
            action="store_true",
            help="Sobreescribe icono_clase, icono_color y url_doc aunque ya tengan valor.",
        )

    def handle(self, *args, **opts):
        forzar = opts["forzar"]
        creados = 0
        actualizados = 0
        sin_cambios = 0

        for nombre, categoria, icono_clase, icono_color, url_doc in HABILIDADES_SOLAR:
            obj, fue_creado = Habilidad.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "categoria": categoria,
                    "url_doc": url_doc,
                    "icono_clase": icono_clase,
                    "icono_color": icono_color,
                    "orden": 0,
                },
            )
            if fue_creado:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f"  + creado: {nombre}"))
                continue

            campos_actualizados = []
            if forzar or not obj.icono_clase:
                if obj.icono_clase != icono_clase:
                    obj.icono_clase = icono_clase
                    campos_actualizados.append("icono_clase")
            if forzar or not obj.icono_color:
                if obj.icono_color != icono_color:
                    obj.icono_color = icono_color
                    campos_actualizados.append("icono_color")
            if forzar or not obj.url_doc:
                if obj.url_doc != url_doc and url_doc:
                    obj.url_doc = url_doc
                    campos_actualizados.append("url_doc")

            if campos_actualizados:
                obj.save(update_fields=campos_actualizados)
                actualizados += 1
                self.stdout.write(f"  ~ actualizado: {nombre}  [{', '.join(campos_actualizados)}]")
            else:
                sin_cambios += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Listo: {creados} creados, {actualizados} actualizados, {sin_cambios} sin cambios."
        ))
