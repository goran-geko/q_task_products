from django.db.models import Avg
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from products.models import Product, Rating


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
    product = instance.product
    rating = Rating.objects.filter(product=product).aggregate(Avg('rating')).get('rating__avg')
    product.rating = rating
    product.save()

    """
    Better approach to this would be to calculate this average as async celery task:
    
    from products.tasks import calculate_average_rating
    calculate_average_rating.delay(product_id=instance.product.pk)
    
    I will leave it as is for now but we would need to add celery as dependency and configure 2 new containers.
    One for celery (worker) and one with redis instance (or any other queue management tool).
    """
