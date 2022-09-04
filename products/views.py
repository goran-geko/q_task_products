from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from products.documents import ProductDocument
from products.models import Product, Rating
from products.serializers import ProductSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'name', 'price', 'updated_at', 'users']
    """
    As field `users` is `ManyToManyField` relation, filter will look if value exists in list of related pk's.
    We could enable searching by other field by creating custom `filterset_class` class. This also goes for field
    `rating_set` which is one to many relation from `Product` to `Rating` aggregation
    """

    def get_queryset(self):
        if self.request.GET.get('source') == 'es':
            """
            Really basic example just to show fetching from elasticsearch. to_queryset() will make a hit to DB (by IDs)
            and after that filters are applied. Not the best case as we can use elasticsearch to filter results as well.
            Implementation of elasticsearch would differ based on project specifications.
            """
            return ProductDocument.search().to_queryset()
        return Product.objects.all()


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class ProductCreateAPIView(CreateAPIView):

    def post(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
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
