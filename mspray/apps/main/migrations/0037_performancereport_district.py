# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-13 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_performancereport_not_eligible'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancereport',
            name='district',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE,
                to='main.Location'),
            preserve_default=False,
        ),
    ]
