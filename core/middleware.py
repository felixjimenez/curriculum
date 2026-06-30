"""
Contador de visitas (middleware).

Registra una fila en la tabla `visitas` por cada visita a una *página* del sitio.
Se saltan el panel de Django (`/admin`), los estáticos y media (`/static`, `/media`),
los recursos por extensión y el propio panel de estadísticas. Nunca rompe la
respuesta: si el registro falla, la página se sirve igual.
"""
from .models import Visita

_ASSET_EXT = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".map", ".json", ".txt", ".xml",
)
_SKIP_PREFIXES = ("/admin", "/static", "/media")


def _es_pagina(path):
    p = path.lower()
    if any(p.startswith(pre) for pre in _SKIP_PREFIXES):
        return False
    if p.endswith(_ASSET_EXT):
        return False
    return True


class VisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET" and _es_pagina(request.path):
            try:
                Visita.objects.create(
                    ruta=request.path,
                    ip=request.META.get("REMOTE_ADDR", "") or "",
                    user_agent=(request.META.get("HTTP_USER_AGENT", "") or "")[:300],
                )
            except Exception:
                pass
        return self.get_response(request)
