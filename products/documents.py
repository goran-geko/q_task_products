from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from products.models import Product, Rating


@registry.register_document
class ProductDocument(Document):
    rating_set = fields.ObjectField(properties={
        'rating': fields.FloatField(),
        'user': fields.ObjectField(properties={
            'username': fields.TextField(),
            'email': fields.TextField(),
        })
    })

    class Index:
        name = 'products'

    class Django:
        model = Product
        fields = [
            'name',
            'price',
            'updated_at',
            'rating',
        ]
        related_models = [Rating, User]

    def get_queryset(self):
        return super(ProductDocument, self).get_queryset().prefetch_related(
            'rating_set'
        ).all()

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Rating):
            return related_instance.product
        if isinstance(related_instance, User):
            return related_instance.products.all()
