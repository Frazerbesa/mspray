# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-07 09:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160906_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataEntryClerk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(db_index=1, max_length=255)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Location')),
            ],
        ),
    ]
