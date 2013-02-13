# Django specific
from django import forms

# App specific
from utils.models import IATIXMLSource
from utils.models import UnHabitatParserLog
from data.models.common import Country, City, UnHabitatIndicatorCity, Solid_waste_disposal_by_shelter_deprivation, DistributionCookingFuelByShelterDepr
import pdb
import csv
from data.models.common import UnHabitatIndicatorCountry

class IATIXMLSourceForm(forms.ModelForm):
    class Meta:
        model = IATIXMLSource

def return_value_else_none(value, type=""):
    if type == "float":
        try:
            float(value)
            return value
        except ValueError:
            return 0
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
                country_str = line.get('Country')
                if not country_str:
                    country_str = line.get('Country Name')
                if not country_str:
                    country_str = line.get('COUNTRY')
                country =  Country.find_iso_country(country_name=country_str)
                if country:
                    if type_upload == 1 or type_upload == 2 or type_upload == 3 or type_upload == 4 or type_upload == 7 or type_upload == 8 or type_upload == 9 or type_upload == 10:
                        for k in keys:
                            value = line[k]

                            if "Country" in k or "City" in k:
                                pass
                            else:
                                try:
                                    year = int(k[:4])
                                    second_year = int(k[5:])
                                    k = year
                                except:
                                    year = k
                                    second_year = None
                                    #@TODO fix logging
                                    pass
                                if year:
                                    pop, created = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=k)

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
                                    #Table 1- city population of urban agglomerations with 750k inhabitants or more
                                    elif type_upload == 7:
                                        try:
                                            city, _ = City.objects.get_or_create(name=line['City'], country=country)
                                            indicator, _ = UnHabitatIndicatorCity.objects.get_or_create(city=city, year=k)
                                            if not value:
                                                indicator.pop_urban_agglomerations = None
                                            else:
                                                indicator.pop_urban_agglomerations = value
                                            indicator.save()
                                        except:
                                            #@TODO fix error processing and logging
                                            pass
                                    #Table 2: Average annual rate of change of the Total Population by major area, Region and Country, 1950-2050 (%)
                                    elif type_upload == 8:
