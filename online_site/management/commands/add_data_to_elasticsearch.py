from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry
from ...models import Profile, ContestResult

class Command(BaseCommand):
    help = 'Index all profiles and contest results in Elasticsearch'

    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            profile_document = registry.get_documents(Profile).from_instance(profile)
            profile_document.save()

        for contest_result in ContestResult.objects.all():
            contest_result_document = registry.get_documents(ContestResult).from_instance(contest_result)
            contest_result_document.save()