# Django specific
from django.conf.urls import patterns
from django.contrib import admin

# App specific
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from data.models.common import  Population
from utils.models import IATIXMLSource, Publisher, ParseSchedule


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


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(IATIXMLSource, IATIXMLSourceAdmin)
admin.site.register(ParseSchedule, ParseScheduleAdmin)
admin.site.register(Population)