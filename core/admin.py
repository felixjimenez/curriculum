from django.contrib import admin
from .models import Experiencia, Educacion, Habilidad, Proyecto


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'publicado', 'badge', 'url')
    list_editable = ('orden', 'publicado', 'badge')
    list_filter = ('publicado',)
    search_fields = ('titulo', 'descripcion')
    ordering = ('orden', 'titulo')
    fieldsets = (
        (None, {
            'fields': ('titulo', 'descripcion', 'url', 'externo'),
        }),
        ('Apariencia', {
            'fields': ('emoji', 'acento', 'oferta', 'badge'),
        }),
        ('Publicación', {
            'fields': ('publicado', 'orden'),
        }),
    )


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'pais', 'fecha_inicio', 'es_trabajo_actual')
    list_filter = ('pais', 'es_trabajo_actual')
    search_fields = ('cargo', 'empresa', 'descripcion')
    date_hierarchy = 'fecha_inicio'


@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'ano_ingreso', 'ano_egreso', 'sitio_web')
    search_fields = ('titulo', 'institucion')


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'icono_clase', 'icono_color', 'orden', 'url_doc')
    list_filter = ('categoria',)
    list_editable = ('icono_clase', 'icono_color', 'orden')
    search_fields = ('nombre',)
    ordering = ('categoria', 'orden', 'nombre')
    fieldsets = (
        (None, {
            'fields': ('nombre', 'categoria', 'url_doc', 'orden'),
        }),
        ('Header sistema solar', {
            'description': 'Si <strong>icono_clase</strong> está vacío, la habilidad aparece solo en la sección Habilidades (sidebar) y no orbita en el header.',
            'fields': ('icono_clase', 'icono_color'),
        }),
    )
