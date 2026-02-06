from django.contrib import admin
from.models import Experiencia, Educacion

@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'pais', 'fecha_inicio', 'es_trabajo_actual')
    list_filter = ('pais', 'es_trabajo_actual')
    search_fields = ('cargo', 'empresa', 'descripcion')
    date_hierarchy = 'fecha_inicio'

@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'fecha_graduacion')