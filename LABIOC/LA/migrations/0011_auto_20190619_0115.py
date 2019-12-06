# Generated by Django 2.2.2 on 2019-06-19 08:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('LA', '0010_auto_20190619_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='azurevirtualmachine',
            name='compliant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='azurevirtualmachine',
            name='rebootrequired',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='azurevirtualmachine',
            name='vmid',
            field=models.UUIDField(default=uuid.UUID('a6fe5666-1241-47cf-b7f5-0791501b16a3')),
        ),
        migrations.AlterField(
            model_name='redhost',
            name='rebootrequired',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='redvirtualmachine',
            name='compliant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='redvirtualmachine',
            name='rebootrequired',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='redvirtualmachine',
            name='vmid',
            field=models.UUIDField(default=uuid.UUID('bb246319-4f0f-427f-846f-c2ae16293ee9')),
        ),
        migrations.AlterField(
            model_name='shhost',
            name='rebootrequired',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='shvirtualmachine',
            name='compliant',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='shvirtualmachine',
            name='rebootrequired',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='shvirtualmachine',
            name='vmid',
            field=models.UUIDField(default=uuid.UUID('9fa95d17-c0b8-4865-86e3-c9fe9cff5c64')),
        ),
    ]
