# Generated by Django 4.1.7 on 2023-05-01 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0003_parkinglot_image_alter_slot_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="take_away_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]