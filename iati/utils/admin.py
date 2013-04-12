# Django specific
from django.conf.urls import patterns
from django.contrib import admin

# App specific
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from tastypie.models import ApiKey
from data.models.common import  UnHabitatIndicatorCountry, UnHabitatIndicatorCity, TypeDeprivationCity, TypeDeprivationCountry, Country, City
from utils.models import IATIXMLSource, Publisher, ParseSchedule, UnHabitatParserLog, UnhabitatRecordLog


class IATIXMLSourceInline(admin.TabularInline):
    model = IATIXMLSource
    extra = 0


class IATIXMLSourceAdmin(admin.ModelAdmin):
    list_display = ['ref', 'publisher', 'type', 'date_created', 'get_parse_status', 'date_updated']
    list_filter = ('publisher', 'type')

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.js',
            '/static/js/xml_source_admin.js',
        )

    def get_urls(self):
        urls = super(IATIXMLSourceAdmin, self).get_urls()
        extra_urls = patterns('',
            (r'^parse-xml/$', self.admin_site.admin_view(self.parse_view))
        )
        return extra_urls + urls

    def parse_view(self, request):
        xml_id = request.GET.get('xml_id')
        obj = get_object_or_404(IATIXMLSource, id=xml_id)
        obj.process(1)
        return HttpResponse('Success')


class PublisherAdmin(admin.ModelAdmin):
    inlines = [IATIXMLSourceInline]
    list_display = ('org_name', 'org_abbreviate')

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.js',
            '/static/js/publisher_admin.js',
            )

    def get_urls(self):
        urls = super(PublisherAdmin, self).get_urls()
        extra_urls = patterns('',
            (r'^parse-publisher/$', self.admin_site.admin_view(self.parse_view))
        )
        return extra_urls + urls

    def parse_view(self, request):
        publisher_id = request.GET.get('publisher_id')
        for obj in IATIXMLSource.objects.filter(publisher__id=publisher_id):
            obj.process(1)
        return HttpResponse('Success')


class ParseScheduleAdmin(admin.ModelAdmin):
    list_display = ['iati_xml_source', 'get_interval_display',]

class UnHabitatIndicatorCountryAdmin(admin.ModelAdmin):
    search_fields = ['country__iso']
    list_filter = ['year', 'country',]

class UnHabitatIndicatorCityAdmin(admin.ModelAdmin):
    search_fields = ['city__name']
    list_filter = ['city', 'year',]

class TypeDeprivationCityAdmin(admin.ModelAdmin):
    raw_id_fields = ('indicator',)
    list_filter = ['type_deprivation', 'indicator__year', 'indicator__city',]

class TypeDeprivationCountryAdmin(admin.ModelAdmin):
    raw_id_fields = ('indicator',)
    list_filter = ['type_deprivation','indicator__year', 'indicator__country',]

class UnhabitatRecordLogAdmin(admin.ModelAdmin):
    search_fields = ['raw_data']
    list_filter = ['country_input_name']

admin.site.register(Publisher, PublisherAdmin)
admin.site.register(IATIXMLSource, IATIXMLSourceAdmin)
admin.site.register(ParseSchedule, ParseScheduleAdmin)
admin.site.register(UnHabitatIndicatorCountry, UnHabitatIndicatorCountryAdmin)
admin.site.register(UnHabitatIndicatorCity, UnHabitatIndicatorCityAdmin)
admin.site.register(TypeDeprivationCity, TypeDeprivationCityAdmin)
admin.site.register(TypeDeprivationCountry, TypeDeprivationCountryAdmin)
#admin.site.register(ApiKey)
admin.site.register(UnHabitatParserLog)
admin.site.register(UnhabitatRecordLog, UnhabitatRecordLogAdmin)
