/*
This script enables ModelOrTextWidget, a widget for CharField that supports
autocomplete for comma-separated values.

It's organization is not final, there are a couple of things that are also used
in widget.js that will be re-factored probably in a script called lib.js.

The API however, is consistent with widget.js, and is not meant to change.

For now, the script is composed of these parts:

- a handful of jQuery extensions to ease treatment of comma separated values in
  an input,
- yourlabs.ModelOrTextWidget is stripped version of yourlabs.Widget, to handle the
  behavior of a comma separated autocompleted input,
- yourlabsModelOrTextWidget jQuery extension which role is to manage ModelOrTextWidget instances,
- yourlabsModelOrTextWidget initialization system, which supports dynamically added
  autocompletes (ie. admin inlines)
*/

jQuery.fn.getSelectionStart = function(){
    // Written by jQuery4U
    // http://www.jquery4u.com/snippets/6-jquery-cursor-functions/#.UDPQ9xXtFw8
    if(this.lengh == 0) return -1;
    input = this[0];
 
    var pos = input.value.length;
 
    if (input.createTextRange) {
        if (window.getSelection) {
            var r = window.getSelection(); //IE11
        } else {
            var r = document.selection.createRange().duplicate();
            r.moveEnd('character', input.value.length);
        }
        if (r.text === '')
            pos = input.value.length;
        pos = input.value.lastIndexOf(r.text);
    } else if(typeof(input.selectionStart)!="undefined")
    pos = input.selectionStart;
 
    return pos;
};

jQuery.fn.getCursorPosition = function(){
    // Written by jQuery4U
    if(this.lengh === 0) return -1;
    return $(this).getSelectionStart();
};

// Return the word on which the cursor is on.
//
// Consider the pipe "|" as an ASCII representation of the cursor, with such an
// input value::
//
//     foo, bar|, baz
//
// getCursorWord would return 'bar'.
jQuery.fn.getCursorWord = function() {
    var value = $(this).val();
    var positions = $(this).getCursorWordPositions();
    return value.substring(positions[0], positions[1]);
};

// Return the offsets of the word on which the cursor is on.
//
// Consider the pipe "|" as an ASCII representation of the cursor, with such an
// input value::
//
//     foo, bar|, baz
//
// getCursorWord would return [6, 8].
jQuery.fn.getCursorWordPositions = function() {
    var position = $(this).getCursorPosition();
    var value = $(this).val();
    var word = '';

    // find start of word
    for(var start=position - 1; start >= 0; start--) {
        if (value[start] == ',') {
            break;
        }
    }
    start = start < 0 ? 0 : start;

    // find end of word
    for(var end=position; end <= value.length - 1; end++) {
        if (value[end] == ',') {
            break;
        }
    }

    while(value[start] == ',' || value[start] == ' ') start++;
    while(value[end] == ',' || value[end] == ' ') end--;

    return [start, end + 1];
};

// ModelOrTextWidget ties an input with an autocomplete.
yourlabs.ModelOrTextWidget = function(input) {
    this.widget = input.closest('.form-group');
    this.input = this.widget.find('input[type=text]');
    this.checkbox = this.widget.find('input[type=checkbox]');
    this.checkbox.hide();
    this.deck = this.widget.find('.deck');
    if (this.deck.find('span').length !== 0) {
      this.input.val(this.deck.find('span[data-value]').attr('data-value'));
      this.checkbox.prop('checked', true);
      this.input.hide();
    }
    this.autocompleteOptions = {
        getQuery: function() {
            return this.input.getCursorWord();
        }
    };
};

// The widget is in charge of managing its Autocomplete.
yourlabs.ModelOrTextWidget.prototype.initializeAutocomplete = function() {
    this.autocomplete = this.input.yourlabsAutocomplete(
        this.autocompleteOptions);
    // Add a class to ease css selection of autocompletes for widgets
    this.autocomplete.box.addClass(
        'autocomplete-light-model-or-text-widget');
};

// Bind Autocomplete.selectChoice signal to ModelOrTextWidget.selectChoice()
yourlabs.ModelOrTextWidget.prototype.bindSelectChoice = function() {
    this.input.bind('selectChoice', function(e, choice) {
        if (!choice.length)
            return; // placeholder: create choice here

        $(this).yourlabsModelOrTextWidget().selectChoice(choice);
    });
};

// Called when a choice is selected from the Autocomplete.
yourlabs.ModelOrTextWidget.prototype.selectChoice = function(choice) {
    var value = this.getValue(choice);
    this.input.val(value);
    this.addToDeck(choice, value);
    this.input.hide();
    this.checkbox.prop('checked', true);

};

// Return the value of an HTML choice, used to fill the input.
yourlabs.ModelOrTextWidget.prototype.getValue = function(choice) {
    return choice.attr('data-value');
};

// Add a selected choice of a given value to the deck.
yourlabs.ModelOrTextWidget.prototype.addToDeck = function(choice, value) {
    var existing_choice = this.deck.find('[data-value="'+value+'"]');
    // Avoid duplicating choices in the deck.
    if (!existing_choice.length) {
        var deckChoice = this.deckChoiceHtml(choice);

        // In case getValue() actually **created** the value, for example
        // with a post request.
        deckChoice.attr('data-value', value);

        this.deck.append(deckChoice);
    }
};

