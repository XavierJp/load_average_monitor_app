from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monitor_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='/load_charts/')),
    url(r'^load_charts/', include('load_charts.urls')),
)
