# Generated by Django 4.1.7 on 2023-05-12 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0005_parkinglot_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parkinglot",
            name="image",
        ),
        migrations.RemoveField(
            model_name="slot",
            name="position",
        ),
        migrations.AddField(
            model_name="booking",
            name="arrived_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="slot",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="webapp.slot"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[
                    ("WAITING", "WAITING"),
                    ("BOOKED", "BOOKED"),
                    ("PARKED", "PARKED"),
                    ("COMPLETED", "COMPLETED"),
                    ("CANCELLED", "CANCELLED"),
                ],
                default="WAITING",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="parkinglot",
            name="description",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="parkinglot",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "PENDING"),
                    ("ACTIVE", "ACTIVE"),
                    ("INACTIVE", "INACTIVE"),
                    ("DELETED", "DELETED"),
                ],
                default="PENDING",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="LotImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="lot_images"),
                ),
                (
                    "lot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webapp.parkinglot",
                    ),
                ),
            ],
        ),
    ]
