# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-28 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_copy_email_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='bounced',
        ),
        migrations.RemoveField(
            model_name='person',
            name='bounced_date',
        ),
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
    ]