# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-10 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_auto_20180110_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexingtask',
            name='weekdays_only',
            field=models.BooleanField(default=False),
        ),
    ]