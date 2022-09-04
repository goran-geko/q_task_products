from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProductConfig(AppConfig):
    name = 'products'
    verbose_name = _('products')

    def ready(self):
        """
        Registering signals (`pre_save`, `post_save`, ...) so that we can use `@receiver` decorator
        """
        import products.signals  # noqa
