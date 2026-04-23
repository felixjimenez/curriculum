from datetime import date
from django.db import migrations


EDUCACION_A_BORRAR = [
    {"titulo__iexact": "Instructor", "institucion__iexact": "iutirla"},
]


EXPERIENCIAS = [
    {
        "cargo": "Programador / Analista",
        "empresa": "Instituto Venezolano de los Seguros Sociales (IVSS)",
        "fecha_inicio": date(1984, 1, 1),
        "fecha_fin": date(1989, 12, 31),
        "descripcion": "Desarrollo en COBOL sobre mainframe Burroughs.",
        "pais": "VE",
    },
    {
        "cargo": "Programador / Analista",
        "empresa": "Instituto Nacional de la Vivienda (INAVI)",
        "fecha_inicio": date(1989, 1, 1),
        "fecha_fin": date(1994, 12, 31),
        "descripcion": "Desarrollo en COBOL, FoxPro y dBase sobre mainframe IBM.",
        "pais": "VE",
    },
    {
        "cargo": "Instructor de Programación",
        "empresa": "Universidad Santa María",
        "fecha_inicio": date(1994, 1, 1),
        "fecha_fin": date(1995, 12, 31),
        "descripcion": "Docencia en programación en paralelo al trabajo en el Ministerio de Finanzas.",
        "pais": "VE",
    },
    {
        "cargo": "Instructor de Programación",
        "empresa": "CUAM (Colegio Universitario de Administración y Mercadeo)",
        "fecha_inicio": date(2007, 1, 1),
        "fecha_fin": date(2008, 12, 31),
        "descripcion": "Docencia en programación en paralelo al trabajo en el Ministerio de Finanzas.",
        "pais": "VE",
    },
    {
        "cargo": "Instructor de Programación",
        "empresa": 'IUTIRLA (Instituto Universitario Tecnológico Industrial "Rodolfo Loero Arismendi")',
        "fecha_inicio": date(2012, 1, 1),
        "fecha_fin": date(2015, 12, 31),
        "descripcion": "Docencia en programación post-jubilación.",
        "pais": "VE",
    },
]


def cargar_curriculum(apps, schema_editor):
    Educacion = apps.get_model("core", "Educacion")
    Experiencia = apps.get_model("core", "Experiencia")

    for filtro in EDUCACION_A_BORRAR:
        Educacion.objects.filter(**filtro).delete()

    for exp in EXPERIENCIAS:
        Experiencia.objects.get_or_create(
            cargo=exp["cargo"],
            empresa=exp["empresa"],
            defaults={
                "fecha_inicio": exp["fecha_inicio"],
                "fecha_fin": exp["fecha_fin"],
                "descripcion": exp["descripcion"],
                "pais": exp["pais"],
            },
        )


def borrar_curriculum(apps, schema_editor):
    Experiencia = apps.get_model("core", "Experiencia")
    for exp in EXPERIENCIAS:
        Experiencia.objects.filter(
            cargo=exp["cargo"],
            empresa=exp["empresa"],
        ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_educacion_logo_alter_experiencia_logo"),
    ]

    operations = [
        migrations.RunPython(cargar_curriculum, borrar_curriculum),
    ]
