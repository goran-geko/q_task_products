from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from products.documents import ProductDocument
from products.models import Product, Rating
from products.serializers import ProductSerializer, RatingSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    """
    API View that provides user an option to:
    1. list products using `get` method
    2. create product using `post` method
    """
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'name', 'price', 'updated_at', 'users']
    """
    As field `users` is `ManyToManyField` relation, filter will look if value exists in list of related pk's.
    We could enable searching by other field by creating custom `filterset_class` class. This also goes for field
    `rating_set` which is one to many relation from `Product` to `Rating` aggregation
    """

    def get_queryset(self):
        """
        Will fetch data from DB or from elasticsearch depending on `source` param:
        1. `source=db` - fetching from DB
        2. `source=es` - fetching from elasticsearch
        """
        if self.request.GET.get('source') == 'es':
            """
            Really basic example just to show fetching from elasticsearch. to_queryset() will make a hit to DB (by IDs)
            and after that filters are applied. Not the best case as we can use elasticsearch to filter results as well.
            Implementation of elasticsearch would differ based on project specifications.
            """
            return ProductDocument.search().to_queryset()
        return Product.objects.all()


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API View that provides user an option to:
    1. retrieve product using `get` method
    2. update product using `put` and `patch` methods
    3. destroy product using `destroy` method
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class RatingCreateAPIView(CreateAPIView):
    """
    API View that provides user an option to rate an product using `post` method
    """
    serializer_class = RatingSerializer

    def post(self, request, pk, *args, **kwargs):
        # Fetching product, raise exception if not found
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Exception('Product does not exist')
        # Fetching currently logged user
        user = request.auth.user
        # Fetching `rating` from request, raise exception if not provided
        rating = request.data.get('rating', None)
        if not rating:
            raise Exception('Rating is not set')
        # Disable option to rate a product for a user if user already rated that product
        if Rating.objects.filter(product=product, user=user).exists():
            # We could update rating here if we want to support that feature
            raise Exception('This user already voted')
        else:
            # Rate product, will emit `post_save` signal that is handled in `rating_post_save` method
            Rating.objects.create(product=product, user=user, rating=rating)
        return Response(status=HTTP_200_OK)
