from django.db import migrations


def backfill_superuser_role(apps, schema_editor):
    """Give superusers created before the `role` field a valid value.

    Historically `start.sh` performed this fix on every container boot. Moving it
    into a migration makes it versioned, idempotent, and safe to run on a
    multi-instance deploy where every replica was mutating user rows at once.
    """
    CustomUser = apps.get_model('marketplace', 'CustomUser')
    CustomUser.objects.filter(is_superuser=True, role='').update(
        role='retailer', email_verified=True
    )


def noop(apps, schema_editor):
    """The backfill only ever widens data, so reversing needs no action."""


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0007_sellerprofile_latitude_sellerprofile_longitude'),
    ]

    operations = [
        migrations.RunPython(backfill_superuser_role, noop),
    ]