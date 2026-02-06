# core/models.py
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

# Modelo para Experiencia Laboral
class Experiencia(models.Model):
    cargo = models.CharField(
        max_length=200, 
        verbose_name="Cargo / Título",
        help_text="Ej: Ingeniero de Software Senior"
    )
    empresa = models.CharField(
        max_length=200, 
        verbose_name="Nombre de la Empresa"
    )
    sitio_web = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="Sitio Web de la Empresa"
    )
    logo = models.ImageField(
        upload_to='logos_empresas/', 
        verbose_name="Logo de la Empresa",
        help_text="Suba una imagen del logo (PNG/JPG)"
    )
    # Generamos automáticamente una miniatura optimizada para la web
    logo_thumbnail = ImageSpecField(
        source='logo',
        processors='',
        format='PNG',
        options={'quality': 90}
    )
    
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Término",
        help_text="Dejar en blanco si es el trabajo actual"
    )
    es_trabajo_actual = models.BooleanField(
        default=False, 
        verbose_name="¿Trabajo Actual?"
    )
    descripcion = models.TextField(
        verbose_name="Descripción de Responsabilidades",
        help_text="Describa sus logros y tareas principales."
    )
    pais = models.CharField(
        max_length=100, 
    #    choices=['chile'],
        default='CL',
        verbose_name="País"
    )

    class Meta:
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencias Laborales"
        ordering = ['-fecha_inicio'] # Ordenar del más reciente al más antiguo

    def __str__(self):
        return f"{self.cargo} en {self.empresa}"

# Modelo para Educación (Casa de Estudio)
class Educacion(models.Model):
    institucion = models.CharField(max_length=200, verbose_name="Institución")
    titulo = models.CharField(max_length=200, verbose_name="Título Obtenido")
    logo = models.ImageField(upload_to='logos_educacion/')
    logo_thumbnail = ImageSpecField(
        source='logo',
        processors='',
        format='PNG',
        options={'quality': 90}
    )
    fecha_graduacion = models.DateField(verbose_name="Fecha de Graduación")
    
    class Meta:
        verbose_name = "Educación"
        verbose_name_plural = "Formación Académica"
        ordering = ['-fecha_graduacion']

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"