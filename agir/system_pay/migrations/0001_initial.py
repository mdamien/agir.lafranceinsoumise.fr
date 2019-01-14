# Generated by Django 2.0.6 on 2018-06-29 13:20

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [("payments", "0006_auto_20180628_1503")]

    operations = [
        migrations.CreateModel(
            name="SystemPayTransaction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "En attente"),
                            (1, "Terminé"),
                            (2, "Abandonné"),
                            (3, "Annulé"),
                            (4, "Refusé"),
                        ],
                        default=0,
                        verbose_name="status",
                    ),
                ),
                (
                    "webhook_calls",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, default=list, verbose_name="Événements de paiement"
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="payments.Payment",
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]
