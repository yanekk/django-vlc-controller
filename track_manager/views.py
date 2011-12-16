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
    tracklist = Track.objects.order_by('name')

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
    playlist = PlaylistElement.objects.all().delete()
    for position, track_id in enumerate(request.POST.getlist('order')):
        track = Track.objects.get(pk=int(track_id))
        playlistElement = PlaylistElement.objects.create(position=position, track=track)
        playlistElement.save()

    # UPDATE PLAYLIST
    playlist = [item.track for item in PlaylistElement.objects.all().order_by('position').select_related()]

    playlist_file = open(settings.CR_PLAYLIST_DIR+"playlist.m3u", "w");
    for track in playlist:
        playlist_file.write('{0}\n'.format(track.path.decode('utf-8')))
    playlist_file.close()

    # CONNECT WITH VLC AND PLAY THE PLAYLIST
    try:
        VLCController.update_and_play(settings.CR_PLAYLIST_DIR+"playlist.m3u")
    except socket.error:
        VLCController.run(settings.CR_PLAYLIST_DIR+"playlist.m3u", settings.CR_VLC_PARAMETERS)


    return HttpResponse(json.dumps({'result':'ok'}), mimetype="application/json")

@login_required
def console(request):
    console = VLCController()
    if (request.method == 'POST'):
        error = None;
        output = None;
        try:
            console.handshake()
            output = console.command(request.POST['command'].encode('utf-8')).split("\n")[:-1]
            console.close()
        except socket.error:
            error = str(sys.exc_info()[1])

        results = {
            'status' : ('error' if error else 'ok'),
            'output' : (('### ERROR ###',error,'### ERROR ###') if error else output)
                }
        return HttpResponse(json.dumps(results), mimetype="application/json")
    else:

        try:
            output = console.handshake().split("\n")[:-1]
        except socket.error:
            VLCController.run(settings.CR_PLAYLIST_DIR+"playlist.m3u", settings.CR_VLC_PARAMETERS)
            time.sleep(1)
            output = console.handshake().split("\n")[:-1]

        console.close()

        variables = {'section':'console', 'title' : "VLC Console", 'output' : output}

        return render_to_response('console.html', variables, context_instance=RequestContext(request))

