# Generated by Django 2.2.2 on 2019-07-31 05:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('LA', '0023_auto_20190724_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redvirtualmachine',
            name='vmid',
            field=models.UUIDField(default=uuid.UUID('a79c4898-c5bc-405a-affe-f41c8ec84c0e')),
        ),
        migrations.AlterField(
            model_name='shvirtualmachine',
            name='vmid',
            field=models.UUIDField(default=uuid.UUID('970f6cd9-3daf-45cb-9806-ca3046918822')),
        ),
    ]
