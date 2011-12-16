/* Author:

*/


$(function(){
    changed_flag = false;
    function set_changed_flag(value) {
        changed_flag = value;
    }
    var set_total_duration = function() {
        duration = 0.0;
        $("#playlist > li").each(function(){
           duration += parseFloat($(this).attr("data-duration"));
        });
        var base = $("#playlist_total_duration");
        base.attr('data-total-duration', duration);
    }
    var update_total_duration = function(duration) {

        var base = $("#playlist_total_duration");
        var total_duration = parseFloat(base.attr('data-total-duration'));;

        var hours = Math.floor(total_duration / 3600);
        total_duration = total_duration - (3600*hours);

        var minutes = Math.floor(total_duration / 60);
        total_duration = total_duration - (60*minutes);

        var seconds = total_duration;

        minutes = minutes < 10 ? "0"+minutes : ""+minutes;
        seconds = seconds < 10 ? "0"+seconds : ""+seconds;
        var base = $("#playlist_total_duration").children('em').html(hours+":"+minutes+":"+seconds);
    }

    $(window).bind('beforeunload', function(){
        if (changed_flag) {
            return 'Are you sure?';
        }
    })

    $('#playlist').sortable({
        opacity: 0.5,
        revert: true,
        stop: function(){
            set_changed_flag(true);

            set_total_duration();
            update_total_duration(duration);
        }
    });

    $('#tracklist > li').draggable({
       connectToSortable: '#playlist',
       helper: 'clone',
       revert: 'invalid'
       });

    $('a#save_playlist').click(function(){
        var playlist = []
        var songOrder = $('#playlist > li')
        songOrder.each(function(){
            playlist.push("order="+$(this).attr('data-song-id'))
        });
        playlist = playlist.join('&')
        $.ajax($(this).attr('href'),{
            data: playlist,
            headers: {'X-CSRFToken' : $('meta[name=csrf_token]').attr('content')},
            type: 'POST',
            complete: function(){
                set_changed_flag(false);

            }
        });
        return false;
    })

    $("#playlist li.remove").live("click", function(){
        var item = $(this).parents('li.song');
        $(this).parent().remove()
        item.slideUp(function(){
            item.remove();
            set_total_duration();
            update_total_duration();
        })
        set_changed_flag(true);


    })
    update_total_duration();
})

