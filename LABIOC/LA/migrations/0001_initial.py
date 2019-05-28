# Generated by Django 2.2.1 on 2019-05-28 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('kbnumber', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SHHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=200)),
                ('ip', models.GenericIPAddressField()),
                ('owner', models.CharField(max_length=200)),
                ('os', models.CharField(max_length=200)),
                ('lastcu', models.CharField(max_length=200)),
                ('compliant', models.BooleanField(default=False)),
                ('lastscantime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vulid', models.IntegerField(default=0)),
                ('vulname', models.CharField(max_length=200)),
                ('vuldescription', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='VirtualMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_name', models.CharField(max_length=200)),
                ('ip', models.GenericIPAddressField()),
                ('owner', models.CharField(max_length=200)),
                ('os', models.CharField(max_length=200)),
                ('lastcu', models.CharField(max_length=200)),
                ('compliant', models.BooleanField(default=True)),
                ('lastscantime', models.DateTimeField()),
                ('loc_host', models.ForeignKey(db_column='host_name', on_delete=django.db.models.deletion.CASCADE, to='LA.SHHost')),
            ],
        ),
    ]