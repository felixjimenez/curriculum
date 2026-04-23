import os

from django.contrib.auth.hashers import make_password
from django.db import migrations


def reset_or_create_admin(apps, schema_editor):
    new_password = os.environ.get("ADMIN_RESET_PASSWORD")
    if not new_password:
        return

    User = apps.get_model("auth", "User")

    user = User.objects.filter(is_superuser=True).order_by("id").first()
    if user is None:
        user = User.objects.create(
            username="admin",
            email="fvjpsg@gmail.com",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

    user.password = make_password(new_password)
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_seed_curriculum"),
    ]

    operations = [
        migrations.RunPython(reset_or_create_admin, migrations.RunPython.noop),
    ]
