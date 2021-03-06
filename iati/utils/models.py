import datetime
import os
import tempfile
from django.db.models.signals import post_save
from lxml import objectify
from StringIO import StringIO

# Django specific
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# App specific
from data.management.commands.import_iati_xml import ActivityParser
from data.management.commands.import_iati_xml import OrganisationParser
from utils.dataset_syncer import DatasetSyncer
from django.contrib.auth.models import User
from tastypie.models import create_api_key

#this post save signals generates an API key for the user
models.signals.post_save.connect(create_api_key, sender=User)

parsers = {
    'iati-organisations': OrganisationParser,
    'iati-activities': ActivityParser
}


INTERVAL_CHOICES = (
    (u'YEARLY', _(u"Parse yearly")),
    (u'MONTHLY', _(u"Parse monthly")),
    (u'WEEKLY', _(u"Parse weekly")),
    (u'DAILY', _(u"Parse daily")),
)
class Publisher(models.Model):
    org_name = models.CharField(max_length=255)
    org_abbreviate = models.CharField(max_length=55, blank=True, null=True)
    default_interval = models.CharField(verbose_name=_(u"Interval"), max_length=55, choices=INTERVAL_CHOICES, default=u'MONTHLY')

    def __unicode__(self):
        if self.org_abbreviate:
            return self.org_abbreviate
        return self.org_name

    class Meta:
        app_label = "utils"
        ordering = ["org_name"]

def fix(value):
    return unicode(str(value).lower().replace(' ', '_'))


def get_upload_path(instance, filename):
    return os.path.join("utils", fix(instance.get_type_display()), fix(instance.publisher), fix(filename))

