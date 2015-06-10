function expand_day() {
    $(".expanded-day").hide();
    prev = null;
    $(".expand-day").click(function(e) {
        if (prev !== null && prev.is($(this))) {
            $(this).closest(".week").find(".expanded-day").toggle();
        } else {
            prev = $(this);
            expanded_day = $(".expanded-day").hide();
            expanded_day = $(this).closest(".week").find(".expanded-day").show();
            events = $(this).find(".events").clone();
            links = $(this).find(".links").clone();
            event_list = expanded_day.find(".event-list");
            event_list.empty();
            event_list.append(events);
            link_list = expanded_day.find(".link-list");
            link_list.empty();
            link_list.append(links);
        }
    });
}

//Show Participants
function show_participants(id, choice_class, plural) {
    $("#div_"+id).hide();
    // get initial data
    $("#div_"+id+" ."+choice_class+" .remove").replaceWith(
        "<button class='btn btn-link remove' type='button'><span class='fa fa-times-circle text-muted'></span></button>"
    );
    $("#div_"+id+"_text .controls").prepend(
        $("#div_"+id+" #"+id+"-deck").html()
    );

    $("#"+id+"_text").yourlabsAutocomplete({
    }).input.bind('selectChoice', function(e, choice, autocomplete) {
        var value = $("#div_"+id+"_text .hilight").attr("data-value");
        // if no selection then add on else remove old selection then add new one
        if (plural === true) {
            // if no selection then add on
            $("#"+id).append("<option value='"+value+"' selected='selected'>"+value+"</option>");
        } else {
            if ($("#"+id+" option:selected").length===0) {
                $("#"+id+"").append("<option value='"+value+"' selected='selected'>"+value+"</option>");
            } else {
                $("#"+id+" option").replaceWith("<option value='"+value+"' selected='selected'>"+value+"</option>");
                $("#"+id+" option[data-value="+value+"]").remove();
                $("#div_"+id+"_text ."+choice_class).remove();
            }
        }

        // display to user whom they selected
        $("#div_"+id+"_text .controls").prepend(
          "<div class='"+choice_class+"' data-value="+value+">"+
            "<button class='btn btn-link remove' type='button'><span class='fa fa-times-circle text-muted'></span></button>"+
            $(choice).html()+
          "</div>"
        );
    });
    // remove selection display and value
    $("#div_"+id+"_text").on("click", ".remove", function() {
      if (plural === true) {
          value = $(this).parent().attr("data-value");
          $("#"+id+" option[value="+value+"]").remove();
          name = $(this).parent().find(".artist-name").text();
          choices = $("#"+id+"_text").val();
          choices = choices.replace(name, "");
          $("#"+id+"_text").val(choices);
          $(this).parent().remove();
      } else {
          // remove selection display and value
          $("#"+id+" option").remove();
          $(this).parent().remove();
          $("#"+id+"_text").val('');
      }
    });
}

$(document).ready(function() {
    // Allows day events to be show with more info below the current week
    expand_day();
    // copy autocomplete field data into/outof the text field
    var eventForm = $("#eventForm");
    if (eventForm.length > 0) {
      show_participants("id_headliner", "artist-autocomplete", false);
      show_participants("id_venue", "user-autocomplete", false);
      show_participants("id_openers", "artist-autocomplete", true);
    }
});
