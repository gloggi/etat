
// Global handling

function showModal(url, options) {
    $('body').modalmanager('loading');
    $.ajax({
        url: url,
        complete: function(xhr, status) {
            if(xhr.status == 500) {
                $('#ajax-modal').html('<pre>'+xhr.responseText+'</pre>');
            } else {
                $('#ajax-modal').html(xhr.responseText);
            }
            $('#ajax-modal').modal(options);
        }
    });
}

$('#ajax-modal').on('click', '.modal_link', function() {
    var url = $(this).attr('href');
        new_width = $(this).data('width') || '900px';

    $('#ajax-modal').load(url, function() {
        $('#ajax-modal').data('modal').options.width = new_width;
        $('#ajax-modal').modal('layout');
    });
    return false;
});

$('#ajax-modal').on('submit', 'form', function() {
    $('#ajax-modal').modal('loading');
    $(this).ajaxSubmit({
        target: '#ajax-modal',
        success: function (res, status, xhr) {
            if (xhr.status == 204) {
                $('#ajax-modal').trigger('modal-saved');
                $('#ajax-modal').modal('hide');
            }
        },
        error: function(res) {
            $('#ajax-modal').html('<pre>'+res.responseText+'</pre>');
        }
    });
    return false;
});