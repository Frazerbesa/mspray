# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-09 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_weeklyreport_structures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyreport',
            name='structures',
            field=models.IntegerField(default=0),
        ),
    ]
