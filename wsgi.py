import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'cable_radio.settings'
sys.path.append(sys.path[0]+'/cable_radio')
print sys.path
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

