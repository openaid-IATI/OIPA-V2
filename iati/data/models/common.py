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


    def __unicode__(self):
        return "%s - %s" % (self.iso, self.get_iso_display())

    @staticmethod
    def find_iso_country(country_name):
        import pdb
        countries = Country.objects.all()

        for country in countries:
#            pdb.set_trace()
            if country_name.decode('utf8') in country.get_iso_display() or country_name.decode('utf8')[:8] in country.get_iso_display() or country_name.decode('utf8')[-8:] in country.get_iso_display():
                return country
        print country_name
        return False
    class Meta:
        app_label = "data"
        verbose_name = _("country")
        verbose_name_plural = _("countries")

class Population(models.Model):
    """
    Added model from project Un-Habitat phase 2 project.

    Storing population data, slum population and slum proportion

    This is on a per country basis
    """
    country = models.ForeignKey(Country)
    year = models.IntegerField()
    population = models.IntegerField(blank=True, null=True, verbose_name=_('Table 4: Total Population at Mid-Year by Major Area, Region and Country, 1950-2050 (thousands)'))
    urban_slum_population = models.IntegerField(blank=True, null=True, verbose_name=_('Table 7: Urban slum population at mid-year'))
    under_five_mortality_rate = models.IntegerField(blank=True, null=True, verbose_name=_('Table 9: Under-Five mortality rate'))
    slum_proportion_living_urban = models.FloatField(blank=True, null=True, verbose_name=_('Table 7: Urban population living in slum area'))

    #water related statistics
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




    def __unicode__(self):
        return "%s of %s" % (self.year, self.country.get_iso_display())

    class Meta:
        app_label = "data"
        verbose_name = _("Unhabitat Global Indicator")
        verbose_name_plural = _('Unhabitat Global Indicators')

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