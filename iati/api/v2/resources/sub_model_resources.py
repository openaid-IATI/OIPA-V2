# Tastypie specific
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.authentication import ApiKeyAuthentication
from tastypie.http import HttpGone, HttpMultipleChoices
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer

# Data specific
import pdb
from tastypie import fields
from tastypie.utils import trailing_slash
from data.models.activity import IATIActivityBudget, IATIActivityDocument
from data.models.activity import IATIActivityCountry
from data.models.activity import IATIActivityRegion
from data.models.activity import IATIActivitySector
from data.models.activity import IATITransaction
from data.models.common import ActivityStatusType, UnHabitatIndicatorCountry, Country, UnHabitatIndicatorCity, City, Region
from data.models.common import CollaborationType
from data.models.common import FlowType
from data.models.common import AidType
from data.models.common import FinanceType
from data.models.common import TiedAidStatusType


class StatusResource(ModelResource):
    class Meta:
        queryset = ActivityStatusType.objects.all()
        fields = ['code']
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data['name'] = bundle.obj.get_code_display()
        return bundle

class OnlyCountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all().distinct().order_by('country_name')
        resource_name = 'country'


class OnlyRegionResource(ModelResource):
    class Meta:
        queryset = Region.objects.all().distinct().order_by('code')
        resource_name = 'region'
class OnlyCityResource(ModelResource):
    class Meta:
        queryset = City.objects.all().distinct().order_by('name')
        resource_name = 'city'

    def dehydrate(self, bundle):
        bundle.data['country'] = bundle.obj.country.iso
        return bundle

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(OnlyCityResource, self).apply_filters(request, applicable_filters)
        countries = request.GET.get('country', None)



        filters = {}
        if countries:
            countries = countries.replace('|', ',').replace('-', ',').split(',')
            filters.update(dict(country__iso__in=countries))

        return base_object_list.filter(**filters).distinct()

class UnHabitatIndicatorCountryResource(ModelResource):
    class Meta:
        queryset = UnHabitatIndicatorCountry.objects.all()
        include_resource_uri = False
        resource_name = 'indicators-country'
        serializer = Serializer(formats=['xml', 'json'])
        filtering = {"year": ALL }
#        authentication = ApiKeyAuthentication()


    def dehydrate(self, bundle):
        bundle.data['country_iso'] = bundle.obj.country.iso
        bundle.data['country_iso3'] = bundle.obj.country.iso3

        bundle.data['country_name'] = bundle.obj.country.get_iso_display()
        bundle.data['dac_region_code'] = bundle.obj.country.dac_region_code
        bundle.data['dac_region_name'] = bundle.obj.country.dac_region_name
        tpset = bundle.obj.typedeprivationcountry_set.all()
        tp_list = {}
        for tp in tpset:
            temp_list = {}
            temp_list['type'] = tp.get_type_deprivation_display()
            temp_list['non_slum_household'] = tp.non_slum_household
            temp_list['slum_household'] = tp.slum_household
            temp_list['one_shelter_deprivation'] = tp.one_shelter_deprivation
            temp_list['two_shelter_deprivations'] = tp.two_shelter_deprivations
            temp_list['three_shelter_deprivations'] = tp.three_shelter_deprivations
            temp_list['four_shelter_deprivations'] = tp.four_shelter_deprivations
            temp_list['gender'] = tp.gender
            temp_list['extra_type_name'] = tp.extra_type_name
            temp_list['is_matrix'] = tp.is_matrix
            temp_list['urban'] = tp.urban
            temp_list['total'] = tp.total
            temp_list['rural'] = tp.rural

            tp_list['deprivation_id_'+str(tp.id)] = temp_list
        bundle.data['deprivation'] = tp_list
        bundle.data.pop('id')

        return bundle

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(UnHabitatIndicatorCountryResource, self).apply_filters(request, applicable_filters)
        regions = request.GET.get('regions', None)
        countries = request.GET.get('country_name', None)
        isos = request.GET.get('iso', None)
        indicators = request.GET.get('indicators', None)



        filters = {}
        if regions:
            # @todo: implement smart filtering with seperator detection
            regions = regions.replace('|', ',').replace('-', ',').split(',')
            filters.update(dict(country__dac_region_code__in=regions))
        if countries:
            countries = countries.replace('|', ',').replace('-', ',').split(',')
            filters.update(dict(country__country_name__in=countries))
        if isos:
            isos = isos.replace('|', ',').replace('-', ',').split(',')
            filters.update(dict(country__iso__in=isos))
