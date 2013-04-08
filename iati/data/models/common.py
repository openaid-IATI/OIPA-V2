# Django specific
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App specific
from data.models.constants import BUDGET_TYPE_CHOICES
from data.models.constants import COUNTRIES_TUPLE
from data.models.constants import DISBURSEMENT_CHANNEL_CHOICES
from data.models.constants import FLOW_TYPE_CHOICES
from data.models.constants import POLICY_SIGNIFICANCE_CHOICES
from data.models.constants import REGION_CHOICES
from data.models.constants import STATUS_CHOICES
from data.models.constants import TIED_AID_STATUS_CHOICES
from data.models.constants import TRANSACTION_TYPE_CHOICES
from data.models.constants import VOCABULARY_CHOICES
from data.models.organisation import Organisation


class Language(models.Model):
    code = models.CharField(max_length=55)

    class Meta:
        app_label = "data"


class Country(models.Model):
    iso = models.CharField(max_length=2, primary_key=True, choices=COUNTRIES_TUPLE)
    dac_region_code = models.IntegerField(null=True, blank=True)
    dac_region_name = models.CharField(max_length=100, null=True, blank=True)
    country_name = models.CharField(max_length=100, null=True, blank=True)
    dac_country_code = models.IntegerField(null=True, blank=True)
    iso2 = models.CharField(max_length=5, null=True, blank=True)
    iso3 = models.CharField(max_length=5, null=True, blank=True)
    latitude = models.FloatField(max_length=20, null=True, blank=True)
    longitude = models.FloatField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.iso, self.get_iso_display())

    @staticmethod
    def find_iso_country(country_name):
        countries = Country.objects.all()
        try:
            for country in countries:
                if country_name.decode('utf8') in country.get_iso_display() or country_name.decode('utf8')[:8] in country.get_iso_display() or country_name.decode('utf8')[-8:] in country.get_iso_display():
                    return country
        except:
            return False
        return False
    class Meta:
        app_label = "data"
        verbose_name = _("country")
        verbose_name_plural = _("countries")

