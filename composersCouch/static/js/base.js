$(document).ready(function() {
    $('#search').yourlabsAutocomplete({
        url: "/search/",
        placeholder: 'Search',
        choiceSelector: 'a',
    }).input.bind('selectChoice', function(e, choice, autocomplete) {
        document.location.href = choice.attr('href');
    });
});
