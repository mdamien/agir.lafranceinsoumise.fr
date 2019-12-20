# Generated by Django 2.2.8 on 2019-12-09 11:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("mailing", "0014_auto_20191206_1758")]

    operations = [
        migrations.AlterField(
            model_name="segment",
            name="exclude_segments",
            field=models.ManyToManyField(
                blank=True,
                related_name="_segment_exclude_segments_+",
                to=settings.NUNTIUS_SEGMENT_MODEL,
                verbose_name="Exclure les personnes membres des segments suivants",
            ),
        )
    ]