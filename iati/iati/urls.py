# Django specific
from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from iati.search_sites import PeriodicalSearchView

from api.v2.urls import api_v2_docs

from utils.views import UploadUnHabitatIndicatorCountryCSV

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^$', api_v2_docs),
    url(r'^upload-data$', UploadUnHabitatIndicatorCountryCSV.as_view(), name="upload_data"),
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