from django.db.models import Avg
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from products.models import Product, Rating


@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance=None, **kwargs):
    # This `if` statement makes sure that we override `instance.rating` only when `Product` is created
    if not instance.pk:
        # Overriding `instance.rating` as field will be calculated when every rating is added
        instance.rating = 0.0


@receiver(post_save, sender=Rating)
def rating_post_save(sender, instance=None, created=None, **kwargs):
    product = instance.product
    rating = Rating.objects.filter(product=product).aggregate(Avg('rating')).get('rating__avg')
    product.rating = rating
    product.save()
