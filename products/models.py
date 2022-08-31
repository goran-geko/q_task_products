from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    updated_at = models.DateTimeField(null=True, auto_now=True)
    ratings = models.ManyToManyField(User)
