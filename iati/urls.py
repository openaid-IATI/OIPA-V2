# Django specific
from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from api.v2.urls import api_v2_docs


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^$', api_v2_docs),

    (r'^api/', include('api.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() #this serves static files and media files.
    #in case media is not served correctly
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )