from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url':'/tracks'}),
    url(r'^tracks', include('track_manager.urls', namespace="tracks", app_name="tracks")),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page' : '/login'}, name='logout')

    # Examples:
    # url(r'^$', 'cable_radio.views.home', name='home'),
    # url(r'^cable_radio/', include('cable_radio.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

