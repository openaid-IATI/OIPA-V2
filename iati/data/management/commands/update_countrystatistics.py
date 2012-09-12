# Django specific
from django.core.management.base import BaseCommand

# App specific
from data.models.activity import IATIActivity
from data.models.common import Country
from data.models.statistics import CountryStatistics


def calculate_statistics(country):
    statistics = CountryStatistics.objects.get_or_create(
        country=country
    )[0]
    statistics.total_activities = IATIActivity.objects.filter(iatiactivitycountry__country__iso__in=[country.iso]).count()
    statistics.save()

class Command(BaseCommand):
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        [calculate_statistics(country) for country in Country.objects.all()]