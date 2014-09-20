from django.conf.urls import patterns, include, url
from hownewspaperswrite_app.views import home, testate, statistiche_generali, trends
from django.contrib.auth import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hownewspaperswrite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^testate/', testate),
    (r'^statistiche/', statistiche_generali),
    (r'^trends/', trends),
    (r'^$/', home),
    (r'', home),
)
