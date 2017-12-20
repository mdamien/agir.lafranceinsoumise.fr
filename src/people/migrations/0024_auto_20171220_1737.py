# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-20 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0023_auto_20171129_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='coordinates_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Coordonnées manuelles'), (10, 'Coordonnées automatiques précises'), (20, 'Coordonnées automatiques approximatives (niveau rue)'), (30, 'Coordonnées automatiques approximatives (ville)'), (50, 'Coordonnées automatiques (qualité inconnue)'), (255, 'Coordonnées introuvables')], editable=False, help_text='Comment les coordonnées ci-dessus ont-elle été acquises', null=True, verbose_name='type de coordonnées'),
        ),
    ]
