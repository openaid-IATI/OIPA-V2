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
import pdb
from data.models.activity import IATIActivity, IATIActivityTitle
from data.models.common import Population
from data.models.constants import COUNTRY_ISO_MAP
from data.models.organisation import Organisation, ParticipatingOrganisation

# App specific
from api.v2.resources.common_model_resources import ActivityStatisticResource, OrganisationStatisticsResource
from api.v2.resources.common_model_resources import DescriptionResource
from api.v2.resources.common_model_resources import TitleResource
from api.v2.resources.sub_model_resources import RecipientCountryResource, UnHabitatDemoGraphicResource
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

from haystack.query import SearchQuerySet
from django.conf.urls.defaults import *
from tastypie.utils import trailing_slash
from django.core.paginator import Paginator, InvalidPage


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

    def dehydrate(self, bundle):
        bundle.data['type'] = bundle.obj.get_type_display()
        return super(OrganisationResource, self).dehydrate(bundle)


class ParticipatingOrganisationResource(ModelResource):
    """
    Resource for IATI ParticipatingOrganisations
    """
    class Meta:
        queryset = ParticipatingOrganisation.objects.all()
        fields = ['ref', 'org_name', 'role', 'type']
        include_resource_uri = False

class ActivityListResource(ModelResource):
    """
    Resource copied from ActivityResource with less attributes to increase result speed
    """

    recipient_country = fields.ToManyField(RecipientCountryResource, 'iatiactivitycountry_set', full=True, null=True)
    unhabitat_indicators = fields.ToManyField(UnHabitatDemoGraphicResource, attribute=lambda bundle: Population.objects.filter(country=ActivityListResource.get_country(bundle)).order_by('year'), full=True, null=True)

    activity_sectors = fields.ToManyField(SectorResource, 'sectors', full=True, null=True)
    titles = fields.ToManyField(TitleResource, 'iatiactivitytitle_set', full=True, null=True)
    descriptions = fields.ToManyField(DescriptionResource, 'iatiactivitydescription_set', full=True, null=True)
    recipient_region = fields.ToManyField(RecipientRegionResource, 'iatiactivityregion_set', full=True, null=True)
    activity_sectors = fields.ToManyField(SectorResource, 'sectors', full=True, null=True)
    statistics = fields.OneToOneField(ActivityStatisticResource, 'activitystatistics', full=True, null=True)

    @staticmethod
    def get_country(bundle):
        try:
            country = bundle.obj.iatiactivitycountry_set.values('country__pk').all()
            return country
        except:
            return None


    class Meta:
        queryset = IATIActivity.objects.filter(is_active=True)
        resource_name = 'activity-list'
        max_limit = 100
        serializer = Serializer(formats=['xml', 'json'])

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(ActivityListResource, self).apply_filters(request, applicable_filters)
        query = request.GET.get('query', None)
        sectors = request.GET.get('sectors', None)
        regions = request.GET.get('regions', None)
        countries = request.GET.get('countries', None)
        organisations = request.GET.get('organisations', None)

#        organisations = request.GET.get('organisations', None)
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
    unhabitat_indicators = fields.ToManyField(UnHabitatDemoGraphicResource, attribute=lambda bundle: Population.objects.filter(country__pk__in=ActivityListResource.get_country(bundle)).order_by('country', 'year',), full=True, null=True)


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


class ActivitySearchResource(ModelResource):
    """
    This resource is now for example purposes, when we decide to use the search platform Haystack with engine Haystack

    This is resource could be requested: http://__url__api__engine/api/v2/activity-search/search/?format=json&q=mozambique
    This resource usages the search engine Haystack, it will request Haystack. Check search engine indexing what has been added to the
    index: iati/search_sites.py

    #todo: create a denormalized resource with all necessary attributes to return faster results.
    """
    class Meta:
        queryset = IATIActivity.objects.all()
        resource_name = 'activity-search'
        max_limit = 100
        serializer = Serializer(formats=['json', 'xml'])

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % ('activity-search', trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            ]


    def get_search(self, request, **kwargs):
#        self.method_check(request, allowed=['get'])
#        self.is_authenticated(request)
#        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(IATIActivity).load_all().auto_query(request.GET.get('q', ''))

        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            #create a result object bundle from the Activity bundle
#            bundle = self.build_bundle(obj=result.object, request=request)
#            bundle = self.full_dehydrate(bundle)
            #creating a result from the stored fields from the search engine
            fields = result.get_stored_fields()

            #we can add fields on the fly, only problem is that this will hit the database, and is causing performance
            try:
                fields['sector'] = result.object.sectors.all()[0].sector.name
            except IndexError:
                fields['sector'] = 'N/A'
            fields['id'] = result.object.pk
            objects.append(fields)

        object_list = {
            'objects': objects,
            }

#        self.log_throttled_access(request)
        return self.create_response(request, object_list)