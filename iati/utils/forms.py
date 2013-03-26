# Django specific
from django import forms

# App specific
from utils.models import IATIXMLSource, UnhabitatRecordLog
from utils.models import UnHabitatParserLog
from data.models.common import Country, City, UnHabitatIndicatorCity, TypeDeprivationCountry
import pdb
import csv
from data.models.common import UnHabitatIndicatorCountry
import datetime
class IATIXMLSourceForm(forms.ModelForm):
    class Meta:
        model = IATIXMLSource


    
class SaveCsvData(object):
    #the uploaded csv file
    csv_file = None
    #the type of document that is being uploaded i.e. Table 3
    type_upload = None
    #the name of the document that is being uploaded
    file_name = None
    #the column names from the csv file
    keys = None
    #temp storage for countries
    countries = {}
    #three different type of documents supported:
    config_type_table = {}
    config_type_table['save_year_in_column_data'] = [1,2,3,4,7,8,9,10]
    config_type_table['save_year_in_row_data'] = []
    config_type_table['save_overall_data'] = [6]
    #temp object to store the uploaded file, and close when the document has been processed
    temp = None
    
    def __init__(self, csv_file, type_upload):
        #set the csv file
        self.set_csv_file(csv_file=csv_file)
        #let the object know what type of document is uploaded
        self.type_upload = type_upload
        
    def set_csv_file(self, csv_file):
        self.temp = open(csv_file.name, 'rU')
        self.file_name = csv_file.name
        try:
            dialect = csv.Sniffer().sniff(self.temp.read(1024), ",\t :;")
        except csv.Error:
            dialect = csv.excel
        #        dialect = csv.Sniffer().sniff(self.temp.read(1024))
        self.temp.seek(0)
        file = csv.DictReader(self.temp, dialect=dialect)
        keys = []
        for key in file.next().iterkeys():
            keys.append(key)
        #setting the keys (columns)
        self.keys = keys
        #setting the csv file
        self.csv_file = file

    def get_csv_file(self):
        #return the csv file
        return self.csv_file
        


    def save(self):
        #check if it contains an uploaded document
        if not self.get_csv_file():
            return "No CSV File "
        #check if it contains a certain type document
        if not self.type_upload:
            return "No idea what kind of document is being uploaded"
        #start the line loop, to walk through the csv document
        self.save_loop_based_on_country()
        #process has been finished, the document does not need to be red anymore
        self.temp.close()
        
        
            
    def save_loop_based_on_country(self):
        #loading the countries from database
        self.set_countries()
        #the country from a csv document
        country_str = None
        #total of lines processed
        total_processed = 0
        #total of countries that are not found
        total_errors = 0
        #the start date of this process
        date_created = datetime.datetime.today()
        #start logging of the parser
        logger = self.log_parser(date_created=date_created)
        #check every line in the csv document
        for line in self.get_csv_file():
            #getting the country string for the mapping
            try:
                country_str = line.get('Country')
                if not country_str:
                    country_str = line.get('Country Name')
                if not country_str:
                    country_str = line.get('COUNTRY')
                if country_str:
                    #get country from database based on the country string found
                    country =  self.find_country(country_name=country_str)
                else:
                    country = None
                    self.save_overall_data(country=country, line=line)

            except ValueError:
                self.save_overall_data(country=None, line=line)
                country = None
            #if a country has been found, we are able to process the data
            if country:
                #checking if the document contains years in the columns
                if self.type_upload in self.config_type_table['save_year_in_column_data']:
                    #save the data
                    self.save_year_in_column_data(country=country, line=line)
                #checking if the document belongs in the overall category
                elif self.type_upload in self.config_type_table['save_overall_data']:
                    #save the overall data
                    self.save_overall_data(country=country, line=line)
                else:
                    #if nothing has been found, it needs to process the csv document as year in rows
                    self.save_year_in_row_data(country=country, line=line)
            else:
                #log that the country is not been found
                self.log_detail_not_found(logger=logger, country_input=country_str, raw_data=line)
                total_errors += 1
            total_processed += 1
        self.log_parser(date_created=date_created, total_processed=total_processed, total_errors=total_errors)

    def set_countries(self):
        h_countries = {}
        countries = Country.objects.all()
        for country in countries:
            h_countries[country.get_iso_display()] = country.iso
        #set the countries from the database
        self.countries = h_countries

    def find_country(self, country_name):
        """
        Mapping the country string, to a country in the database
        @todo create a more optimized solution for this, it only matches an exact string, or the first 8 or last 8 characters
        @param country_name string from csv document:
        @return: country from database or False if it could not map a country
        """
        for str, iso in self.countries.items():
            if country_name.decode('utf8') in str or country_name.decode('utf8')[:8] in str or country_name.decode('utf8')[-8:] in str:
                try:
                    return Country.objects.get(iso=iso)
                except Country.DoesNotExist:
                    return None
                except KeyError:
                    pass
        return False

    def log_parser(self, date_created, total_errors=0, total_processed=0, message=None):
        log, _ = UnHabitatParserLog.objects.get_or_create(date_created=date_created, type_upload=self.type_upload)
        log.csv_file = self.file_name
        log.message = message
        log.total_errors = total_errors
        log.total_processed = total_processed
        log.save()
        return log

    def log_detail_not_found(self,logger, country_input=None, city_input=None, raw_data=None, year=None):
        if not country_input:
            country_input = 'no country found'
        log = UnhabitatRecordLog()
        log.city_input_name = city_input
        log.country_input_name = country_input
        log.raw_data = raw_data
        log.year = year
        log.parser = logger
        log.success = False
        log.save()
        
    def save_year_in_column_data(self, country, line):
        error = True
        for k in self.keys:
            value = line[k]

            if "country" in k.lower() or "city" in k.lower():
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

                    if self.type_upload == 1:

                        if not value:
                            pop.population = None
                        else:
                            pop.population = value
                    elif self.type_upload == 2:

                        if not value:
                            pop.urban_slum_population = None
                        else:
                            pop.urban_slum_population = value
                    elif self.type_upload == 3:

                        if not value:
                            pop.slum_proportion_living_urban = None
                        else:
                            pop.slum_proportion_living_urban = value
                    elif self.type_upload == 4:
                        if not value:
                            pop.under_five_mortality_rate = None
                        else:
                            pop.under_five_mortality_rate = value
                    elif self.type_upload == 29:
                        pop.urban_population = self.return_value_else_none(value)
                    #Table 1- city population of urban agglomerations with 750k inhabitants or more
                    elif self.type_upload == 7:
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
                    elif self.type_upload == 8:
                    #                                        pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=year)
                        if not value:
                            pop.year_plus_range = second_year
                            pop.avg_annual_rate_change_total_population = None
                        else:
                            pop.year_plus_range = second_year
                            pop.avg_annual_rate_change_total_population = value

                    #Table 3: Average annual rate of change of urban agglomerations with 750,000 inhabitants or more in 2007, by country, 1950-2025
                    elif self.type_upload == 9:
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
                    elif self.type_upload == 10:
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
    def save_year_in_row_data(self, country, line):
    #checking table Table 10: Improved water source and improved toilet (Country Level)
        if self.type_upload == 5:
            pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['Year'])


            pop.year = self.return_value_else_none(line['Year'])
            pop.improved_pit_latrine = self.return_value_else_none(line['Improved pit latrine'])
            pop.improved_spring_surface_water = self.return_value_else_none(line['Improved spring surface water'])
            pop.piped_water = self.return_value_else_none(line['Piped water'])
            pop.public_tap_pump_borehole = self.return_value_else_none(line['Public tap'])
            pop.improved_water = self.return_value_else_none(line['Improved water'])
            pop.composting_toilet = self.return_value_else_none(line['Composting toilet'])
            pop.protected_well = self.return_value_else_none(line['Protected well'])
            pop.pit_latrine_with_slab_or_covered_latrine = self.return_value_else_none(line['Pit latrine with slab or covered latrine'])
            pop.bottle_water = self.return_value_else_none(line['Bottle water'])
            pop.pump_borehole = self.return_value_else_none(line['pump/ borehole'])
            pop.rainwater = self.return_value_else_none(line['Rainwater'])
            pop.improved_toilet = self.return_value_else_none(line['Improved toilet'])
            pop.improved_flush_toilet = self.return_value_else_none(line['Flush toilet'])
            pop.pit_latrine_without_slab = self.return_value_else_none(line['pit latrine (without slab)'])

            pop.save()
            #Table 6: Population of Rural and urban areas and perc  entage urban, 2007
        if self.type_upload == 11:
            pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['Year'])


            pop.pop_urban_area = self.return_value_else_none(line['Urban'].replace(',',''))
            pop.pop_rural_area = self.return_value_else_none(line['Rural'].replace(',',''))
            pop.pop_urban_percentage = self.return_value_else_none(line['urban_percentage'], type="float")
            pop.population = self.return_value_else_none(line['Total'].replace(',',''))

            pop.save()
            #Table 11: Access to improved toilet,improved floor, sufficient living, connection to telephone, connection to electricity.
        if self.type_upload == 12:
            pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['Year'])


            pop.improved_floor = self.return_value_else_none(line['Improved floor'].replace(',',''), type="float")
            pop.sufficient_living = self.return_value_else_none(line['sufficient living'].replace(',',''), type="float")
            pop.has_telephone = self.return_value_else_none(line['Has Telephone'], type="float")
            pop.connection_to_electricity = self.return_value_else_none(line['Connection to electricity'].replace(',',''), type="float")

            pop.save()
            #Table 12: Improved Services (City Level)
        if self.type_upload == 13:
            city, _ = City.objects.get_or_create(name=line['City'], country=country)
            pop, _ = UnHabitatIndicatorCity.objects.get_or_create(city=city, year=line['Year'])


            pop.improved_water = self.return_value_else_none(line['Improved water'].replace(',',''), type="float")
            pop.improved_toilet =   self.return_value_else_none(line['Improved toilet'].replace(',',''), type="float")
            pop.improved_floor = self.return_value_else_none(line['Improved floor'].replace(',',''), type="float")
            pop.sufficient_living = self.return_value_else_none(line['sufficient living'].replace(',',''), type="float")
            pop.has_telephone = self.return_value_else_none(line['Has Telephone'], type="float")
            pop.connection_to_electricity = self.return_value_else_none(line['Connection to electricity'].replace(',',''), type="float")

            pop.save()
            #Table 13 matrix waste disposal by shelter deprivation
        if self.type_upload == 14:
            pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['year'])
            solid_waste_disposal_by_shelter_deprivation, _ = TypeDeprivationCountry.objects.get_or_create(indicator=pop,type_deprivation=1, is_matrix=True, extra_type_name=self.return_value_else_none(line['KIND OF SOIL WASTE DISPOSAL']))
            solid_waste_disposal_by_shelter_deprivation.urban = self.return_value_else_none(line['URBAN'])
            solid_waste_disposal_by_shelter_deprivation.non_slum_household= self.return_value_else_none(line['non slum household'])
            solid_waste_disposal_by_shelter_deprivation.slum_household= self.return_value_else_none(line['slum household'])
            solid_waste_disposal_by_shelter_deprivation.one_shelter_deprivation= self.return_value_else_none(line['one shelter deprivation'])
            solid_waste_disposal_by_shelter_deprivation.two_shelter_deprivations= self.return_value_else_none(line['two shelter deprivations'])
            solid_waste_disposal_by_shelter_deprivation.save()

        #Table 14: Percent distribution of type of cooking fuel by shelter deprivation
        if self.type_upload == 15:
            try:
                pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['YEAR'])
                cooking_fuel, _ = TypeDeprivationCountry.objects.get_or_create(indicator=pop, type_deprivation=2, is_matrix=True, extra_type_name=self.return_value_else_none(line['TYPE OF COOKING FUEL']))
                cooking_fuel.urban = self.return_value_else_none(line['Urban'])
                cooking_fuel.non_slum_household= self.return_value_else_none(line['non slum household'])
                cooking_fuel.slum_household= self.return_value_else_none(line['slum household'])
                cooking_fuel.one_shelter_deprivation= self.return_value_else_none(line['one shelter deprivation'])
                cooking_fuel.two_shelter_deprivations= self.return_value_else_none(line['two shelter deprivations'])
                cooking_fuel.save()
            except ValueError:
                pass

        #Table 15:
        if self.type_upload == 16:
            pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['Year'])
            cooking_fuel, _ = TypeDeprivationCountry.objects.get_or_create(indicator=pop, type_deprivation=3, gender=2, is_matrix=False)
            cooking_fuel.urban = self.return_value_else_none(line['total Urban'])
            cooking_fuel.rural = self.return_value_else_none(line['total Rural'])

            cooking_fuel.non_slum_household= self.return_value_else_none(line['Non-slum'])
            cooking_fuel.slum_household= self.return_value_else_none(line['all Slum'])

            cooking_fuel.one_shelter_deprivation = self.return_value_else_none(line['one sheltar deprivation'])
            cooking_fuel.two_shelter_deprivations= self.return_value_else_none(line['two shelter deprivations'])

            cooking_fuel.three_shelter_deprivations = self.return_value_else_none(line['three shelter deprivations'])


            cooking_fuel.save()
            #Table 16 male:
        if self.type_upload == 17:
            pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['Year'])
            cooking_fuel, _ = TypeDeprivationCountry.objects.get_or_create(indicator=pop, type_deprivation=4, gender=1, is_matrix=False)
            cooking_fuel.urban = self.return_value_else_none(line['Urban'])
            cooking_fuel.rural = self.return_value_else_none(line['Rural'])
            cooking_fuel.total = self.return_value_else_none(line['Total'])


            cooking_fuel.non_slum_household= self.return_value_else_none(line['non slum household'])
            cooking_fuel.slum_household= self.return_value_else_none(line['slum household'])

            cooking_fuel.one_shelter_deprivation = self.return_value_else_none(line['one shelter deprivation'])
            cooking_fuel.two_shelter_deprivations= self.return_value_else_none(line['two shelter deprivation'])

            cooking_fuel.three_shelter_deprivations = self.return_value_else_none(line['three shelter deprivation'])


            cooking_fuel.save()
            #Table 16 female:
        if self.type_upload == 26:
            pop, _ = UnHabitatIndicatorCountry.objects.get_or_create(country=country, year=line['Year'])
            cooking_fuel, _ = TypeDeprivationCountry.objects.get_or_create(indicator=pop, type_deprivation=4, gender=2, is_matrix=False)
            cooking_fuel.urban = self.return_value_else_none(line['Urban'], type="float")
            cooking_fuel.rural = self.return_value_else_none(line['Rural'], type="float")
            cooking_fuel.total = self.return_value_else_none(line['Total'], type="float")


            cooking_fuel.non_slum_household= self.return_value_else_none(line['non slum household'], type="float")
            cooking_fuel.slum_household= self.return_value_else_none(line['slum household'], type="float")

            cooking_fuel.one_shelter_deprivation = self.return_value_else_none(line['one shelter deprivation'], type="float")
            cooking_fuel.two_shelter_deprivations= self.return_value_else_none(line['two shelter deprivation'], type="float")

            cooking_fuel.three_shelter_deprivations = self.return_value_else_none(line['three shelter deprivation'], type="float")


            cooking_fuel.save()
            #Table 17
        if self.type_upload == 18:
            city, _ = City.objects.get_or_create(name=line['City'], country=country)
            pop, _ = UnHabitatIndicatorCity.objects.get_or_create(city=city, year=line['Year'])


            pop.enrollment_female_primary_education = self.return_value_else_none(line['Female'], type="float")
            pop.enrollment_male_primary_education =   self.return_value_else_none(line['Male'], type="float")
            pop.save()

        #Table 29
        if self.type_upload == 27:
            city, _ = City.objects.get_or_create(name=line['City'], country=country)
            pop, _ = UnHabitatIndicatorCity.objects.get_or_create(city=city, year=line['Year'])


            pop.diarrhea_last_two_weeks = self.return_value_else_none(line['diarrhea in last 2 weeks'], type="float")
            pop.diarrhea_had_ari =   self.return_value_else_none(line['ARI'], type="float")
            pop.fever_last_two_weeks =   self.return_value_else_none(line['in last 2 weeks'], type="float")

            pop.save()

        #Table 30
        if self.type_upload == 28:
            city, _ = City.objects.get_or_create(name=line['City'], country=country)
            pop, _ = UnHabitatIndicatorCity.objects.get_or_create(city=city, year=line['Year'])


            pop.perc_malnourished = self.return_value_else_none(line['Malnutrition'], type="float")
            pop.perc_measles =   self.return_value_else_none(line['Measles'], type="float")
            pop.save()

        if self.type_upload == 31:
            try:
                city, _ = City.objects.get_or_create(name=line['City'], country=country)
                pop, _ = UnHabitatIndicatorCity.objects.get_or_create(city=city, year=line['Year'])
                pop.cpi_5_dimensions =self.return_value_else_none(line['five'], type="float")
                pop.cpi_4_dimensions =self.return_value_else_none(line['four'], type="float")
                pop.cpi_productivity_index =self.return_value_else_none(line['Productivity Index'], type="float")
                pop.cpi_quality_of_live_index =self.return_value_else_none(line['Quality of life Index'], type="float")
                pop.cpi_infrastructure_index =self.return_value_else_none(line['Infrastructure Index'], type="float")
                pop.cpi_environment_index = self.return_value_else_none(line['Enivronment Index'], type="float")
                pop.cpi_equity_index = self.return_value_else_none(line['Equity Index'], type="float")
                pop.save()
            except ValueError:
                pass

    def save_overall_data(self, country, line):
        if self.type_upload == 6:
            #add region info to country
            try:
                country, _ = Country.objects.get_or_create(iso=line['iso2'])
                country.country_name = line['country_name']
                country.dac_country_code = line['dac_country_code']
                country.dac_region_code = line['dac_region_code']
                country.dac_region_name = line['dac_region_name']
                country.iso2 = line['iso2']
                country.iso3 = line['iso3']
                country.save()
            except Country.DoesNotExist:
                pass
        if self.type_upload == 32:
            #will change odd (unusual city names to "normal" city names)
            usable_name = line['Usable name']
            unusable_name = line['Unusable name']
            cities = City.objects.filter(name=unusable_name)
            for city in cities:
                city.name = usable_name
                city.save()




    def return_value_else_none(self, value, type=""):
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
        #use the saving object
        saver = SaveCsvData(csv_file=self.cleaned_data['csv_file'], type_upload=self.cleaned_data['type_upload'])
        saver.save()


