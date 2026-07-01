from django.db import migrations


PROYECTOS = [
    {
        'titulo': 'Aprende Inglés',
        'url': 'https://ingles.felixjimenez.cl',
        'emoji': '🇬🇧',
        'descripcion': 'Practica inglés con lecciones interactivas que suben de nivel contigo, '
                       'a tu ritmo y sin apuro. La inteligencia artificial te corrige y te acompaña.',
        'oferta': '🎉 Inauguración: 5 lecciones por $3.000 · la 1ª es gratis',
        'badge': '',
        'acento': '#4f46e5',
        'externo': True,
        'orden': 10,
    },
    {
        'titulo': 'Aprende a Administrar tu PC',
        'url': 'https://aprende.felixjimenez.cl',
        'emoji': '🖥️',
        'descripcion': 'Todos los pasos para manejar tus equipos y servidores, e instalar '
                       'tus aplicaciones en la web. De cero a producción, explicado paso a paso.',
        'oferta': '🎉 Inauguración: 5 lecciones por $3.000 · la 1ª es gratis',
        'badge': '',
        'acento': '#7c3aed',
        'externo': True,
        'orden': 20,
    },
    {
        'titulo': 'Tienda',
        'url': 'https://tienda.felixjimenez.cl',
        'emoji': '🛒',
        'descripcion': 'Aplicación para la venta de tus productos: catálogo, inventario y '
                       'registro de ventas en un solo lugar. Mírala funcionando de verdad.',
        'oferta': '',
        'badge': 'En vivo',
        'acento': '#10b981',
        'externo': True,
        'orden': 30,
    },
    {
        'titulo': 'Mi Currículum',
        'url': '/curriculum',
        'emoji': '📜',
        'descripcion': 'Más de 30 años al servicio de la informática: mainframes, COBOL, redes '
                       'y hoy Python e inteligencia artificial. Conoce mi largo camino.',
        'oferta': '',
        'badge': '',
        'acento': '#0ea5e9',
        'externo': False,
        'orden': 40,
    },
    {
        'titulo': 'Imágenes',
        'url': 'https://fotos.felixjimenez.cl',
        'emoji': '🖼️',
        'descripcion': 'Organiza las fotos de tu familia y amigos con inteligencia artificial '
                       'que reconoce rostros y agrupa a las personas por sí sola.',
        'oferta': '',
        'badge': '',
        'acento': '#f59e0b',
        'externo': True,
        'orden': 50,
    },
    {
        'titulo': 'Aplicaciones web a tu medida',
        'url': 'https://adderlyconstrucciones.cl',
        'emoji': '🌐',
        'descripcion': 'Desarrollamos la aplicación que tu negocio necesita y te entrenamos '
                       'para que la manejes solo. Mira un caso real: Adderly Construcciones.',
        'oferta': '',
        'badge': 'Caso real',
        'acento': '#ec4899',
        'externo': True,
        'orden': 60,
    },
]


def crear_proyectos(apps, schema_editor):
    Proyecto = apps.get_model('core', 'Proyecto')
    for datos in PROYECTOS:
        # Idempotente: si ya existe una tarjeta con ese título, no la duplica
        # ni pisa los cambios que Felix haya hecho desde el admin.
        Proyecto.objects.get_or_create(titulo=datos['titulo'], defaults=datos)


def borrar_proyectos(apps, schema_editor):
    Proyecto = apps.get_model('core', 'Proyecto')
    titulos = [p['titulo'] for p in PROYECTOS]
    Proyecto.objects.filter(titulo__in=titulos).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_proyecto'),
    ]

    operations = [
        migrations.RunPython(crear_proyectos, borrar_proyectos),
    ]
