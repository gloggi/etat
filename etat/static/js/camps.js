
$(function () {
    var campList = new List('camp-view', {
        valueNames: ['title', 'begin', 'type']
    });

    $('select.year').change(function () {
        var year = $(this).val();
        if (year === '') {
            campList.filter();
        } else {
            campList.filter(function(camp) {
                return camp.values().begin.indexOf(year) !== -1;
            });
        }
    });

    $('select.type').change(function () {
        var type = $(this).val();
        if (type === '') {
            campList.filter();
        } else {
            campList.filter(function(camp) {
                return camp.values().type === type;
            });
        }
    });
});