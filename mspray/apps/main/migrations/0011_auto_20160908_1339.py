# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-08 13:39
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20160908_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='directlyobservedsprayingform',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='sprayoperatordailysummary',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
