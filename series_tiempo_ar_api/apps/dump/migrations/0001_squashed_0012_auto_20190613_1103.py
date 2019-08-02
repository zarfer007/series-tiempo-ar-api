# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-08-02 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import minio_storage.storage
import series_tiempo_ar_api.apps.dump.models


class Migration(migrations.Migration):

    replaces = [('dump', '0001_initial'), ('dump', '0002_auto_20181003_1735_squashed_0005_auto_20181004_1028'), ('dump', '0003_auto_20181009_1131_squashed_0005_generatedumptask_file_type'), ('dump', '0004_auto_20181022_1237'), ('dump', '0005_auto_20181022_1304'), ('dump', '0006_zipdumpfile'), ('dump', '0007_auto_20181102_1542'), ('dump', '0008_auto_20181129_1247'), ('dump', '0009_auto_20181219_1227'), ('dump', '0010_auto_20190123_1530'), ('dump', '0011_generatedumptask_node'), ('dump', '0012_auto_20190613_1103')]

    initial = True

    dependencies = [
        ('django_datajsonar', '0006_synchronizer_node'),
        ('django_datajsonar', '0012_auto_20180831_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenerateDumpTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('RUNNING', 'Procesando catálogos'), ('FINISHED', 'Finalizada')], max_length=20)),
                ('created', models.DateTimeField()),
                ('finished', models.DateTimeField(null=True)),
                ('logs', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DumpFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=minio_storage.storage.MinioMediaStorage(), upload_to=series_tiempo_ar_api.apps.dump.models.dumpfile_upload_to)),
                ('file_name', models.CharField(choices=[('series-tiempo', 'Series de tiempo (valores + metadatos)'), ('series-tiempo-valores', 'Series de tiempo (valores)'), ('series-tiempo-metadatos', 'Series de tiempo (metadatos)'), ('series-tiempo-fuentes', 'Series de tiempo (fuentes)')], max_length=64)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dump.GenerateDumpTask')),
                ('file_type', models.CharField(choices=[('csv', 'CSV'), ('xlsx', 'XLSX'), ('zip', 'ZIP'), ('sql', 'SQL')], default='csv', max_length=12)),
                ('node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_datajsonar.Node')),
            ],
        ),
        migrations.AddField(
            model_name='generatedumptask',
            name='file_type',
            field=models.CharField(choices=[('csv', 'CSV'), ('xlsx', 'XLSX'), ('sql', 'SQL'), ('dta', 'DTA')], default='CSV', max_length=12),
        ),
        migrations.CreateModel(
            name='ZipDumpFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=minio_storage.storage.MinioMediaStorage(), upload_to=series_tiempo_ar_api.apps.dump.models.zipfile_upload_to)),
                ('dump_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dump.DumpFile')),
            ],
        ),
        migrations.AlterField(
            model_name='dumpfile',
            name='file_type',
            field=models.CharField(choices=[('csv', 'CSV'), ('xlsx', 'XLSX'), ('zip', 'ZIP'), ('sqlite', 'SQL'), ('dta', 'DTA')], default='csv', max_length=12),
        ),
        migrations.AlterField(
            model_name='generatedumptask',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterModelOptions(
            name='generatedumptask',
            options={'verbose_name': 'Corrida de generación de dumps', 'verbose_name_plural': 'Corridas de generación de dumps'},
        ),
        migrations.AddField(
            model_name='generatedumptask',
            name='node',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_datajsonar.Node'),
        ),
    ]
