import cloudinary
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Experiencia, Educacion
import os


class Command(BaseCommand):
    help = 'Sube los logos locales a Cloudinary manteniendo los mismos paths'

    def handle(self, *args, **options):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
        )

        media_root = getattr(settings, 'MEDIA_ROOT', settings.BASE_DIR / 'media')

        modelos = [
            ('Experiencias', Experiencia.objects.all(), 'logo'),
            ('Educacion', Educacion.objects.all(), 'logo'),
        ]

        for nombre, queryset, campo in modelos:
            self.stdout.write(f'\n--- {nombre} ---')
            for obj in queryset:
                field_value = getattr(obj, campo).name  # ej: logos_empresas/logo-cc.jpg
                local_path = os.path.join(media_root, field_value)

                if not os.path.exists(local_path):
                    self.stdout.write(self.style.WARNING(f'  FALTA: {local_path}'))
                    continue

                try:
                    public_id, _ = os.path.splitext(field_value)  # sin extensión
                    result = cloudinary.uploader.upload(
                        local_path,
                        public_id=public_id,
                        overwrite=True,
                        use_filename=False,
                    )
                    self.stdout.write(self.style.SUCCESS(f'  OK: {field_value}'))
                    self.stdout.write(f'      {result["secure_url"]}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ERROR {field_value}: {e}'))

        self.stdout.write(self.style.SUCCESS('\nListo. Recarga el sitio en Render.'))
