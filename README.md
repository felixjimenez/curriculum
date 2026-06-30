# portafolio
# curriculum

CV / portafolio personal hecho con **Django 5.2** (app `core`), desplegado con Docker
(gunicorn) y archivos estáticos vía WhiteNoise.

## Contador de visitas (para el administrador)

El sitio registra **cada visita a una página** en la tabla `visitas` (modelo
`core.Visita`): ruta, fecha/hora, IP y navegador. Lo hace el middleware
`core/middleware.py` (`VisitCounterMiddleware`), que ignora el panel de Django
(`/admin`), los estáticos/media y los recursos por extensión.

**Cómo lo miras (uso personal):**

```
/admin/visitas/?token=EL_TOKEN
```

- Si estás logueado como **staff** de Django, lo ves directo.
- Si no, se protege con la variable de entorno **`VISITAS_TOKEN`**. Si no coincide,
  responde **404** (queda oculto).

Muestra **total**, **visitas de hoy**, **conteo por día** (30 días), **rutas más
visitadas** y las **últimas 50 visitas**.

> **Importante al desplegar:** la tabla nueva requiere correr las migraciones
> (`python manage.py migrate`) en el servidor, y definir `VISITAS_TOKEN` en el entorno.
> Si entras al panel antes de migrar, te avisa con un mensaje (no rompe el sitio).
