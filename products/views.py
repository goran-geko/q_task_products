from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from products.models import Product, Rating
from products.serializers import ProductSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class ProductCreateAPIView(CreateAPIView):

    def post(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist as e:
            raise Exception('Product does not exist')
        user = request.auth.user
        rating = request.data.get('rating', None)
        if not rating:
            raise Exception('Rating is not set')
        if Rating.objects.filter(product=product, user=user).exists():
            # We could update rating here if we want to support that feature
            raise Exception('This user already voted')
        else:
            Rating.objects.create(product=product, user=user, rating=rating)
        return Response(status=HTTP_200_OK)
