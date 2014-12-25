from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from rainmap import settings
from apps.rainmap.views import profile

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^profile/', profile, {'template': 'rainmap/profile.html'}, name='user_profile'),
    (r'^scans/', include('apps.rainmap.urls')),
    url(r'^$', 'apps.rainmap.views.index', name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^storage/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.OUTPUT_ROOT}),
        url(r'^(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
)
