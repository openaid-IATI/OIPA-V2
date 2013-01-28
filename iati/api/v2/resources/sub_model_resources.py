# Tastypie specific
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer

# Data specific
import pdb
from data.models.activity import IATIActivityBudget, IATIActivityDocument
from data.models.activity import IATIActivityCountry
from data.models.activity import IATIActivityRegion
from data.models.activity import IATIActivitySector
from data.models.activity import IATITransaction
from data.models.common import ActivityStatusType
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