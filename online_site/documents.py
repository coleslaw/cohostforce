from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Profile, ContestResult


@registry.register_document
class ProfileDocument(Document):
    name = fields.TextField()
    rating = fields.IntegerField()
    max_rating = fields.IntegerField()
    title = fields.TextField()
    best_title = fields.TextField()

    def __str__(self):
        return self.name

    class Index:
        name = 'profiles'

    class Django:
        model = Profile


@registry.register_document
class ContestResultDocument(Document):
    name = fields.TextField()
    rating_change = fields.IntegerField()
    new_rating = fields.IntegerField()
    title_change = fields.TextField()
    user = fields.ObjectField(properties={
        'name': fields.TextField(),
        'rating': fields.IntegerField(),
        'max_rating': fields.IntegerField(),
        'title': fields.TextField(),
        'best_title': fields.TextField()
    })

    def __str__(self):
        return self.name

    class Index:
        name = 'contest_results'

    class Django:
        model = ContestResult
