(function() {

function open_global_modal_overlay(message) {
    $('#global-modal-overlay-content').text(message);
    $('#global-modal-overlay').addClass('is-active');
}


function close_global_modal_overlay() {
    $('#global-modal-overlay').removeClass('is-active');
}


function form_message_failure(formId, message) {
    // create message box, prepend it before form and scroll to it
    var msgElId = formId + '-failure-msg';
    var msgEl = $('#' + msgElId);
    if (msgEl.length == 0) {
        var msgEl = $('<article class="message is-warning" id="' + msgElId + '"><div class="message-body">xxx</div></article>');
    }
    var bodyEl = msgEl.find('.message-body');
    bodyEl.text(message);
    var form = $('#' + formId);
    msgEl.insertBefore(form);
}

window.submit_ajax_form = function (formId) {
    open_global_modal_overlay('Sending form, please wait.');
    var form = $('#' + formId);

    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        dataType: 'json',
        success: function(json) {
            close_global_modal_overlay();
            form.find('.pkih-form-error-block').remove();  // clear all error blocks
            if (json.success) {
                window.location.href(success.redirect);
            } else {
                // parse error messages
                let fieldErrorBlocks = {};
                $.each(json.errors, function(_index, item) {
                    var fieldName = item.field;
                    if (!fieldErrorBlocks[fieldName]) {
                        let fieldEl = $('#' + item.field_id);
                        let fieldBlock = fieldEl.closest('div.field');
                        let fieldErrorEl = $('<p class="help is-danger pkih-form-error-block"></p>');
                        fieldBlock.append(fieldErrorEl);
                        fieldErrorBlocks[fieldName] = fieldErrorEl;
                    }
                    var errorEl = $('<p></p>').text(item.error_text);
                    fieldErrorBlocks[fieldName].append(errorEl);
                });
                form_message_failure(formId, 'Form processing error.');
            }
        },
        error: function(jqXHR, textStatus) {
            close_global_modal_overlay();
            form_message_failure(formId, 'Server query failed.');
        }
    });
}


window.data_destroy_element = function(self) {
    var a = $(self).attr('data-target-id');
    var el = $('#' + a);
    el.remove();
}

})();
