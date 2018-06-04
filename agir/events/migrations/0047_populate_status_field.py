# Generated by Django 2.0.5 on 2018-06-04 15:29

from django.db import migrations, models


def populate_status_field(apps, schema):
    RSVP = apps.get_model('events', 'RSVP')

    RSVP.objects.update(status=models.Case(
        models.When(canceled=True, then=models.Value('CA')),
        default=models.Value('CO')
    ))


def populate_canceled_field(apps, schema):
    RSVP = apps.get_model('events', 'RSVP')

    RSVP.objects.update(canceled=models.Case(
        models.When(status='CO', then=models.Value(False)),
        default=models.Value(True)
    ))


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0046_create_status_field'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_status_field,
            reverse_code=populate_canceled_field
        ),
    ]
