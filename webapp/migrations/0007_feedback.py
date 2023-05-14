# Generated by Django 4.1.7 on 2023-05-13 17:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0006_remove_parkinglot_image_remove_slot_position_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                ("updated_at", models.DateTimeField(auto_created=True, auto_now=True)),
                (
                    "created_at",
                    models.DateTimeField(auto_created=True, auto_now_add=True),
                ),
                (
                    "rating",
                    models.DecimalField(
                        decimal_places=1,
                        default=0,
                        max_digits=2,
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
                ("comments", models.TextField()),
                (
                    "lot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        to="webapp.parkinglot",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]