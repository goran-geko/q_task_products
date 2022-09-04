from django.db.models import Avg

from products.celery import app
from products.models import Product, Rating


@app.task(name='calculate_average_rating')
def calculate_average_rating(product_id):
    """
    Method that will calculate and store average rating per `Product`
    """
    product = Product.objects.get(pk=product_id)
    rating = Rating.objects.filter(product=product).aggregate(Avg('rating')).get('rating__avg')
    product.rating = rating
    product.save()
