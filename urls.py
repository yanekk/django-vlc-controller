from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url':'/tracks'}),
    url(r'^tracks$', 'track_manager.views.main'),
    url(r'^tracks/refresh$', 'track_manager.views.refresh'),
    url(r'^tracks/update$', 'track_manager.views.update'),
    url(r'^console$', 'track_manager.views.console'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page' : '/login'})

    # Examples:
    # url(r'^$', 'cable_radio.views.home', name='home'),
    # url(r'^cable_radio/', include('cable_radio.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

