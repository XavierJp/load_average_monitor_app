from django.conf.urls import patterns, include, url

urlpatterns = patterns('load_charts.views',
    url(r'^$', 'index'),
    url(r'^test-get/$', 'test_get'),
)
