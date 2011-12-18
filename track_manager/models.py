# -*- coding: utf-8 -*-

from django.db import models
from glob import glob

import settings, os

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
# Create your models here.


class Track(models.Model):
    path = models.TextField()
    duration = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    colour = models.CharField(max_length=6, default='eee')
    not_found = models.BooleanField(default=False)

    album = models.CharField(max_length=255, null=True)
    track_number = models.IntegerField(null=True)
    artist = models.CharField(max_length=255, null=True)
    title  = models.CharField(max_length=255, null=True)

    def fetch_info(self):
        print u"Fetching metadata for {0}".format(self.path)
        metadata      = MP3(self.path, ID3=EasyID3)

        self.duration = round(metadata.info.length, 2)
        self.artist       = metadata['artist'][0]
        self.title        = metadata['title'][0]
        self.album        = metadata['album'][0]
        self.track_number = int(metadata['tracknumber'][0].split('/')[0])


    def background_colour(self):
        if self.not_found:
            return 'F00'
        return self.colour

    def status(self):
        if self.not_found:
            return "File not found"
        return "OK"

    def name(self):
        if (self.artist and self.title):
            return u"{0} - {1}".format(self.artist, self.title)
        else:
            return os.path.basename(self.path)

    @classmethod
    def refresh(cls):
        db_tracks = Track.objects.all()
        all_tracks = {}

        for track in db_tracks:
            all_tracks[track.path] = track

        file_tracks = glob(u"{0}/**/*.mp3".format(settings.CR_MUSIC_WATCH_DIR))
        for track_path in file_tracks:

            if track_path in all_tracks.keys():
                print "Updating existing track..."
                track = all_tracks[track_path]
                track.not_found = False
                track.fetch_info()
                track.save()

                del all_tracks[track.path]

            else:
                print "Creating new track..."
                track = Track()
                track.path = track_path

                track.fetch_info()
                track.save()

                if track.path in all_tracks:
                    del all_tracks[track.path]

        for key, value in all_tracks.items():
            value.playlistelement_set.all().delete()
            value.delete()

    def duration_time(self):
        duration = int(self.duration)
        minutes = duration/60
        seconds = duration % 60
        return "{0}:{1}".format(minutes, (seconds if seconds >= 10 else "0"+str(seconds)))

    def __unicode__(self):
        return self.name

class PlaylistElement(models.Model):
    track = models.ForeignKey(Track)
    position = models.IntegerField()