class IATIXMLSource(models.Model):
    TYPE_CHOICES = (
        (1, _(u"Activity Files")),
        (2, _(u"Organisation Files")),
    )
    ref = models.CharField(verbose_name=_(u"Reference"), max_length=55, help_text=_(u"Reference for the XML file. Preferred usage: 'collection' or single country or region name"))
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    publisher = models.ForeignKey(Publisher)
    source_url = models.URLField(unique=True, help_text=_(u"Hyperlink to an IATI activity or organisation XML file."))
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        app_label = "utils"
        ordering = ["ref"]

    def __unicode__(self):
        return self.ref

    def get_parse_status(self):
        return mark_safe("<img class='loading' src='/static/img/loading.gif' alt='loading' style='display:none;' /><a data-xml='xml_%i' class='parse'><img src='/static/img/utils.parse.png' style='cursor:pointer;' /></a>") % self.id
    get_parse_status.allow_tags = True
    get_parse_status.short_description = _(u"Parse status")

    def process(self, verbosity, save=True):
        dirname, filename = os.path.split(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../media/utils/temp_files/')+self.ref)
        prefix, suffix = os.path.splitext(filename)
        fd, filename = tempfile.mkstemp(suffix, prefix+"_", dirname)
        file_url = self.source_url
        try:
            try:
                # python >= 2.7
                import requests
                r = requests.get(file_url)
                f = StringIO(r.content)
            except ImportError:
                # python <= 2.6
                import urllib2
                r = urllib2.urlopen(file_url)
                f = r
            file = ContentFile(f.read(), filename)
            file.close()
            try:
                tree = objectify.parse(file)
                parser_cls = parsers[tree.getroot().tag]
                try:
                    parser_cls(tree, True, verbosity).parse()
                    os.remove(file.name)
                except Exception, e:
                    os.remove(file.name)
                    raise Exception, e #TODO log error
            except KeyError:
                raise ImportError(u"Undefined document structure")
        except Exception, e:
            pass #TODO log error
        if save:
            self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.process(verbosity=1, save=False)
        super(IATIXMLSource, self).save()



class ParseSchedule(models.Model):
    interval = models.CharField(verbose_name=_(u"Interval"), max_length=55, choices=INTERVAL_CHOICES)
    iati_xml_source = models.ForeignKey(IATIXMLSource, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return "%s %s" % (self.get_interval_display(), self.iati_xml_source.source_url)

    class Meta:
        app_label = "utils"

    def _add_month(self, d,months=1):
        year, month, day = d.timetuple()[:3]
        new_month = month + months
        return datetime.date(year + ((new_month-1) / 12), (new_month-1) % 12 +1, day)

    def process(self, verbosity):
        if self.interval == u'YEARLY' and (self._add_month(self.iati_xml_source.date_updated, 12) <= datetime.datetime.now().date()):
            self.iati_xml_source.process(verbosity)
        elif self.interval == u'MONTHLY' and (self._add_month(self.iati_xml_source.date_updated) <= datetime.datetime.now().date()):
            self.iati_xml_source.process(verbosity)
        elif self.interval == u'WEEKLY' and (self.iati_xml_source.date_updated+datetime.timedelta(7) <= datetime.datetime.today()):
            self.iati_xml_source.process(verbosity)
        elif self.interval == u'DAILY' and (self.iati_xml_source.date_updated+datetime.timedelta(1) <= datetime.datetime.today()):
            self.iati_xml_source.process(verbosity)

class DatasetSync(models.Model):
    TYPE_CHOICES = (
        (1, _(u"Activity Files")),
        (2, _(u"Organisation Files")),
        )

    interval = models.CharField(verbose_name=_(u"Interval"), max_length=55, choices=INTERVAL_CHOICES)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)

    def __unicode__(self):
        return self.interval

    class Meta:
        app_label = "utils"

    def sync_now(self):
        return mark_safe("<img class='loading' src='/static/img/loading.gif' alt='loading' style='display:none;' /><a data-sync='sync_%i' class='sync    '><img src='/static/img/utils.parse.png' style='cursor:pointer;' /></a>") % self.id
    sync_now.allow_tags = True
    sync_now.short_description = _(u"Sync now?")

    def _add_month(self, d,months=1):
        year, month, day = d.timetuple()[:3]
        new_month = month + months
        return datetime.date(year + ((new_month-1) / 12), (new_month-1) % 12 +1, day)

    def process(self):
        if self.interval == u'YEARLY' and (self._add_month(self.date_updated, 12) <= datetime.datetime.now().date()):
            self.sync_dataset_with_iati_api()
        elif self.interval == u'MONTHLY' and (self._add_month(self.date_updated) <= datetime.datetime.now().date()):
            self.sync_dataset_with_iati_api()
        elif self.interval == u'WEEKLY' and (self.date_updated+datetime.timedelta(7) <= datetime.datetime.today()):
            self.sync_dataset_with_iati_api()
        elif self.interval == u'DAILY' and (self.date_updated+datetime.timedelta(1) <= datetime.datetime.today()):
            self.sync_dataset_with_iati_api()

    def sync_dataset_with_iati_api(self):
        syncer = DatasetSyncer()
        syncer.synchronize_with_iati_api(self.type)

def update_publisher_records(sender, instance, created, **kwargs):
    if not created:
        for iati_xml_source in IATIXMLSource.objects.filter(publisher__id=instance.id):
            try:
                ParseSchedule.objects.get(iati_xml_source=iati_xml_source)
            except ParseSchedule.DoesNotExist:
                ParseSchedule.objects.create(
                    iati_xml_source=iati_xml_source,
                    interval=instance.default_interval
                )

post_save.connect(update_publisher_records, sender=Publisher)

type_unhabitat_uploads = (
    (1, _('Table 4: Total Population at Mid-Year by Major Area, Region and Country, 1950-2050 (thousands)')),
    (2, _('Table 7: Urban Slum UnHabitatIndicatorCountry')),
    (3, _('Table 7: Proportion of urban population living in slum area')),
    (29, _('Table 7: Urban Population')),
    (4, _('Table 9: Under-five mortality rate')),
    (5, _('Table 10: Improved water source and improved toilet')),
    (6, _('ISO DAC Countries Regions')),
    (7, _('Table 1- city population of urban agglomerations with 750k inhabitants or more')),
    (8, _('Table 2: Average annual rate of change of the Total Population by major area, Region and Country, 1950-2050 (%)')),
    (9, _('Table 3: Average annual rate of change of urban agglomerations with 750,000 inhabitants or more in 2007, by country, 1950-2025')),
    (10, _('Table 5:Average Annual Rate of Change of the Percentage Urban by Major Area, Region and Country, 1950-2050 (per cent)')),
    (11, _('Table 6: Population of Rural and urban areas and percentage urban, 2007')),
    (12, _('Table 11: Access to improved toilet,improved floor, sufficient living, connection to telephone, connection to electricity.')),
    (13, _('Table 12: Table 12: Improved Services (City Level)')),
#    (14, _('Table 13: Solid waste disposal by shelter deprivation')),
    (15, _('Table 14: Percent distribution of type of cooking fuel by shelter deprivation')),
    (16, _('Table 15: Education; Literacy Rates by Shelter Deprivation (Woman)')),
    (17, _('Table 16: Enrolmen in primary education in urban and rural areas male')),
    (26, _('Table 16: Enrolmen in primary education in urban and rural areas female')),

    (18, _('Table 17: Enrolment in primary education  (female and male)(City)')),
#    (19, _('Table 18: Percentage of female aged 15-24 years unemployed by shelter depriviation')),
#    (20, _('Table 18: Percentage of male aged 15-24 years unemployed by shelter depriviation')),

#    (21, _('Table 19: Percentage of female aged 15-24 years in informal employment by shelter depriviation')),
#    (22, _('Table 26: Percentage of children  with Diarhea')),
#    (23, _('Table 27: Percentage of women who were attended to during delivery by skilled personnel')),
#    (24, _('Table 28: Percentage of Malnourished children')),
#    (25, _('Table 28: Percentage of children immunised against Measles')),
    (27, _('Table 29: Percentage of children with diarrhea in last two weeks, ARI, fever in last 2 week')),
    (28, _('Table 30: Percentage of Malnourished and of Children immunised against measles')),
    (31, _('Table CPI: City Prosperity Index, and the components of its 5 dimensions')),
    (32, _('Convert unusable city names to usable city names')),
)

class UnHabitatParserLog(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
    type_upload = models.IntegerField(choices=type_unhabitat_uploads)
    ip_address = models.IPAddressField(null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)
    total_errors = models.IntegerField(default=0)
    total_processed = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, editable=True)
    date_updated = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        app_label = "utils"

class UnhabitatRecordLog(models.Model):
    parser = models.ForeignKey(UnHabitatParserLog)

    country_iso = models.CharField(max_length=255)
    message = models.CharField(max_length=255, null=True, blank=True)
    success = models.BooleanField(default=False)
    country_success = models.CharField(max_length=255, null=True, blank=True)
    city_success = models.CharField(max_length=255, null=True, blank=True)

    country_input_name = models.CharField(max_length=255)
    city_input_name = models.CharField(max_length=255, null=True, blank=True)
    raw_data = models.TextField(null=True, blank=True)

    year = models.IntegerField(max_length=4, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        app_label = "utils"

    def __unicode__(self):
        return self.raw_data

class ConversationCityNames(models.Model):
    unusable_name = models.CharField(max_length=255)
    usable_name = models.CharField(max_length=255)

    class Meta:
        app_label = 'utils'

