from django.db.models.signals import pre_save
from django.dispatch import receiver

from products.models import Product


@receiver(pre_save, sender=Product)
def pre_save(sender, instance=None, **kwargs):
    # This `if` statement makes sure that we override `instance.rating` only when `Product` is created
    if not instance.pk:
        # Overriding `instance.rating` as field will be calculated when every rating is added
        instance.rating = 0.0
