(function() {

function open_global_modal_overlay(message)
{
    $('#global-modal-overlay-content').text(message);
    $('#global-modal-overlay').addClass('is-active');
}


function close_global_modal_overlay()
{
    $('#global-modal-overlay').removeClass('is-active');
}


function confirmation_modal_dialog(text, cb, yesTitle, cancelTitle)
{
    if (!yesTitle) {
        yesTitle = 'Yes, delete';
    }
    if (!cancelTitle) {
        cancelTitle = 'Cancel';
    }
    // create confirmation modal box
    var confirmationEl = $('<div class="modal is-active pkih-modal-esc-close"><div class="modal-background"></div><div class="modal-card"><header class="modal-card-head"></header><section class="modal-card-body"><div class="confirmation-text"></div></section><footer class="modal-card-foot"><button class="button is-info pkih-yes"></button> <button class="button pkih-cancel"></button></footer></div></div>');
    confirmationEl.find('.confirmation-text').text(text);
    confirmationEl.find('.pkih-yes').text(yesTitle);
    confirmationEl.find('.pkih-cancel').text(cancelTitle);


    var bodyEl = $('body');

    bodyEl.append(confirmationEl);

    confirmationEl.find('.modal-background, .pkih-cancel').on('click', function() {
        confirmationEl.remove();
    });
    confirmationEl.find('.pkih-yes').on('click', function() {
        cb(function() {
            confirmationEl.remove();
        });
    });
}

function form_message_failure(formId, message)
{
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
                window.location.href = json.redirect;
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


window.data_destroy_element = function(self)
{
    var a = $(self).attr('data-target-id');
    var el = $('#' + a);
    el.remove();
}


window.grid_delete_selected = function(tableId)
{
    var table = $('#' + tableId).first();
    var checkedIds = [];
    table.find("input[type='checkbox']").each(function(_index, item) {
        if (item.checked) {
            checkedIds.push(item.getAttribute('value'));
        }
    });
    if (!checkedIds.length) {
        return;
    }

    confirmation_modal_dialog('Delete selected items?', function(closeModalFn) {
        $.ajax({
            type: 'POST',
            url: table.attr('data-url'),
            traditional: true,
            data: {
                csrfmiddlewaretoken: table.attr('data-csrf-token'),
                ids: checkedIds
            },
            success: function() {
                location.reload();
            },
            error: function() {
                closeModalFn();
            }
        });
    });
}


window.do_logout = function(csrfToken)
{
    $.ajax({
        type: 'POST',
        url: '/accounts/logout',
        traditional: true,
        data: {
            csrfmiddlewaretoken: csrfToken,
        },
        success: function() {
            location.reload();
        },
        error: function() {
        }
    });
}


// add event listener to close all modal marked as "pkih-modal-esc-close"
$(document).ready(function() {
    $('.dropdown-trigger').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).closest('.dropdown').toggleClass('is-active');
    });
    $('body').on('click', function() {
        let dropdowns = $('.dropdown');
        if (dropdowns.length) {
            dropdowns.removeClass('is-active');
        }
    });
    $(this).keydown(function(e) {
        if (e.keyCode == 27) {  // Esc
            let dropdowns = $('.dropdown');
            if (dropdowns.length) {
                dropdowns.removeClass('is-active');
            }
            let modals = $('.pkih-modal-esc-close');
            if (modals.length) {
                e.preventDefault();
                modals.remove();
            }
        }
    });
});

})();
