# Tastypie specific
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer

# Data specific
from data.models.common import Country
from data.models.common import Region
from data.models.common import Sector


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