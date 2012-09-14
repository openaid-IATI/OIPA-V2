# Django specific
from django.core.management.base import BaseCommand

# App specific
from django.db.models.aggregates import Count
from data.models.organisation import Organisation
from data.models.statistics import OrganisationStatistics


def calculate_statistics(organisation):
    statistics = OrganisationStatistics.objects.get_or_create(
        organisation=organisation
    )[0]
    statistics.total_activities = organisation.iatiactivity_set.count()
    statistics.save()

class Command(BaseCommand):
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        [calculate_statistics(organisation) for organisation in Organisation.objects.annotate(activity_count=Count('iatiactivity')).filter(activity_count__gte=1)]