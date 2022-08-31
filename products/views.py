from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from products.models import Product
from products.serializers import ProductSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()