import os
import sys

from django.contrib.auth.hashers import make_password
from django.db import migrations


def reset_all_admins(apps, schema_editor):
    new_password = os.environ.get("ADMIN_RESET_PASSWORD")
    User = apps.get_model("auth", "User")

    superusers = list(User.objects.filter(is_superuser=True).order_by("id"))
    usernames = [u.username for u in superusers]
    print(f"[0005_reset_admin_retry] superusers encontrados: {usernames}", file=sys.stderr)

    if not new_password:
        print(
            "[0005_reset_admin_retry] ADMIN_RESET_PASSWORD no está definida, nada que hacer",
            file=sys.stderr,
        )
        return

    if not superusers:
        user = User.objects.create(
            username="admin",
            email="fvjpsg@gmail.com",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        superusers = [user]
        print("[0005_reset_admin_retry] creado superuser 'admin'", file=sys.stderr)

    for user in superusers:
        user.password = make_password(new_password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        print(f"[0005_reset_admin_retry] password reseteado para '{user.username}'", file=sys.stderr)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_reset_admin"),
    ]

    operations = [
        migrations.RunPython(reset_all_admins, migrations.RunPython.noop),
    ]
