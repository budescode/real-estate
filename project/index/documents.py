# from elasticsearch_dsl.connections import connections
# # Create a connection to ElasticSearch
# connections.create_connection()
# from django_elasticsearch_dsl import DocType, Index
# from .models import Poster

# posters = Index('posters') 

# # reference elasticsearch doc for default settings here
# # poster.settings(
# #     number_of_shards=1,
# #     number_of_replicas=0
# # )

# @posters.doc_type
# class PosterDocument(DocType):

#     class Meta:
#         model = Poster
#         fields = ['unit', 'street_number', 'street_name', 'suburb', 'postcode', 'state', 'land_size', 'Price', 'Bedrooms', 'Bathrooms', 'Car_spaces']
        
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Poster


@registry.register_document
class PosterDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'poster'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Poster # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['unit', 'street_number', 'street_name', 'suburb', 'postcode', 'state', 'land_size', 'Price', 'Bedrooms', 'Bathrooms', 'Car_spaces']

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000