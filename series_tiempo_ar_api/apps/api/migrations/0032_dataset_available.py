# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-04 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20180404_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
