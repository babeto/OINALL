# Generated by Django 2.2.1 on 2019-05-28 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LA', '0002_auto_20190528_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shhost',
            name='lastcu',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shhost',
            name='os',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='virtualmachine',
            name='lastcu',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='virtualmachine',
            name='os',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
