# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from track_manager.models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Fetch MP3s from given path
        """
        Track.refresh()
        Track.refresh()

