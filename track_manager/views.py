# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from models import *
from vlc import VLCController
import json, telnetlib, socket, time, sys

@login_required
def main(request):
    playlist = PlaylistElement.objects.all().order_by('position').select_related()
    playlist = [item.track for item in playlist]
    #playlist.append(PlaylistElement())
    tracklist = Track.objects.order_by('artist','album','track_number')

    total_duration = 0
    for item in playlist:
        total_duration += item.duration


    variables = {
                    'playlist' : playlist,
                    'tracklist': tracklist,
                    'section'  : 'track_manager',
                    'title'    : 'Track Manager',
                    'total_duration' : total_duration}

    return render_to_response('main.html', variables, context_instance=RequestContext(request))

@login_required
def refresh(request):
    Track.refresh()
    return redirect('/tracks')

@login_required
def update(request):
    error = None
    playlist = PlaylistElement.objects.all().delete()
    for position, track_id in enumerate(request.POST.getlist('order')):
        track = Track.objects.get(pk=int(track_id))
        playlistElement = PlaylistElement.objects.create(position=position, track=track)
        playlistElement.save()

    # UPDATE PLAYLIST
    playlist = [item.track for item in PlaylistElement.objects.all().order_by('position').select_related()]

    playlist_file = open(settings.CR_PLAYLIST_DIR+"playlist.m3u", "w");
    for track in playlist:
        playlist_file.write('{0}\n'.format(track.path.encode('utf-8')))
    playlist_file.close()

    # CONNECT WITH VLC AND PLAY THE PLAYLIST
    try:
        VLCController.update_and_play(settings.CR_PLAYLIST_DIR+"playlist.m3u")
    except socket.error:
        error = "VLC is not running, playlist cannot be updated."

    results = {
        'status'  : ('error' if error else 'ok'),
        'content' : error
    }
    return HttpResponse(json.dumps(results), mimetype="application/json")

@login_required
def console(request):
    console = VLCController()
    error = None;
    output = None;
    try:
        output = console.handshake().split("\n")[:-1]
        if (request.method == 'POST'):
            output = console.command(request.POST['command'].encode('utf-8')).split("\n")[:-1]
        console.close()

    except socket.error:
        error = "VLC is not running, run VLC via SSH."


    results = {
        'status' : ('error' if error else 'ok'),
        'output' : (('### ERROR ###',error,'### ERROR ###') if error else output),
            }

    if (request.method == 'POST'):
        return HttpResponse(json.dumps(results), mimetype="application/json")
    else:
        results['section'] = 'console'
        results['title'] = 'VLC Console'
        return render_to_response('console.html', results, context_instance=RequestContext(request))

@login_required
def change_colour(request):
    error = None
    results = {'status' : 'ok'}
    try:
        song_id = int(request.POST['song_id'])
        track = Track.objects.get(pk=song_id);
        track.colour = request.POST['colour']
        track.save()
        if not track:
            raise Exception("Track with id #{0} doesn't exist.".format(song_id))
    except:
        results['status']  = 'error'
        results['content'] = "{0} - {1}".format(sys.exc_info[0], sys.exc_info[1])

    return HttpResponse(json.dumps(results), mimetype="application/json")

