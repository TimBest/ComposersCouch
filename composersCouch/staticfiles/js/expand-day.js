$(document).ready(function() {
    $(".expanded-day").hide();
    prev = null;
    $(".expand-day").click(function(e) {
        if (prev != null && prev.is($(this))) {
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
});
