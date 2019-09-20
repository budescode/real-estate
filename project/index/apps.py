from django.apps import AppConfig
import elasticsearch_dsl.connections
from django.conf import settings


class IndexConfig(AppConfig):
    name = 'index'

    def ready(self):
        elasticsearch_dsl.connections.connections.create_connection(timeout=40)
        # elasticsearch_dsl.connections.connections.create_connection(timeout=20)
        # import shop.signals