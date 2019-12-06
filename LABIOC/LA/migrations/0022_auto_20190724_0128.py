# Generated by Django 2.2.2 on 2019-07-24 08:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('LA', '0021_auto_20190702_2233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='azurevirtualmachine',
            old_name='azmname',
            new_name='machine_name',
        ),
        migrations.RenameField(
            model_name='redhost',
            old_name='host_name',
            new_name='machine_name',
        ),
        migrations.RenameField(
            model_name='redvirtualmachine',
            old_name='vm_name',
            new_name='machine_name',
        ),
        migrations.RenameField(
            model_name='shhost',
            old_name='host_name',
            new_name='machine_name',
        ),
        migrations.RenameField(
            model_name='shvirtualmachine',
            old_name='vm_name',
            new_name='machine_name',
        ),
        migrations.AlterField(
            model_name='redvirtualmachine',
            name='vmid',
            field=models.UUIDField(default=uuid.UUID('f6e3fbac-6ef5-4816-b500-a68951424168')),
        ),
        migrations.AlterField(
            model_name='shvirtualmachine',
            name='vmid',
            field=models.UUIDField(default=uuid.UUID('bf5d7136-373c-4a68-b544-db1ef91ff6f3')),
        ),
    ]
