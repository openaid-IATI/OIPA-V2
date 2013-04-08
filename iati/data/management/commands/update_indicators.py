# Django specific
from django.core.management.base import BaseCommand
from data.models import Country
from data.models.common import UnHabitatIndicatorCountry, IndicatorData, Indicator
from data.models.constants import COUNTRY_LOCATION


class Command(BaseCommand):
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        for country in Country.objects.all():
            if not country.latitude:
                try:
                    country.latitude = COUNTRY_LOCATION[country.iso]['latitude']
                    country.longitude = COUNTRY_LOCATION[country.iso]['longitude']
                    country.save()
                except KeyError:
                    pass
            unhabitat_indicators = UnHabitatIndicatorCountry.objects.filter(country=country)
            for i in unhabitat_indicators:
                indicator, _ = Indicator.objects.get_or_create(name='population')
                id, _ =IndicatorData.objects.get_or_create(indicator=indicator, country=country, value=i.population, year=i.year)
