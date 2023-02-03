from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_multiple_of


class VendingMachineUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deposit = models.PositiveIntegerField(
        verbose_name=_("Deposit"),
        default=0,
        help_text=_("The amount of money the user has deposited in cents."),
    )
    ROLE_CHOICES = [
        ("buyer", _("Buyer")),
        ("seller", _("Seller")),
    ]
    role = models.CharField(
        verbose_name=_("Role"),
        max_length=20,
        choices=ROLE_CHOICES,
        default="buyer",
        help_text=_("The role of the user in the vending machine system."),
    )

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class Product(models.Model):
    seller = models.ForeignKey(
        VendingMachineUser, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(
        verbose_name=_("Product Name"),
        max_length=80,
        unique=True,
        blank=False,
        null=False,
        help_text=_("Name of the product, cannot be blank."),
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Price"),
        validators=[MinValueValidator(5), validate_multiple_of(5)],
        help_text=_("Price of the product in cents, must be multiple of 5."),
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Available Stock"),
        default=0,
        help_text=_("Number of available products in the stock."),
    )
