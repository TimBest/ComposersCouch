

$(document).ready(function() {
  // hide text input
  $('input[title=model-or-text-widget-text-input]').hide();

  // copy values form model input to text input on submit
  $('button[type=submit]').click(function() {
    $(this).closest('form').find('input[title=model-or-text-widget-model-input]').each(function() {

      var model_input = $(this);
      var widget = model_input.closest('.form-group');
      var deck = widget.find('.deck');
      var text_input = widget.find('input[title=model-or-text-widget-text-input]');

      var value = "";

      if (deck.find('span').length !== 0) {
        value = deck.find('span[data-value]').attr('data-value');
      } else {
        value = model_input.val();
      }

      text_input.val(value);

    });
  });
});
