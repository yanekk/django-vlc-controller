#!/usr/bin/env python
from django.core.management import execute_manager
import sys
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    if '--vlc-command' in sys.argv:
        print 'nohup vlc {0} "file://{1}playlist.m3u" &'.format(settings.CR_VLC_PARAMETERS, settings.CR_PLAYLIST_DIR.replace(' ', '%20'))
        exit()
    execute_manager(settings)

