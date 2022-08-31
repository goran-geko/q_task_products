from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProductConfig(AppConfig):
    name = 'products'
    verbose_name = _('products')

    def ready(self):
        import products.signals  # noqa
