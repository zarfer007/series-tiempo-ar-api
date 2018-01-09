# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-04 17:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetsIndexingFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('indexing_file', models.FileField(upload_to='datasets_indexing_files/')),
                ('state', models.CharField(choices=[('UPLOADED', 'Cargado'), ('PROCESSING', 'Procesando'), ('PROCESSED', 'Procesado'), ('FAILED', 'Error')], max_length=20)),
                ('logs', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
