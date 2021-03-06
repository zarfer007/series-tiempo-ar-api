# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-21 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_distribution_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='identifier',
            field=models.CharField(default='sspm', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='data_hash',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='error',
            field=models.TextField(default=''),
        ),
    ]
