# Tastypie specific
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
from data.models.common import ActivityStatusType, Population, Country
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

class UnHabitatDemoGraphicResource(ModelResource):
    class Meta:
        queryset = Population.objects.all()
        include_resource_uri = False
        resource_name = 'indicators'
        serializer = Serializer(formats=['xml', 'json'])
        filtering = {"year": ALL }


    def dehydrate(self, bundle):
        bundle.data['country_iso'] = bundle.obj.country.iso
        bundle.data['country_name'] = bundle.obj.country.get_iso_display()
        bundle.data['dac_region_code'] = bundle.obj.country.dac_region_code
        bundle.data['dac_region_name'] = bundle.obj.country.dac_region_name

        bundle.data.pop('id')

        return bundle

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(UnHabitatDemoGraphicResource, self).apply_filters(request, applicable_filters)
        regions = request.GET.get('regions', None)
        countries = request.GET.get('country_name', None)
        isos = request.GET.get('iso', None)



        filters = {}
        if regions:
            # @todo: implement smart filtering with seperator detection
            regions = regions.replace('|', ' ').replace('-', ' ').split(' ')
            filters.update(dict(country__dac_region_code__in=regions))
        if countries:
            countries = countries.replace('|', ' ').replace('-', ' ').split(' ')
            filters.update(dict(country__country_name__in=countries))
        if isos:
            isos = isos.replace('|', ' ').replace('-', ' ').split(' ')
            filters.update(dict(country__iso__in=isos))

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