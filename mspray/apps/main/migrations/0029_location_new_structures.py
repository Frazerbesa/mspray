# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_sprayday_is_new_structure'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='new_structures',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
