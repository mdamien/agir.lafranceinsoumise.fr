# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("people", "0031_auto_20180420_1046")]

    operations = [
        migrations.AlterField(
            model_name="personform",
            name="main_question",
            field=models.CharField(
                blank=True,
                help_text="Uniquement utilisée si des choix de tags sont demandés.",
                max_length=200,
                verbose_name="Intitulé de la question principale",
            ),
        )
    ]
