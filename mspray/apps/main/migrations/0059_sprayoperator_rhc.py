# Generated by Django 2.1.3 on 2018-11-24 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("main", "0058_sprayoperator_district")]

    operations = [
        migrations.AddField(
            model_name="sprayoperator",
            name="rhc",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sop_rhc",
                to="main.Location",
            ),
        )
    ]
