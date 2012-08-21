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

    def process(self, verbosity):
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
        self.save()


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
        else:
            self.iati_xml_source.process(verbosity)


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