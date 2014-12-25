from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.rainmap.views',
    url(r'^new/', 'scan_new', {'template': 'rainmap/scan_new.html'}, name='rainmap_scan_new'),
    url(r'^edit/(?P<scan_id>\d+)/$', 'scan_edit', {'template': 'rainmap/scan_edit.html'}, name='rainmap_scan_edit'),
    url(r'^run/(?P<scan_id>\d+)/$', 'scan_run', {'template': 'rainmap/scan_list.html'}, name='rainmap_scan_run'),
    url(r'^copy/(?P<scan_id>\d+)/$', 'scan_copy', {'template': 'rainmap/scan_list.html'}, name='rainmap_scan_copy'),
    url(r'^delete/(?P<scan_id>\d+)/$', 'scan_delete', {'template': 'rainmap/scan_list.html'}, name='rainmap_scan_delete'),
    url(r'^view/(?P<scan_id>\d+)/$', 'scan_view', {'template': 'rainmap/scan_view.html'}, name='rainmap_scan_view'),
    url(r'^results/(?P<result_id>\d+)/$', 'result_view', {'template': 'rainmap/result_view.html'}, name='rainmap_result_view'),
    url(r'^results/delete/(?P<result_id>\d+)/$', 'result_delete', {'template': 'rainmap/result_delete.html'}, name='rainmap_result_delete'),
    url(r'^$', 'scan_list', {'template': 'rainmap/scan_list.html'}, name='rainmap_scan_list'),
)
