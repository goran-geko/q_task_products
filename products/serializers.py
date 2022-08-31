from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'rating', 'updated_at', 'ratings')
        read_only_fields = ['ratings']
