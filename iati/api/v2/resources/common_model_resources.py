# Tastypie specific
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer

# Data specific
from data.models.activity import IATIActivityTitle, IATIActivityDescription
from data.models.common import Country, Language
from data.models.common import Region
from data.models.common import Sector
from data.models.statistics import ActivityStatistics


class CountryResource(ModelResource):
    """
    Resource for Countries
    """
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'countries'
        serializer = Serializer(formats=['xml', 'json'])

    def dehydrate(self, bundle):
        obj = self.obj_get(iso=bundle.data['iso'])
        bundle.data['name'] = obj.get_iso_display()
        return super(CountryResource, self).dehydrate(bundle)


class RegionResource(ModelResource):
    """
    Resource for Regions
    """
    class Meta:
        queryset = Region.objects.all()
        resource_name = 'regions'
        serializer = Serializer(formats=['xml', 'json'])

    def dehydrate(self, bundle):
        obj = self.obj_get(code=bundle.data['code'])
        bundle.data['name'] = obj.get_code_display()
        return super(RegionResource, self).dehydrate(bundle)


class SectorResource(ModelResource):
    """
    Resource for Regions
    """
    class Meta:
        queryset = Sector.objects.all()
        resource_name = 'sectors'
        serializer = Serializer(formats=['xml', 'json'])


class LanguageResource(ModelResource):
    include_resource_uri = False
    excludes = ['id']
    class Meta:
        queryset = Language.objects.all()


class TitleResource(ModelResource):
    language = fields.ToOneField(LanguageResource, 'language', full=True, null=True)
    class Meta:
        queryset = IATIActivityTitle.objects.all()
        include_resource_uri = False
        excludes = ['id']


class DescriptionResource(ModelResource):
    language = fields.ToOneField(LanguageResource, 'language', full=True, null=True)
    class Meta:
        queryset = IATIActivityDescription.objects.all()
        include_resource_uri = False
        excludes = ['id']


class ActivityStatisticResource(ModelResource):
    """
    Resource for ActivityStatistics
    """
    class Meta:
        queryset = ActivityStatistics.objects.all()
        resource_name = 'total_budgets'
        include_resource_uri = False
        excludes = ['id']
        filtering = {
            'total_budget': ['gt', 'gte', 'lt', 'lte'],
        }