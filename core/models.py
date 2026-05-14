# core/models.py
from django.db import models


class Habilidad(models.Model):
    CATEGORIAS = [
        ('infraestructura', 'Infraestructura / DevOps'),
        ('backend',         'Backend Python'),
        ('base_datos',      'Bases de Datos'),
        ('ia_vision',       'IA / Visión Computacional'),
        ('web',             'Web Frontend'),
        ('legado',          'Sistemas Legados'),
    ]

    nombre = models.CharField(max_length=80)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS)
    url_doc = models.URLField(blank=True, help_text="Link a documentación oficial")
    icono_clase = models.CharField(
        max_length=120,
        blank=True,
        help_text='Clase CSS del icono que aparece en el header (sistema solar). '
                  'Devicon: "devicon-python-plain colored". '
                  'FontAwesome: "fas fa-shield-alt". '
                  'Si queda vacío, la habilidad no aparece orbitando, solo en la sección de Habilidades.',
    )
    icono_color = models.CharField(
        max_length=20,
        blank=True,
        help_text='Color hex opcional para overridear el color por defecto del icono. Ej: #44B78B',
    )
    orden = models.PositiveSmallIntegerField(default=0, help_text="Orden dentro de la categoría")

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ['categoria', 'orden', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"


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
        blank=True,
        null=True,
        verbose_name="Logo de la Empresa",
        help_text="Suba una imagen del logo (PNG/JPG)"
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
    logo = models.ImageField(upload_to='logos_educacion/', blank=True, null=True)
    sitio_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Sitio Web de la Institución"
    )
    ano_ingreso = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Año de Ingreso"
    )
    ano_egreso = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Año de Egreso"
    )

    class Meta:
        verbose_name = "Educación"
        verbose_name_plural = "Formación Académica"
        ordering = ['-ano_egreso']

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"