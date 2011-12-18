
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
        axis: 'y',
        forcePlaceHolderSize: true,
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

    $('.minimenu-opener').click(function(){
        var base = $(this);
        base.toggleClass('open');
        base.siblings('.minimenu').toggle();
        return false;
    });
    $('.colour-changer select').change(function(){
        var base = $(this);
        var form = base.parents('form')
        var item = base.parents('li.song')
        var song_id = form.children('input[name=song_id]').val();

        $('.song-'+song_id).css('background-color', '#'+base.val());

        $.ajax(form.attr('action'),{
            data: form.serialize(),
            headers: {'X-CSRFToken' : $('meta[name=csrf_token]').attr('content')},
            type: 'POST',
            dataType: 'json',
            success: function(data, status){
                if(data.status == 'error') {
                    alert(data.content);
                }
            }
        });
    })
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
            dataType: 'json',
            success: function(data, status){
                set_changed_flag(false);
                if(data.status == 'error') {
                    alert(data.content);
                }
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

