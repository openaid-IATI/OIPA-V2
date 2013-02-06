# Django specific
from django import forms

# App specific
from utils.models import IATIXMLSource
from utils.models import UnHabitatParserLog
from data.models.common import Country
import pdb
import csv
from data.models.common import Population

class IATIXMLSourceForm(forms.ModelForm):
    class Meta:
        model = IATIXMLSource

def return_value_else_none(value):
    if value:
        return value
    else:
        return None
class UploadForm(forms.ModelForm):
    class Meta:
        model = UnHabitatParserLog
        fields = ('csv_file', 'type_upload',)


    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.content_type == 'text/csv': return forms.ValidationError('Upload a correct CSV file')

    #        pdb.set_trace()
        temp = open(csv_file.name, 'w')
        temp.writelines(csv_file.read())
        temp.close()
        return csv_file



    def save(self):
        temp = open(self.cleaned_data['csv_file'].name, 'rU')
        type_upload = self.cleaned_data['type_upload']
        print type_upload
        #        csv_file = open(temp, 'rU')
        try:
            dialect = csv.Sniffer().sniff(temp.read(1024), ",\t :;")
        except csv.Error:
            dialect = csv.excel
#        dialect = csv.Sniffer().sniff(temp.read(1024))
        temp.seek(0)
        file = csv.DictReader(temp, dialect=dialect)
        keys = []
        for key in file.next().iterkeys():
            keys.append(key)
        country = False
#        pdb.set_trace()
        for line in file:
            try:
                country =  Country.find_iso_country(country_name=line['Country'])
                if country:
                    if type_upload == 1 or type_upload == 2 or type_upload == 3 or type_upload == 4:
                        for k in keys:
                            value = line[k]

                            if k == "Country":
                                pass
                            else:
                                pop, created = Population.objects.get_or_create(country=country, year=k)

                                if type_upload == 1:

                                    if not value:
                                        pop.population = None
                                    else:
                                        pop.population = value
                                elif type_upload == 2:

                                    if not value:
                                        pop.urban_slum_population = None
                                    else:
                                        pop.urban_slum_population = value
                                elif type_upload == 3:

                                    if not value:
                                        pop.slum_proportion_living_urban = None
                                    else:
                                        pop.slum_proportion_living_urban = value
                                elif type_upload == 4:
                                    if not value:
                                        pop.under_five_mortality_rate = None
                                    else:
                                        pop.under_five_mortality_rate = value
                                try:
                                    pop.save()
                                except ValueError:
                                    pass

                    #checking table Table 10: Improved water source and improved toilet (Country Level)
                    if type_upload == 5:
                        pop, created = Population.objects.get_or_create(country=country, year=line['Year'])


                        pop.year = return_value_else_none(line['Year'])
                        pop.improved_pit_latrine = return_value_else_none(line['Improved pit latrine'])
                        pop.improved_spring_surface_water = return_value_else_none(line['Improved spring surface water'])
                        pop.piped_water = return_value_else_none(line['Piped water'])
                        pop.public_tap_pump_borehole = return_value_else_none(line['Public tap'])
                        pop.improved_water = return_value_else_none(line['Improved water'])
                        pop.composting_toilet = return_value_else_none(line['Composting toilet'])
                        pop.protected_well = return_value_else_none(line['Protected well'])
                        pop.pit_latrine_with_slab_or_covered_latrine = return_value_else_none(line['Pit latrine with slab or covered latrine'])
                        pop.bottle_water = return_value_else_none(line['Bottle water'])
                        pop.pump_borehole = return_value_else_none(line['pump/ borehole'])
                        pop.rainwater = return_value_else_none(line['Rainwater'])
                        pop.improved_toilet = return_value_else_none(line['Improved toilet'])
                        pop.improved_flush_toilet = return_value_else_none(line['Flush toilet'])
                        pop.pit_latrine_without_slab = return_value_else_none(line['pit latrine (without slab)'])

                        pop.save()
            #we are sure now that we are not handling Unhabitat indicators
            except KeyError:
                if type_upload == 6:
                    #add region info to country
                    try:
                        country = Country.objects.get(iso=line['iso2'])
                        country.country_name = line['country_name']
                        country.dac_country_code = line['dac_country_code']
                        country.dac_region_code = line['dac_region_code']
                        country.dac_region_name = line['dac_region_name']
                        country.iso2 = line['iso2']
                        country.iso3 = line['iso3']
                        country.save()
                    except Country.DoesNotExist:
                        pass







                    #                            pop.save()
#                    country = False

        temp.close()