// Called when the user clicks .remove in a deck choice.
yourlabs.ModelOrTextWidget.prototype.deselectChoice = function(choice) {
    choice.remove();
    this.input.val("");
    this.input.show();
    this.checkbox.prop('checked', false);
};

yourlabs.ModelOrTextWidget.prototype.deckChoiceHtml = function(choice, value) {
    var deckChoice = choice.clone();

    this.addRemove(deckChoice);

    return deckChoice;
};

yourlabs.ModelOrTextWidget.prototype.addRemove = function(choices) {
    var removeTemplate = this.widget.find('.remove:last')
        .clone().css('display', 'inline-block');

    var target = choices.find('.prepend-remove');

    if (target.length) {
        target.prepend(removeTemplate);
    } else {
        // Add the remove icon to each choice
        choices.prepend(removeTemplate);
    }
};

// Initialize the widget.
yourlabs.ModelOrTextWidget.prototype.initialize = function() {
    this.initializeAutocomplete();
    this.bindSelectChoice();
};

// Destroy the widget. Takes a widget element because a cloned widget element
// will be dirty, ie. have wrong .input and .widget properties.
yourlabs.ModelOrTextWidget.prototype.destroy = function(input) {
    input
        .unbind('selectChoice')
        .yourlabsAutocomplete('destroy');
};

// ModelOrTextWidget factory, registry and destroyer, as jQuery extension.
$.fn.yourlabsModelOrTextWidget = function(overrides) {
    var overrides = overrides ? overrides : {};

    if (overrides == 'destroy') {
        var widget = this.data('widget');
        if (widget) {
            widget.destroy(this);
            this.removeData('widget');
        }
        return
    }

    if (this.data('widget') === undefined) {
        // Instanciate the widget
        var widget = new yourlabs.ModelOrTextWidget(this);

        // Pares data-*
        var data = this.data();
        var dataOverrides = {
            autocompleteOptions: {
                // workaround a display bug
                minimumCharacters: 3,
                getQuery: function() {
                    // Override getQuery since we need the autocomplete to filter
                    // choices based on the word the cursor is on, rather than the full
                    // input value.
                    return this.input.getCursorWord();
                }
            }
        };
        for (var key in data) {
            if (!key) continue;

            if (key.substr(0, 12) == 'autocomplete') {
                if (key == 'autocomplete') continue;

                var newKey = key.replace('autocomplete', '');
                newKey = newKey.replace(newKey[0], newKey[0].toLowerCase())
                dataOverrides['autocompleteOptions'][newKey] = data[key];
            } else {
                dataOverrides[key] = data[key];
            }
        }

        // Allow attribute overrides
        widget = $.extend(widget, dataOverrides);

        // Allow javascript object overrides
        widget = $.extend(widget, overrides);

        this.data('widget', widget);

        // Setup for usage
        widget.initialize();

        // Widget is ready
        widget.input.attr('data-widget-ready', 1);
        widget.input.trigger('widget-ready');
    }

    return this.data('widget');
};

$(document).ready(function() {
    $('body').on('initialize', '.autocomplete-light-model-or-text-widget[data-widget-bootstrap=text]', function() {
        /*
        Only setup autocompletes on inputs which have
        data-widget-bootstrap=text, if you want to initialize some
        autocompletes with custom code, then set
        data-widget-boostrap=yourbootstrap or something like that.
        */
        $(this).yourlabsModelOrTextWidget();
    });
    // Call Widget.deselectChoice when .remove is clicked
    $('body').on('click', '.autocomplete-light-model-or-text-widget.deck .remove', function() {
        widget = $(this).closest('.form-group').find(
                '.autocomplete-light-model-or-text-widget[data-widget-bootstrap=text]'
            ).yourlabsModelOrTextWidget();

        var choice = $(this).parent();

        widget.deselectChoice(choice);
    });

    // Solid initialization, usage::
    //
    //      $(document).bind('yourlabsModelOrTextWidgetReady', function() {
    //          $('body').on('initialize', 'input[data-widget-bootstrap=text]', function() {
    //              $(this).yourlabsModelOrTextWidget({
    //                  yourCustomArgs: // ...
    //              })
    //          });
    //      });
    $(document).trigger('yourlabsModelOrTextWidgetReady');

    $('.autocomplete-light-model-or-text-widget:not([id*="__prefix__"])').each(function() {
        $(this).trigger('initialize');
    });

    $(document).bind('DOMNodeInserted', function(e) {
        var widget = $(e.target).find('.autocomplete-light-model-or-text-widget');

        if (!widget.length) {
            widget = $(e.target).is('.autocomplete-light-model-or-text-widget') ? $(e.target) : false;

            if (!widget) {
                return;
            }
        }

        // Ignore inserted autocomplete box elements.
        if (widget.is('.yourlabs-autocomplete')) {
            return;
        }

        // Ensure that the newly added widget is clean, in case it was cloned.
        widget.yourlabsWidget('destroy');
        widget.find('input').yourlabsAutocomplete('destroy');

        widget.trigger('initialize');
    });
});