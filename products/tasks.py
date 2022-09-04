from django.db.models import Avg

from products.models import Product, Rating


def calculate_average_rating(product_id):
    """
    Not used currently. It is here to show how we could utilize celery to run async task
    and improve overall app performance.
    """
    product = Product.objects.get(pk=product_id)
    rating = Rating.objects.filter(product=product).aggregate(Avg('rating')).get('rating__avg')
    product.rating = rating
    product.save()
