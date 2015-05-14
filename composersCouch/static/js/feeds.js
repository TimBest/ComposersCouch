$(document).ready(function() {
    $('.more-genres').hide();
    $('#load-more-genres').click(function(e) {
        e.stopPropagation();
        $('.more-genres').show();
        $('#load-more-genres').hide();
    });
});
