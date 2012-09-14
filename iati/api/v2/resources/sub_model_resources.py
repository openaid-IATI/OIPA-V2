# Tastypie specific
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer

# Data specific
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


class RecipientCountryResource(ModelResource):
    class Meta:
        queryset = IATIActivityCountry.objects.all()
        include_resource_uri = False


class RecipientRegionResource(ModelResource):
    class Meta:
        queryset = IATIActivityRegion.objects.all()
        include_resource_uri = False


class SectorResource(ModelResource):
    class Meta:
        queryset = IATIActivitySector.objects.all()
        include_resource_uri = False


class CollaborationTypeResource(ModelResource):
    class Meta:
        queryset = CollaborationType.objects.all()
        include_resource_uri = False


class FlowTypeResource(ModelResource):
    class Meta:
        queryset = FlowType.objects.all()
        include_resource_uri = False


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

class DocumentResource(ModelResource):
    class Meta:
        queryset = IATIActivityDocument.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data.pop('id')
        return bundle