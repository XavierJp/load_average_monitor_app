from django.conf.urls import patterns, include, url

urlpatterns = patterns('load_charts.views',
    url(r'^$', 'index'),
    url(r'^get-charts/$', 'get_charts_values'),
    url(r'^get-stats/$', 'get_updated_date'),
)
