from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ProductAbstract(models.Model):
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    class Meta:
        abstract = True


class Product(ProductAbstract):
    name = models.CharField(max_length=256, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    # TODO: Rename `ratings` filed to `users` as this makes more sense :)
    ratings = models.ManyToManyField(User, through='Rating')


class Rating(ProductAbstract):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_set')
