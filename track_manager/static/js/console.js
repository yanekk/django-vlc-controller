$(function(){
    var add_output = function(content, error) {
        var base = $("#console_input");
        var console_output = $("#console_output");

        var output = $("<li>");
        if (error) {
            output.addClass('error');
        }

        console_output.append(output.html(content));
        console_output.parent().scrollTop(console_output.height());

        base.attr("disabled", false);
        base.val('');
        base.focus();
    }
    var forbidden_commands = ["shutdown", "logout", "quit"]

    $("#console_input").focus();
    $("#console_input").keypress(function(event){
        base = $(this);
        if(event.keyCode == 13) {
            var command = $.trim($("#console_input").val());

            if (command) {
                base.attr("disabled", true);
                if (forbidden_commands.indexOf(command) > -1) {
                    add_output('Command "'+command+'" is forbidden via web console.', true);
                    return false;
                }

                var console_output = $("#console_output");
                $.ajax('/console',{
                    data: "command="+escape(command),
                    headers: {'X-CSRFToken' : $('meta[name=csrf_token]').attr('content')},
                    type: 'POST',
                    success: function(data, status){
                        var result = data.output.join('<br >');
                        error = false;
                        if(result.status == 'error') {
                            error = true;
                        }
                        add_output(result, error);

                    },
                    dataType: 'json'
                });
            }
        }
    })
})