class Indicator(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = "data"


class IndicatorData(models.Model):
    indicator = models.ForeignKey(Indicator)
    country = models.ForeignKey(Country)
    value = models.FloatField(null=True, blank=True)
    year = models.IntegerField(max_length=5)

    class Meta:
        app_label = "data"


class City(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    country = models.ForeignKey(Country)


    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "data"
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

types_deprivation = (
    (1, _('Table 13 matrix waste disposal by shelter deprivation')),
    (2, _('Table 14: Percent distribution of type of cooking fuel by shelter deprivation')),
    (3, _('Table 15: Education; Literacy Rates by Shelter Deprivation (Woman)')),
    (4, _('Table 16: Enrolmen in primary education in urban and rural areas (female and male)')),
    (6, _('Table 18: Percentage of female and male aged 15-24 years unemployed by shelter depriviation')),
    (7, _('Table 19: Percentage of female and male aged 15-24 years in informal employment by shelter depriviation')),
    (8, _('Table 26: Percentage of children  with Diarhea')),
    (9, _('Table 27: Percentage of women who were attended to during delivery by skilled personnel')),
    (10, _('Table 28: Percentage of Malnourished children and Percentage of children immunised against Measles')),
)
class TypeDeprivation(models.Model):
    urban = models.FloatField(blank=True, null=True, verbose_name=_('urban'))
    total = models.FloatField(blank=True, null=True, verbose_name=_('total'))

    rural = models.FloatField(blank=True, null=True, verbose_name=_('rural'))


    non_slum_household = models.FloatField(blank=True, null=True, verbose_name=_('non slum household'))
    slum_household = models.FloatField(blank=True, null=True, verbose_name=_('slum household'))
    one_shelter_deprivation = models.FloatField(blank=True, null=True, verbose_name=_('one shelter deprivation'))
    two_shelter_deprivations = models.FloatField(blank=True, null=True, verbose_name=_('two shelter deprivations'))
    three_shelter_deprivations = models.FloatField(blank=True, null=True, verbose_name=_('three shelter deprivations'))
    four_shelter_deprivations = models.FloatField(blank=True, null=True, verbose_name=_('four shelter deprivations'))

    gender = models.IntegerField(blank=True, null=True, choices=((1, _('Man')), (2, _('Woman'))))

    extra_type_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Extra type field for matrix tables'))

    is_matrix = models.BooleanField(default=False)

    type_deprivation = models.IntegerField(choices=types_deprivation)

    class Meta:
        abstract = True

class TypeDeprivationCity(TypeDeprivation):
    indicator = models.ForeignKey('UnHabitatIndicatorCity')
    def __unicode__(self):
        return self.get_type_deprivation_display()

    class Meta:
        app_label = "data"
        verbose_name = _("Type Deprivation City")
        verbose_name_plural = _('Type Deprivations City')

class TypeDeprivationCountry(TypeDeprivation):
    indicator = models.ForeignKey('UnHabitatIndicatorCountry')
    def __unicode__(self):
        if self.extra_type_name:
            return "year: %s, country: %s, type %s, table %s" % (self.indicator.year, self.indicator.country, self.extra_type_name, self.get_type_deprivation_display())
        else:
            return "year: %s, country: %s, table %s" % (self.indicator.year, self.indicator.country, self.get_type_deprivation_display())


    class Meta:
        app_label = "data"
        verbose_name = _("Type Deprivation Country")
        verbose_name_plural = _('Type Deprivation Countries')


class UnhabitatIndicator(models.Model):
    class Meta:
        abstract = True

    year = models.IntegerField()

    #extra options
    year_plus_range = models.IntegerField(blank=True, null=True, verbose_name=_('Range in year+'), help_text=_('Some tables ask for year ranges, with this field we can add this range'))

    #Table 4: Total UnHabitatIndicatorCountry at Mid-Year by Major Area, Region and Country, 1950-2050 (thousands)
    population = models.IntegerField(blank=True, null=True, verbose_name=_('Table 4: Total UnHabitatIndicatorCountry at Mid-Year by Major Area, Region and Country, 1950-2050 (thousands)'))

    #Table 7: Urban slum population at mid-year
    urban_slum_population = models.IntegerField(blank=True, null=True, verbose_name=_('Table 7: Urban slum population at mid-year'))
    slum_proportion_living_urban = models.FloatField(blank=True, null=True, verbose_name=_('Table 7: proportion of urban population living'))
    urban_population = models.FloatField(blank=True, null=True, verbose_name=_('Table 7: urban population'))


    #Table 9: Under-Five mortality rate
    under_five_mortality_rate = models.IntegerField(blank=True, null=True, verbose_name=_('Table 9: Under-Five mortality rate'))

    #Table 10: Water resources
    improved_water = models.FloatField(blank=True, null=True, verbose_name=_('Table 10: Improved water source'))
    piped_water = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Piped water'))
    public_tap_pump_borehole = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Public tap/pump bore hole'))
    protected_well = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Protected well'))
    improved_spring_surface_water = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Improved spring surface water'))
    rainwater = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Rainwater'))
    bottle_water = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Bottle water'))
    improved_toilet = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Improved toilet'))
    improved_flush_toilet = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Improved flush toilet'))
    improved_pit_latrine = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Improved pit latrine'))
    pit_latrine_with_slab_or_covered_latrine = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Pit latrine with slab or covered latrine'))
    composting_toilet = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Composting toilet'))
    pit_latrine_without_slab = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Pit latrine without slab'))
    pump_borehole = models.FloatField(blank=True, null=True,verbose_name=_('Table 10: Pump bore hole'))

    #Table 11: Access to improved toilet,improved floor, sufficient living, connection to telephone, connection to electricity.
    improved_floor = models.FloatField(blank=True, null=True, verbose_name=_('Table 11 - Improved floor'))
    sufficient_living = models.FloatField(blank=True, null=True, verbose_name=_('Table 11 - sufficient living'))
    has_telephone = models.FloatField(blank=True, null=True, verbose_name=_('Table 11 - has telephone'))
    connection_to_electricity = models.FloatField(blank=True, null=True, verbose_name=_('Table 11 - connection to electricity'))

    #Table 17:     enrollment_male_primary_education = models.FloatField(blank=True, null=True, verbose_name=_('Table 17: Enrolment in primary education male'))
    enrollment_female_primary_education = models.FloatField(blank=True, null=True, verbose_name=_('Table 17: Enrolment in primary education female'))
    enrollment_male_primary_education = models.FloatField(blank=True, null=True, verbose_name=_('Table 17: Enrolment in primary education male'))





    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)



class UnHabitatIndicatorCountry(UnhabitatIndicator):
    """
    Added model from project Un-Habitat phase 2 project.

    Storing all received indicators from 28 tables related to countries. This is from the global urban indicators database 2010.xls file

    This is on a per country and year basis
    """

    #country and year are the primary keys
    country = models.ForeignKey(Country)

    #Table 2: Average annual rate of change of the Total Population by major area, Region and Country, 1950-2050 (%)
    avg_annual_rate_change_total_population = models.FloatField(blank=True, null=True, verbose_name=_('Table 2: Average annual rate of change of the Total Population'))


    #Table 5:Average Annual Rate of Change of the Percentage Urban by Major Area, Region and Country, 1950-2050 (per cent)
    avg_annual_rate_change_percentage_urban = models.FloatField(blank=True, null=True, verbose_name=_('Table 5:Average Annual Rate of Change of the Percentage Urban by Major Area, Region and Country, 1950-2050 (per cent)'))

    #Table 6- Population of Rural and urban areas and percentage urban 2007
    pop_urban_area = models.FloatField(blank=True, null=True, verbose_name=_('Table 6- Population urban areas and percentage urban'))
    pop_rural_area = models.FloatField(blank=True, null=True, verbose_name=_('Table 6- Population Rural areas and percentage urban'))
    pop_urban_percentage = models.FloatField(blank=True, null=True, verbose_name=_('Table 6- Percentage urban areas urban'))





    def __unicode__(self):
            return "%s of %s" % (self.year, self.country.get_iso_display())

    class Meta:
        app_label = "data"
        verbose_name = _("Unhabitat Global Indicator per country")
        verbose_name_plural = _('Unhabitat Global Indicators per country')

##Table 13 matrix waste disposal by shelter deprivation
#class SolidWastDisposalShelterDeprivation(models.Model):
#    unhabitat_indicator_country = models.ForeignKey(UnHabitatIndicatorCountry)
#
#    kind_of_soil_waste_disposal = models.CharField(max_length=100, verbose_name=_('Kind of soil waste disposal'))
#
#
#    def __unicode__(self):
#        return "%s from %s" % (self.kind_of_soil_waste_disposal, self.unhabitat_indicator_country.country.country_name)
#
#    class Meta:
#        app_label = "data"
#        verbose_name = _("Table 13: matrix waste disposal by shelter deprivation")
#        verbose_name_plural = _('Table 13: matrix waste disposals by shelter deprivation')
#
##Table 14: Percent distribution of type of cooking fuel by shelter deprivation
#class DistributionCookingFuelByShelterDepr(models.Model):
#    unhabitat_indicator_country = models.ForeignKey(UnHabitatIndicatorCountry)
#
#    type_of_cooking_fuel = models.CharField(max_length=100, verbose_name=_('Type of cooking fuel'))
#
#
#    def __unicode__(self):
#        return "%s from %s" % (self.type_of_cooking_fuel, self.unhabitat_indicator_country.country.country_name)
#
#    class Meta:
#        app_label = "data"
#        verbose_name = _("Table 14: Percent distribution of type of cooking fuel by shelter deprivation")
#        verbose_name_plural = _('Table 14: Percent distribution of type of cooking fuel by shelter deprivation')

class UnHabitatIndicatorCity(UnhabitatIndicator):
    """
    Added model from project Un-Habitat phase 2 project.

    Storing all received indicators from 28 tables related to countries. This is from the global urban indicators database 2010.xls file

    This is on a per country and year basis
    """

    #country and year are the primary keys
    city = models.ForeignKey(City)

    #Table 1: city population of urban agglomerations with 750k inhabitants or more
    pop_urban_agglomerations = models.FloatField(blank=True, null=True, verbose_name=_('Table 1: city population of urban agglomerations with 750k inhabitants or more'))

    #Table 3: Average annual rate of change of urban agglomerations with 750,000 inhabitants or more in 2007, by country, 1950-2025
    avg_annual_rate_change_urban_agglomerations = models.FloatField(blank=True, null=True, verbose_name=_('Table 3: Average annual rate of change of urban agglomerations with 750,000 inhabitants'))

    #Table 29: Percentage of children with diarrhea in last two weeks, ARI, fever in last 2 weeks
    diarrhea_last_two_weeks = models.FloatField(blank=True, null=True, verbose_name=_('Table 29: diarrhea in last two weeks'))
    diarrhea_had_ari = models.FloatField(blank=True, null=True, verbose_name=_('Table 29: had ari'))
    fever_last_two_weeks = models.FloatField(blank=True, null=True, verbose_name=_('Table 29: fever in last two weeks'))

    #Table 30: Percentage of Malnourished and of Children immunised against measles
    perc_malnourished =models.FloatField(blank=True, null=True, verbose_name=_('Table 30: Percentage of Malnourished'))
    perc_measles =models.FloatField(blank=True, null=True, verbose_name=_('Table 30: Children immunised against measles'))

    cpi_5_dimensions = models.FloatField(blank=True, null=True, verbose_name=_('City Prosperity Index (CPI) with 5 Dimensions'))
    cpi_4_dimensions = models.FloatField(blank=True, null=True, verbose_name=_('City Prosperity Index (CPI) with 4 Dimensions'))
    cpi_productivity_index = models.FloatField(blank=True, null=True, verbose_name=_('Productivity Index'))
    cpi_quality_of_live_index = models.FloatField(blank=True, null=True, verbose_name=_('Quality of life Index'))
    cpi_infrastructure_index = models.FloatField(blank=True, null=True, verbose_name=_('Infrastructure Index'))
    cpi_environment_index = models.FloatField(blank=True, null=True, verbose_name=_('Enivronment Index'))
    cpi_equity_index = models.FloatField(blank=True, null=True, verbose_name=_('Equity Index'))






    def __unicode__(self):
        return "%s of %s" % (self.year, self.city.name)

    class Meta:
        app_label = "data"
        verbose_name = _("Unhabitat Global Indicator per city")
        verbose_name_plural = _('Unhabitat Global Indicators per city')




class Region(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True, choices=REGION_CHOICES)

    def __unicode__(self):
        return "%s - %s" % (self.code, self.get_code_display())

    class Meta:
        app_label = "data"
        verbose_name = _("region")
        verbose_name_plural = _("regions")


class CommonType(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class VocabularyType(models.Model):
    code = models.CharField(max_length=15, primary_key=True, choices=VOCABULARY_CHOICES)

    class Meta:
        app_label = "data"


class SignificanceType(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True, choices=POLICY_SIGNIFICANCE_CHOICES)

    class Meta:
        app_label = "data"


class CollaborationType(models.Model):
    code = models.CharField(max_length=55, primary_key=True)

    class Meta:
        app_label = "data"


class FlowType(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True, choices=FLOW_TYPE_CHOICES)

    class Meta:
        app_label = "data"


class FinanceType(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True)

    class Meta:
        app_label = "data"


class AidType(models.Model):
    code = models.CharField(max_length=5, primary_key=True)

    class Meta:
        app_label = "data"


class TiedAidStatusType(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True, choices=TIED_AID_STATUS_CHOICES)

    class Meta:
        app_label = "data"


class CurrencyType(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    language = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "data"


class ActivityStatusType(models.Model):
    code = models.IntegerField(max_length=8, unique=True, choices=STATUS_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "data"


class Sector(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=55, primary_key=True)
    vocabulary_type = models.ForeignKey(VocabularyType, blank=True, null=True)

    class Meta:
        app_label = "data"


class Budget(models.Model):
    period_start = models.DateField()
    period_end = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.IntegerField(max_length=2, choices=BUDGET_TYPE_CHOICES, blank=True, null=True)
    currency = models.ForeignKey(CurrencyType, blank=True, null=True)

    class Meta:
        app_label = "data"


class Transaction(models.Model):
    transaction_type = models.CharField(max_length=55, choices=TRANSACTION_TYPE_CHOICES)
    provider_org = models.ForeignKey(Organisation, related_name='provider_org')
    receiver_org = models.ForeignKey(Organisation, related_name='receiver_org', blank=True, null=True)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    value_date = models.DateField()
    transaction_date = models.DateField(blank=True, null=True)
    flow_type = models.ForeignKey(FlowType, blank=True, null=True)
    finance_type = models.ForeignKey(FinanceType, blank=True, null=True)
    aid_type = models.ForeignKey(AidType, blank=True, null=True)
    disbursement_channel = models.IntegerField(choices=DISBURSEMENT_CHANNEL_CHOICES, blank=True, null=True)
    tied_aid_status_type = models.IntegerField(choices=TIED_AID_STATUS_CHOICES, blank=True, null=True)
    currency = models.ForeignKey(CurrencyType, blank=True, null=True)

    class Meta:
        app_label = "data"


class Contact(models.Model):
    organisation = models.CharField(max_length=255, blank=True, null=True)
    person_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    mailing_address = models.CharField(max_length=500)

    class Meta:
        abstract = True


class Document(models.Model):
    """
    @url        The target URL of the external document, e.g. "http://www.example.org/doc.html".
    @format     The MIME type of the external document, e.g. "application/pdf". A partial list of MIME types
                appears at http://iatistandard.org/codelists/file_format
    @language   The ISO 639 language code for the target document, e.g. "en".
    """
    url = models.URLField()
    format = models.CharField(max_length=55, null=True, blank=True)
    language = models.ForeignKey(Language, null=True, blank=True)

    class Meta:
        abstract = True


class Website(models.Model):
    url = models.URLField()

    class Meta:
        abstract = True