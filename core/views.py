from django.shortcuts import render
from.models import Experiencia, Educacion

def home(request):
    # Obtener datos de la BD
    experiencias_cl = Experiencia.objects.filter(pais='CL')
    experiencias_ve = Experiencia.objects.filter(pais='VE')
    educacion = Educacion.objects.all()
    
    context = {
        'experiencias_cl': experiencias_cl,
        'experiencias_ve': experiencias_ve,
        'educacion': educacion,
    }
    return render(request, 'core/home.html', context)