from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from products.models import Product, Rating
from products.tasks import calculate_average_rating


@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance=None, **kwargs):
    """
    Will be triggered just before SQL is executed to create a Product
    """
    # This `if` statement makes sure that we override `instance.rating` only when `Product` is created
    if not instance.pk:
        # Overriding `instance.rating` as field will be calculated when every rating is added
        instance.rating = 0.0


@receiver(post_save, sender=Rating)
def rating_post_save(sender, instance=None, created=None, **kwargs):
    """
    Will be triggered just after SQL is executed to create a Rating
    """
    if settings.IS_TEST:
        # If we are running tests, method will be executed in same thread (synchronous).
        calculate_average_rating(product_id=instance.product.pk)
    else:
        # In real environment, it will be sent to broker so that can be picked up by worker.
        calculate_average_rating.delay(product_id=instance.product.pk)
