from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductSerializer(ModelSerializer):
    """
    Serializer for `Product` model.
    Can't be used to update `rating_set` (`Rating` model).
    """
    rating_set = SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'rating', 'updated_at', 'rating_set')
        read_only_fields = ['id', 'rating_set']

    @staticmethod
    def get_rating_set(instance: Product):
        return [rating.rating for rating in instance.rating_set.all()]
