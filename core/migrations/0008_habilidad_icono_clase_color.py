from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_add_habilidad_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='habilidad',
            name='icono_clase',
            field=models.CharField(
                blank=True,
                help_text='Clase CSS del icono que aparece en el header (sistema solar). '
                          'Devicon: "devicon-python-plain colored". '
                          'FontAwesome: "fas fa-shield-alt". '
                          'Si queda vacío, la habilidad no aparece orbitando, solo en la sección de Habilidades.',
                max_length=120,
            ),
        ),
        migrations.AddField(
            model_name='habilidad',
            name='icono_color',
            field=models.CharField(
                blank=True,
                help_text='Color hex opcional para overridear el color por defecto del icono. Ej: #44B78B',
                max_length=20,
            ),
        ),
    ]
