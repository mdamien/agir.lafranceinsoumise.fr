# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-18 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0042_auto_20180427_1540")]

    operations = [
        migrations.AddField(
            model_name="event",
            name="max_participants",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Nombre maximum de participants"
            ),
        )
    ]
