# Django specific
from django.core.management.base import BaseCommand
from data.models import Country
from data.models.common import UnHabitatIndicatorCountry, IndicatorCityData, Indicator, City, UnHabitatIndicatorCity
from data.models.constants import CITY_LOCATIONS


class Command(BaseCommand):
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        for city in City.objects.all():
            for location in CITY_LOCATIONS['features']:
                if location['properties']['nameascii'] == city.name or location['properties']['namealt'] == city.name or location['properties']['namepar'] == city.name or location['properties']['name'] == city.name:
                    if city.country.iso2 == location['properties']['iso_a2']:
                        city.longitude = location['properties']['longitude']
                        city.latitude = location['properties']['latitude']
                        city.save()
                        print '%s has been updated' % location['properties']['nameascii']



# for (var i = 0;i < city_database.length;i++){
#
#	for(var y = 0;y < city_locations.features.length; y++){
#
#		if(city_database[i].Name == city_locations.features[y].properties.nameascii || city_database[i].Name == city_locations.features[y].properties.namealt || city_database[i].Name == city_locations.features[y].properties.name){
#
#			if(city_database[i].iso2 == city_locations.features[y].properties.iso_a2){
#				counter++;
#
#				sqltext += "update data_city set latitude='"+ city_locations.features[y].properties.longitude +"', longitude='" +city_locations.features[y].properties.latitude+"' where id = "+city_database[i].id+";";
#
#			}
#		}
#	}
#}
               


