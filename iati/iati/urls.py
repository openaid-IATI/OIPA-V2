# Django specific
from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from iati.search_sites import PeriodicalSearchView

from api.v2.urls import api_v2_docs

from utils.views import UploadUnHabitatIndicatorCountryCSV, test_json_response, test_json_city_response, json_cpi_filter_response, json_activities_response, json_filter_projects

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^$', api_v2_docs),
    url(r'^upload-data$', UploadUnHabitatIndicatorCountryCSV.as_view(), name="upload_data"),
    url(r'^json$', test_json_response , name="json_test"),
    url(r'^json-city$', test_json_city_response , name="json_city_test"),
    url(r'^json-filter-cpi$', json_cpi_filter_response , name="json_filter_cpi"),
    url(r'^json-activities$', json_activities_response, name='json_activities'),
    url(r'^json-project-filters', json_filter_projects, name='json_project_filters'),


    (r'^api/', include('api.urls')),
    url(r'^search/$', PeriodicalSearchView(template='search/search.html'),
        name='haystack_search'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() #this serves static files and media files.
    #in case media is not served correctly
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )