from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'track_manager.views.main', name='main'),
    url(r'^/refresh$', 'track_manager.views.refresh', name='refresh'),
    url(r'^/update$', 'track_manager.views.update', name='update'),
    url(r'^/console$', 'track_manager.views.console', name='console'),
    url(r'^/change-colour$', 'track_manager.views.change_colour', name='change-colour'),
)

