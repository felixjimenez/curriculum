from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Experiencia, Educacion, Habilidad, Visita, Proyecto


def home(request):
    """Portada / portafolio: grilla de tarjetas leída de la tabla Proyecto."""
    proyectos = Proyecto.objects.filter(publicado=True)
    return render(request, 'core/portada.html', {'proyectos': proyectos})


def curriculum(request):
    experiencias_cl = Experiencia.objects.filter(pais='CL')
    experiencias_ve = Experiencia.objects.filter(pais='VE')
    educacion = Educacion.objects.all()

    # Habilidades que orbitan en el header: solo las que tienen icono asignado.
    habilidades_solar = list(
        Habilidad.objects.exclude(icono_clase='').order_by('categoria', 'orden', 'nombre')
    )
    total = len(habilidades_solar)
    paso = 360 / total if total else 0
    for i, h in enumerate(habilidades_solar):
        h.angulo = round(i * paso, 2)

    # Habilidades para sidebar — agrupadas por categoría, en el orden del modelo.
    categorias_orden = [c[0] for c in Habilidad.CATEGORIAS]
    etiquetas = dict(Habilidad.CATEGORIAS)
    todas = list(Habilidad.objects.all())
    habilidades_por_categoria = []
    for cat in categorias_orden:
        items = [h for h in todas if h.categoria == cat]
        if items:
            habilidades_por_categoria.append({
                'label': etiquetas[cat],
                'items': items,
            })

    context = {
        'experiencias_cl': experiencias_cl,
        'experiencias_ve': experiencias_ve,
        'educacion': educacion,
        'habilidades_solar': habilidades_solar,
        'habilidades_por_categoria': habilidades_por_categoria,
    }
    return render(request, 'core/home.html', context)


def admin_visitas(request):
    """Panel simple de visitas (staff de Django o ?token=VISITAS_TOKEN)."""
    token = request.GET.get('token', '')
    ok = request.user.is_staff or (settings.VISITAS_TOKEN and token == settings.VISITAS_TOKEN)
    if not ok:
        raise Http404()
    try:
        total = Visita.objects.count()
        hoy = Visita.objects.filter(ts__date=timezone.now().date()).count()
        desde = timezone.now() - timedelta(days=30)
        por_dia = list(Visita.objects.filter(ts__gte=desde)
                       .annotate(dia=TruncDate('ts')).values('dia')
                       .annotate(n=Count('id')).order_by('-dia'))
        top_rutas = list(Visita.objects.values('ruta')
                         .annotate(n=Count('id')).order_by('-n')[:20])
        recientes = list(Visita.objects.order_by('-id')[:50])
    except Exception:
        # La tabla aún no existe (falta correr `python manage.py migrate`).
        return HttpResponse(
            "<p>Contador de visitas: la tabla aún no está creada. "
            "Ejecuta <code>python manage.py migrate</code> en el servidor.</p>",
            status=503,
        )
    fdia = "".join(f"<tr><td>{r['dia']}</td><td>{r['n']}</td></tr>" for r in por_dia)
    frutas = "".join(f"<tr><td>{r['ruta']}</td><td>{r['n']}</td></tr>" for r in top_rutas)
    frec = "".join(
        f"<tr><td>{v.ts:%Y-%m-%d %H:%M}</td><td>{v.ruta}</td><td>{v.ip}</td>"
        f"<td>{v.user_agent[:60]}</td></tr>" for v in recientes)
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Visitas · CV</title>
<style>body{{font-family:system-ui,sans-serif;margin:1.2rem;color:#222}}
h1{{font-size:1.3rem}} h2{{font-size:1rem;margin-top:1.5rem}}
table{{border-collapse:collapse;width:100%;max-width:680px;margin:.4rem 0}}
td,th{{border:1px solid #ccc;padding:.3rem .5rem;font-size:.85rem;text-align:left}}
.big{{font-size:2rem;font-weight:700}}</style></head><body>
<h1>📊 Contador de visitas — CV</h1>
<p>Total: <span class="big">{total}</span> &nbsp;·&nbsp; Hoy: <strong>{hoy}</strong></p>
<h2>Últimos 30 días</h2><table><tr><th>Día</th><th>Visitas</th></tr>{fdia}</table>
<h2>Rutas más visitadas</h2><table><tr><th>Ruta</th><th>Visitas</th></tr>{frutas}</table>
<h2>Últimas 50 visitas</h2><table><tr><th>Cuándo</th><th>Ruta</th><th>IP</th><th>Navegador</th></tr>{frec}</table>
</body></html>"""
    return HttpResponse(html)