#                                        pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=year)
                                        if not value:
                                            pop.year_plus_range = second_year
                                            pop.avg_annual_rate_change_total_population = None
                                        else:
                                            pop.year_plus_range = second_year
                                            pop.avg_annual_rate_change_total_population = value

                                    #Table 3: Average annual rate of change of urban agglomerations with 750,000 inhabitants or more in 2007, by country, 1950-2025
                                    elif type_upload == 9:
                                        try:
                                            city, _ = City.objects.get_or_create(name=line['City'], country=country)

                                            indicator, _ = UnHabitatIndicatorCity.objects.get_or_create(city=city, year=year)
                                            if not value:
                                                indicator.year_plus_range = second_year
                                                indicator.avg_annual_rate_change_urban_agglomerations = None
                                            else:
                                                indicator.year_plus_range = second_year
                                                try:
                                                    float(value)
                                                except:
                                                    value = 0
                                                indicator.avg_annual_rate_change_urban_agglomerations = value
                                            indicator.save()
                                        except:
                                            #@todo fix logging
                                            pass
                                    #Table 5: Average annual rate of change of urban agglomerations with 750,000 inhabitants or more in 2007, by country, 1950-2025
                                    elif type_upload == 10:
                                        if not value:
                                            pop.year_plus_range = second_year
                                            pop.avg_annual_rate_change_percentage_urban = None
                                        else:
                                            pop.year_plus_range = second_year
                                            pop.avg_annual_rate_change_percentage_urban = value

                                    try:
                                        pop.save()
                                    except ValueError:
                                        pass

                    #checking table Table 10: Improved water source and improved toilet (Country Level)
                    if type_upload == 5:
                        pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['Year'])


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
                    #Table 6: Population of Rural and urban areas and perc  entage urban, 2007
                    if type_upload == 11:
                        pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['Year'])


                        pop.pop_urban_area = return_value_else_none(line['Urban'].replace(',',''))
                        pop.pop_rural_area = return_value_else_none(line['Rural'].replace(',',''))
                        pop.pop_urban_percentage = return_value_else_none(line['urban_percentage'], type="float")
                        pop.population = return_value_else_none(line['Total'].replace(',',''))

                        pop.save()
                    #Table 11: Access to improved toilet,improved floor, sufficient living, connection to telephone, connection to electricity.
                    if type_upload == 12:
                        pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=2007)


                        pop.improved_floor = return_value_else_none(line['Improved floor'].replace(',',''), type="float")
                        pop.sufficient_living = return_value_else_none(line['sufficient living'].replace(',',''), type="float")
                        pop.has_telephone = return_value_else_none(line['Has Telephone'], type="float")
                        pop.connection_to_electricity = return_value_else_none(line['Connection to electricity'].replace(',',''), type="float")

                        pop.save()
                    #Table 12: Improved Services (City Level)
                    if type_upload == 13:
                        city, _ = City.objects.get_or_create(name=line['City'], country=country)
                        pop, _ = UnHabitatIndicatorCity.objects.get_or_create(city=city, year=line['Year'])


                        pop.improved_water = return_value_else_none(line['Improved water'].replace(',',''), type="float")
                        pop.improved_toilet =   return_value_else_none(line['Improved toilet'].replace(',',''), type="float")
                        pop.improved_floor = return_value_else_none(line['Improved floor'].replace(',',''), type="float")
                        pop.sufficient_living = return_value_else_none(line['sufficient living'].replace(',',''), type="float")
                        pop.has_telephone = return_value_else_none(line['Has Telephone'], type="float")
                        pop.connection_to_electricity = return_value_else_none(line['Connection to electricity'].replace(',',''), type="float")

                        pop.save()
                    #Table 13 matrix waste disposal by shelter deprivation
                    if type_upload == 14:
                        pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['year'])
                        solid_waste_disposal_by_shelter_deprivation, _ = Solid_waste_disposal_by_shelter_deprivation.objects.get_or_create(unhabitat_indicator_country=pop, kind_of_soil_waste_disposal=return_value_else_none(line['KIND OF SOIL WASTE DISPOSAL']))
                        solid_waste_disposal_by_shelter_deprivation.urban = return_value_else_none(line['URBAN'])
                        solid_waste_disposal_by_shelter_deprivation.non_slum_household= return_value_else_none(line['non slum household'])
                        solid_waste_disposal_by_shelter_deprivation.slum_household= return_value_else_none(line['slum household'])
                        solid_waste_disposal_by_shelter_deprivation.one_shelter_deprivation= return_value_else_none(line['one shelter deprivation'])
                        solid_waste_disposal_by_shelter_deprivation.two_shelter_deprivations= return_value_else_none(line['two shelter deprivations'])
                        solid_waste_disposal_by_shelter_deprivation.save()

                    #Table 14: Percent distribution of type of cooking fuel by shelter deprivation
                    if type_upload == 15:
                        try:
                            pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['YEAR'])
                            cooking_fuel, _ = DistributionCookingFuelByShelterDepr.objects.get_or_create(unhabitat_indicator_country=pop, type_of_cooking_fuel=return_value_else_none(line['TYPE OF COOKING FUEL']))
                            cooking_fuel.urban = return_value_else_none(line['Urban'])
                            cooking_fuel.non_slum_household= return_value_else_none(line['non slum household'])
                            cooking_fuel.slum_household= return_value_else_none(line['slum household'])
                            cooking_fuel.one_shelter_deprivation= return_value_else_none(line['one shelter deprivation'])
                            cooking_fuel.two_shelter_deprivations= return_value_else_none(line['two shelter deprivations'])
                            cooking_fuel.save()
                        except ValueError:
                            pass





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