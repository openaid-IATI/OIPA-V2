# Tastypie specific
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer

# Data specific
from data.models.activity import IATIActivityTitle
from data.models.activity import IATIActivityDescription
from data.models.common import Country
from data.models.common import Language
from data.models.common import Region
from data.models.common import Sector
from data.models.statistics import ActivityStatistics
from data.models.statistics import CountryStatistics
from data.models.statistics import OrganisationStatistics


class CountryStatisticResource(ModelResource):
    """
    Resource for CountryStatistics
    """
    class Meta:
        queryset = CountryStatistics.objects.all()
        include_resource_uri = False
        excludes = ['id']
        filtering = {
            'total_activities': ['gt', 'gte', 'lt', 'lte'],
        }


class OrganisationStatisticsResource(ModelResource):
    """
    Resource for OrganisationStatistics
    """
    class Meta:
        queryset = OrganisationStatistics.objects.all()
        include_resource_uri = False
        excludes = ['id']
        filtering = {
            'total_activities': ['gt', 'gte', 'lt', 'lte'],
        }


class CountryResource(ModelResource):
    """
    Resource for Countries
    """
    statistics = fields.OneToOneField(CountryStatisticResource, 'countrystatistics', full=True, null=True)

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'countries'
        serializer = Serializer(formats=['xml', 'json'])
        filtering = {
            'statistics': ALL_WITH_RELATIONS,
        }

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
    class Meta:
        queryset = Language.objects.all()
        include_resource_uri = False
        excludes = ['id']


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
        include_resource_uri = False
        excludes = ['id']
        filtering = {
            'total_budget': ['gt', 'gte', 'lt', 'lte'],
        }