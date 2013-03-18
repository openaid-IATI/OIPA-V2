# Django specific
from django.conf.urls import *
from django.http import HttpResponseRedirect

# Tastypie specific
from tastypie.api import Api

# App specific
from api.v2.resources.model_resources import OrganisationResource
from api.v2.resources.model_resources import ActivityResource
from api.v2.resources.model_resources import ActivityListResource
from api.v2.resources.model_resources import ActivitySearchResource

from api.v2.resources.common_model_resources import CountryResource
from api.v2.resources.common_model_resources import RegionResource
from api.v2.resources.common_model_resources import SectorResource
from api.v2.resources.sub_model_resources import RecipientCountryResource, UnHabitatIndicatorCountryResource, UnHabitatIndicatorCityResource, OnlyCityResource, OnlyRegionResource, OnlyCountryResource

v2_api = Api(api_name='v2')
v2_api.register(OrganisationResource())
v2_api.register(ActivityResource())
v2_api.register(CountryResource())
v2_api.register(RegionResource())
v2_api.register(SectorResource())
v2_api.register(ActivityListResource())
v2_api.register(ActivitySearchResource())
v2_api.register(RecipientCountryResource(), canonical=True)
v2_api.register(UnHabitatIndicatorCountryResource(), canonical=True)
v2_api.register(UnHabitatIndicatorCityResource(), canonical=True)
v2_api.register(OnlyCountryResource())
v2_api.register(OnlyRegionResource())
v2_api.register(OnlyCityResource())





def api_v2_docs(request):
    return HttpResponseRedirect('/api/v2/docs/')

urlpatterns = patterns('',
    (r'^$', api_v2_docs),
    (r'^v2/$', api_v2_docs),
    url(r'^v2/docs/$', 'api.v2.views.docs_index', name='docs'),
    url(r'^v2/docs/getting-started/$', 'api.v2.views.docs_start', name='start_docs'),
    url(r'^v2/docs/resources/$', 'api.v2.views.docs_resources', name='resource_docs'),
    url(r'^v2/docs/filtering/$', 'api.v2.views.docs_filtering', name='filter_docs'),
    url(r'^v2/docs/ordering/$', 'api.v2.views.docs_ordering', name='ordering_docs'),
    url(r'^v2/docs/about/$', 'api.v2.views.docs_about', name='about_docs'),
    (r'', include(v2_api.urls)),
)