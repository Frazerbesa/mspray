# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-21 05:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_sprayday_was_sprayed'),
    ]

    operations = [
        migrations.CreateModel(
            name='SprayDayHealthCenterLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.SprayDay')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Location')),
            ],
        ),
    ]
