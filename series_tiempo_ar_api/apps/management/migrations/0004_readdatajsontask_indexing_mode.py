# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-09 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20180720_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='readdatajsontask',
            name='indexing_mode',
            field=models.CharField(choices=[('updated', 'Sólo actualizados'), ('all', 'Todos (forzar indexación)')], default='updated', max_length=200),
        ),
    ]
