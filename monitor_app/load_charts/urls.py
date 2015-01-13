from django.conf.urls import patterns, include, url

urlpatterns = patterns('load_charts.views',
    url(r'^$', 'index'),
    url(r'^charts-get/$', 'charts_get'),
    url(r'^check-alerts/$', 'check_alerts'),
)
