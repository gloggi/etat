
window.Etat = {
    Models: {},
    Collections: {},
    Views: {},
};


$(function () {
    // Global jquery helpers
    $("select").chosen({width: '100%'});
    $('.datepicker').datepicker({
        format: 'dd.mm.yyyy'
    });

    // Bootstrap 3 support for bootstrap-modal
    $.fn.modal.defaults.spinner = $.fn.modalmanager.defaults.spinner =
    '<div class="loading-spinner" style="width: 200px; margin-left: -100px;">' +
        '<div class="progress progress-striped active">' +
            '<div class="progress-bar" style="width: 100%;"></div>' +
        '</div>' +
    '</div>';
});