#

        return base_object_list.filter(**filters).distinct()

class UnHabitatIndicatorCityResource(ModelResource):
    class Meta:
        queryset = UnHabitatIndicatorCity.objects.all()
        include_resource_uri = False
        resource_name = 'indicators-city'
        serializer = Serializer(formats=['xml', 'json'])
        filtering = {"year": ALL }
    #        authentication = ApiKeyAuthentication()


    def dehydrate(self, bundle):
        bundle.data['country_iso'] = bundle.obj.city.country.iso
        bundle.data['country_name'] = bundle.obj.city.country.get_iso_display()
        bundle.data['dac_region_code'] = bundle.obj.city.country.dac_region_code
        bundle.data['dac_region_name'] = bundle.obj.city.country.dac_region_name
        bundle.data['city_name'] = bundle.obj.city.name

    #        bundle.data['']

        bundle.data.pop('id')

        return bundle

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(UnHabitatIndicatorCityResource, self).apply_filters(request, applicable_filters)
        regions = request.GET.get('regions', None)
        countries = request.GET.get('country_name', None)
        isos = request.GET.get('iso', None)
        city = request.GET.get('city', None)



        filters = {}
        if regions:
            # @todo: implement smart filtering with seperator detection
            regions = regions.replace('|', ',').replace('-', ',').split(',')
            filters.update(dict(city__country__dac_region_code__in=regions))
        if countries:
            countries = countries.replace('|', ',').replace('-', ',').split(',')
            filters.update(dict(city__country__country_name__in=countries))
        if isos:
            isos = isos.replace('|', ',').replace('-', ',').split(',')
            filters.update(dict(city__country__iso__in=isos))
        if city:
            city = city.replace('|', ',').replace('-', ',').split(',')

            filters.update(dict(city__name__in=city))

        return base_object_list.filter(**filters).distinct()

class RecipientCountryResource(ModelResource):
    class Meta:
        queryset = IATIActivityCountry.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data['iso'] = bundle.obj.country.iso
        bundle.data['name'] = bundle.obj.country.get_iso_display()
        bundle.data.pop('id')
        return bundle





class RecipientRegionResource(ModelResource):
    class Meta:
        queryset = IATIActivityRegion.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data['code'] = bundle.obj.region.code
        bundle.data['name'] = bundle.obj.region.get_code_display()
        bundle.data.pop('id')
        return bundle


class SectorResource(ModelResource):
    class Meta:
        queryset = IATIActivitySector.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data['code'] = bundle.obj.sector.code
        bundle.data['name'] = bundle.obj.sector.name
        bundle.data.pop('id')
        return bundle


class CollaborationTypeResource(ModelResource):
    class Meta:
        queryset = CollaborationType.objects.all()
        include_resource_uri = False


class FlowTypeResource(ModelResource):
    class Meta:
        queryset = FlowType.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data['name'] = bundle.obj.get_code_display()
        return bundle


class AidTypeResource(ModelResource):
    class Meta:
        queryset = AidType.objects.all()
        include_resource_uri = False


class FinanceTypeResource(ModelResource):
    class Meta:
        queryset = FinanceType.objects.all()
        include_resource_uri = False


class TiedAidStatusTypeResource(ModelResource):
    class Meta:
        queryset = TiedAidStatusType.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data['name'] = bundle.obj.get_code_display()
        return bundle


class ActivityBudgetResource(ModelResource):
    class Meta:
        queryset = IATIActivityBudget.objects.all()
        include_resource_uri = False
        excludes = ['id']


class TransactionResource(ModelResource):
    class Meta:
        queryset = IATITransaction.objects.all()
        include_resource_uri = False
        filtering = {
            'value': ALL,
            }

    def dehydrate(self, bundle):
        # todo convert to resource
        if bundle.obj.currency:
            bundle.data['currency'] = bundle.obj.currency.code
        bundle.data.pop('id')
        return bundle


class DocumentResource(ModelResource):
    class Meta:
        queryset = IATIActivityDocument.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data.pop('id')
        return bundle