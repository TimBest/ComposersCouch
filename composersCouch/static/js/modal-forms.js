
function modalConnect(modalTriger, modalForm, deleteTriger) {
    // unbind the click to prevent multiple click event bindings, since binding is done after each ajax call.
    $(modalTriger).unbind('click');
    $(modalTriger).click(function(e) {
        e.preventDefault();
        modalTriger = $(this).attr('href');
        getForm(modalTriger, modalForm, deleteTriger);
    });
}
function getForm(url, modalForm, deleteTriger) {
    $.get(
        url,
        function(results){
          var form = $(modalForm, results);
          $('.modal').html(form).modal('show');
          $(document).ready(function () {
              // bind submit, add, and delete to an AJAX action
              bindModalEvents(url, modalForm, deleteTriger);
          });
        }, "html");
        // prevents the click propagation
        return false;
}

function bindModalEvents(url, modalForm, deleteTriger){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    deleteObject(url, modalForm, deleteTriger);
    saveForm(url, modalForm, deleteTriger);
}
function saveForm(url, modalForm, deleteTriger){
    //bind the form. prevent default behavior and submit form via ajax instead
    $(modalForm).submit(function(e){
        /* quick hack to fix autocomplete issues */
        zipcode_fix();
        e.preventDefault();
        $.ajax({
          type: $(this).attr('method'),
          url: $(this).attr('action'),
          data: new FormData(this),
          processData: false,
          contentType: false,
          success:function(response, textStatus, jqXHR){
              var form = $(modalForm, response);
              if (form.html()) {
                  // form is invalid update modal with the response
                  $('.modal').html(form).modal('show');
                  // rebind submit button
                  saveForm(url, modalForm, deleteTriger);
              }
              else {
                  // form is valid load the response
                  var addMore = false;
                  var $btn = $(document.activeElement);
                  if (
                      // there is an activeElement at all
                      $btn.length &&
                      // it's a child of the form
                      $(modalForm).has($btn) &&
                      // it's really a submit element
                      $btn.is('button[type="submit"], input[type="submit"], input[type="image"]')
                  ) {
                      var classList =$btn.attr('class').split(/\s+/);
                      $.each( classList, function(index, item){
                          if (item === 'addMore') {
                             addMore = true;
                          }
                      });
                  }
                  if (addMore == true) {
                      getForm(url, modalForm, deleteTriger)
                  } else {
                      document.open();
                      document.write(response);
                      document.close();
                  }


              }
          },
          error: function (request, status, error) {
              //TODO: implament error handling
          }
        });
        return false;
    });
}
function deleteObject(url, modalForm, deleteTriger) {
    $(deleteTriger).unbind('click');
    $(deleteTriger).click(function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('href'),
            type: 'DELETE',
            success: function(response, status, request) {
                //needs to update the form
                getForm(url, modalForm, deleteTriger);
            }
        });
      return false;
    });
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
