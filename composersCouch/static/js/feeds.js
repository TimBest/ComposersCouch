$(document).ready(function() {
  $('#availability-select').popover({
      html: true,
      placement: 'bottom',
      content: function () {
          return $('.availability-content').html();
      }
  });
  $('#zipcode-select').popover({
      html: true,
      placement: 'bottom',
      content: function () {
          return $('.zipcode-content').html();
      }
  });
  $('html').on('click', function (e) {
    $('[data-toggle="popover"]').each(function () {
      //the 'is' for buttons that trigger popups
      //the 'has' for icons within a button that triggers a popup
      if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
        $(this).popover('hide');
      }
    });
  });
  $('#availability-select').on('shown.bs.popover', function () {
      $(function () {
          $('#id_date').datetimepicker({pickTime: false});
      });
  })
  $('#zipcode-select').on('shown.bs.popover', function () {
        // TODO: get url with not so fancy javascript
        $('#div_id_zip_code').yourlabsWidget({
            autocompleteOptions: {
                url: '/autocomplete/ZipcodeAutocomplete/',
                choiceSelector: '[data-value]',
                placeholder: '',
            },
        });
  })
  $('.more-genres').hide();
  $('#load-more-genres').click(function(e) {
    e.stopPropagation();
    $('.more-genres').show();
    $('#load-more-genres').hide();
  });
});
