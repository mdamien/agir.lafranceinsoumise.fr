# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-21 15:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('people', '0010_person_meta'),
        ('events', '0008_event_contact_hide_phone'),
    ]

    operations = [
        # to add a through model, we run all these steps through a SeparateDatabaseAndState migration
        # so that the database is not touched during this operation
        # see https://stackoverflow.com/a/40654521/1122474
        migrations.SeparateDatabaseAndState(state_operations=[
            migrations.CreateModel(
                name='OrganizerConfig',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ],
                options={
                    'db_table': 'events_event_organizers',
                },
            ),
            migrations.AlterField(
                model_name='event',
                name='organizers',
                field=models.ManyToManyField(related_name='organized_events', through='events.OrganizerConfig',
                                             to='people.Person'),
            ),
            migrations.AddField(
                model_name='organizerconfig',
                name='event',
                field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                        related_name='organizer_configs', to='events.Event'),
            ),
            migrations.AddField(
                model_name='organizerconfig',
                name='person',
                field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                        related_name='organizer_configs', to='people.Person'),
            ),
        ])
    ]
