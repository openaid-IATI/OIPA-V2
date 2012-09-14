import warnings

# Django specific
from django.db.models import Q

# Tastypie specific
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer

# Data specific
from data.models.activity import IATIActivity
from data.models.constants import COUNTRY_ISO_MAP
from data.models.organisation import Organisation, ParticipatingOrganisation

# App specific
from api.v2.resources.common_model_resources import ActivityStatisticResource, OrganisationStatisticsResource
from api.v2.resources.common_model_resources import DescriptionResource
from api.v2.resources.common_model_resources import TitleResource
from api.v2.resources.sub_model_resources import RecipientCountryResource
from api.v2.resources.sub_model_resources import RecipientRegionResource
from api.v2.resources.sub_model_resources import StatusResource
from api.v2.resources.sub_model_resources import SectorResource
from api.v2.resources.sub_model_resources import CollaborationTypeResource
from api.v2.resources.sub_model_resources import FlowTypeResource
from api.v2.resources.sub_model_resources import FinanceTypeResource
from api.v2.resources.sub_model_resources import AidTypeResource
from api.v2.resources.sub_model_resources import TiedAidStatusTypeResource
from api.v2.resources.sub_model_resources import ActivityBudgetResource
from api.v2.resources.sub_model_resources import TransactionResource
from api.v2.resources.sub_model_resources import DocumentResource
from utils.cache import NoTransformCache


class OrganisationResource(ModelResource):
    """
    Resource for IATI Organisations
    """
    statistics = fields.OneToOneField(OrganisationStatisticsResource, 'organisationstatistics', full=True, null=True)

    class Meta:
        queryset = Organisation.objects.all()
        resource_name = 'organisations'
        serializer = Serializer(formats=['xml', 'json'])
        excludes = ['date_created']
        filtering = {
            # example to allow field specific filtering.
            'org_name': ALL,
            'ref': ALL,
            'statistics': ALL_WITH_RELATIONS,
        }

#    def dehydrate(self, bundle):
#        obj = self.obj_get(ref=bundle.data['ref'])
#        bundle.data['type'] = obj.get_type_display()
#        return super(OrganisationResource, self).dehydrate(bundle)


class ParticipatingOrganisationResource(ModelResource):
    """
    Resource for IATI ParticipatingOrganisations
    """
    class Meta:
        queryset = ParticipatingOrganisation.objects.all()
        fields = ['ref', 'org_name', 'role', 'type']
        include_resource_uri = False


class ActivityResource(ModelResource):
    """
    Resource for IATI Activities
    """
    reporting_organisation = fields.ForeignKey(OrganisationResource, attribute='reporting_organisation', full=True, null=True)
    participating_organisations = fields.ToManyField(ParticipatingOrganisationResource, 'participatingorganisation_set', full=True, null=True)
    activity_status = fields.ForeignKey(StatusResource, attribute='activity_status', full=True, null=True)
    recipient_country = fields.ToManyField(RecipientCountryResource, 'iatiactivitycountry_set', full=True, null=True)
    recipient_region = fields.ToManyField(RecipientRegionResource, 'iatiactivityregion_set', full=True, null=True)
    activity_sectors = fields.ToManyField(SectorResource, 'sectors', full=True, null=True)
    titles = fields.ToManyField(TitleResource, 'iatiactivitytitle_set', full=True, null=True)
    descriptions = fields.ToManyField(DescriptionResource, 'iatiactivitydescription_set', full=True, null=True)
    collaboration_type = fields.ForeignKey(CollaborationTypeResource, attribute='collaboration_type', full=True, null=True)
    default_flow_type = fields.ForeignKey(FlowTypeResource, attribute='default_flow_type', full=True, null=True)
    default_finance_type = fields.ForeignKey(FinanceTypeResource, attribute='default_finance_type', full=True, null=True)
    default_aid_type = fields.ForeignKey(AidTypeResource, attribute='default_aid_type', full=True, null=True)
    default_tied_status_type = fields.ForeignKey(TiedAidStatusTypeResource, attribute='default_tied_status_type', full=True, null=True)
    activity_budgets = fields.ToManyField(ActivityBudgetResource, 'iatiactivitybudget_set', full=True, null=True)
    activity_transactions = fields.ToManyField(TransactionResource, 'iatitransaction_set', full=True, null=True)
    documents = fields.ToManyField(DocumentResource, 'iatiactivitydocument_set', full=True, null=True)
    statistics = fields.OneToOneField(ActivityStatisticResource, 'activitystatistics', full=True, null=True)

    class Meta:
        queryset = IATIActivity.objects.filter(is_active=True)
        resource_name = 'activities'
        max_limit = 100
        serializer = Serializer(formats=['xml', 'json'])
        excludes = ['date_created', 'is_active']
        ordering = ['start_actual', 'start_planned', 'end_actual', 'end_planned', 'activity_sectors', 'statistics']
        filtering = {
            'statistics': ALL_WITH_RELATIONS,
            'sectors': ALL,
            'iati_identifier': ALL
        }
        cache = NoTransformCache()

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(ActivityResource, self).apply_filters(request, applicable_filters)
        query = request.GET.get('query', None)
        sectors = request.GET.get('sectors', None)
        regions = request.GET.get('regions', None)
        countries = request.GET.get('countries', None)
        organisations = request.GET.get('organisations', None)
        filters = {}
        if sectors:
            # @todo: implement smart filtering with seperator detection
            sectors = sectors.replace('|', ' ').replace('-', ' ').split(' ')
            filters.update(dict(sectors__sector__code__in=sectors))
        if regions:
            # @todo: implement smart filtering with seperator detection
            regions = regions.replace('|', ' ').replace('-', ' ').split(' ')
            filters.update(dict(iatiactivityregion__region__code__in=regions))
        if countries:
            # @todo: implement smart filtering with seperator detection
            countries = countries.replace('|', ' ').replace('-', ' ').split(' ')
            filters.update(dict(iatiactivitycountry__country__iso__in=countries))
        if organisations:
            organisations = organisations.replace('|', ' ').split(' ')
            filters.update(dict(reporting_organisation__ref__in=organisations))
        if query:
            query_words = query.split(' ')
            query_countries = []
            for query_word in query_words:
                if query_word in COUNTRY_ISO_MAP.values() and not countries:
                    query_countries.append([item[0] for item in COUNTRY_ISO_MAP.items() if item[1] == query_word].pop())
            if query_countries:
                qset = (
                    Q(iatiactivitycountry__country__iso__in=query_countries, **filters) |
                    Q(iatiactivitytitle__title__icontains=query, **filters) |
                    Q(iatiactivitydescription__description__icontains=query, **filters)
                )
            else:
                qset = (
                    Q(iatiactivitytitle__title__icontains=query, **filters) |
                    Q(iatiactivitydescription__description__icontains=query, **filters)
                )
            return base_object_list.filter(qset).distinct()
        return base_object_list.filter(**filters).distinct()