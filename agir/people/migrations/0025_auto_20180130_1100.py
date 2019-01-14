# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-30 10:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("people", "0024_auto_20171220_1737")]

    operations = [
        migrations.AddField(
            model_name="personform",
            name="created",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="created",
            ),
        ),
        migrations.AddField(
            model_name="personform",
            name="modified",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="modified",
            ),
        ),
        migrations.AddField(
            model_name="personformsubmission",
            name="created",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="created",
            ),
        ),
        migrations.AddField(
            model_name="personformsubmission",
            name="modified",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="modified",
            ),
        ),
    ]
