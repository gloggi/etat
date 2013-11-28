

$(function () {
    var campList = new List('camp-view', {
        valueNames: ['title', 'type']
    });

    $('.type-filter a').click(function () {
        $('.type-filter a').removeClass('active');
        $(this).addClass('active');

        var filter = $(this).data('filter');
        if (filter === '') {
            campList.filter();
        } else {
            campList.filter(function(camp) {
                return parseInt(camp.values().type, 10) === filter;
            });
        }
    });

    $('#camp-tabs a').click(function (e) {
      e.preventDefault();
      $(this).tab('show');
    });

    $('#camp-tabs a:first').tab('show');
});