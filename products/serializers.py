from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductSerializer(ModelSerializer):
    ratings = SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'rating', 'updated_at', 'ratings')
        read_only_fields = ['id', 'ratings']

    @staticmethod
    def get_ratings(instance: Product):
        return [rating.rating for rating in instance.rating_set.all()]
