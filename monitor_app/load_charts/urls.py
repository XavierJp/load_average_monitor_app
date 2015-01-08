from django.conf.urls import patterns, include, url

urlpatterns = patterns('load_charts.views',
    url(r'^$', 'index'),
)
