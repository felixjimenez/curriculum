from django.shortcuts import render
from .models import Experiencia, Educacion, Habilidad


def home(request):
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
