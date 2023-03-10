# Generated by Django 4.1.5 on 2023-01-31 20:44

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from api.vending_machine.validators import validate_multiple_of


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VendingMachineUser",
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
                    "deposit",
                    models.PositiveIntegerField(
                        default=0,
                        help_text=(
                            "The amount of money the user has deposited in"
                            " cents."
                        ),
                        verbose_name="Deposit",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("buyer", "Buyer"), ("seller", "Seller")],
                        default="buyer",
                        help_text=(
                            "The role of the user in the vending machine"
                            " system."
                        ),
                        max_length=20,
                        verbose_name="Role",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                    "name",
                    models.CharField(
                        help_text="Name of the product, cannot be blank.",
                        max_length=80,
                        unique=True,
                        verbose_name="Product Name",
                    ),
                ),
                (
                    "price",
                    models.PositiveIntegerField(
                        help_text=(
                            "Price of the product in cents, must be multiple"
                            " of 5."
                        ),
                        validators=[
                            django.core.validators.MinValueValidator(5),
                            validate_multiple_of(5),
                        ],
                        verbose_name="Price",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Number of available products in the stock.",
                        verbose_name="Available Stock",
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="vending_machine.vendingmachineuser",
                    ),
                ),
            ],
        ),
    ]
