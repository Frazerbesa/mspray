# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 07:40
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_household_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
    ]
