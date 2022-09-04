from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ProductAbstract(models.Model):
    """
    Inherits `models.Model` and will be inherited by `Product` and `Rating` models as both will have `rating` field
    """
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    class Meta:
        abstract = True


class Product(ProductAbstract):
    """
    Main model in this app. Stores product records in DB.
    """
    name = models.CharField(max_length=256, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    users = models.ManyToManyField(User, through='Rating', related_name='products')


class Rating(ProductAbstract):
    """
    Model that will be used as aggregation between `Product` and `User` models. We need to store custom field `rating`
    into it so that is why we cannot use standard `ManyToManyField` relation without `through` argument.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_set')
