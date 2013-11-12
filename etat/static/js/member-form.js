
Etat.Views.MemberForm = Backbone.View.extend({
    events : {
        'change input[name$=main]'  : 'onlyOneAddress',
    },

    onlyOneAddress: function(event) {
        $('input[name$=main][id!='+event.target.id+']').prop('checked', false);
    },

    currentDate: function() {
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1;
        var yyyy = today.getFullYear();
        return dd + '.' + mm + '.' + yyyy;
    },

    initWidgets: function() {
        $(".member-form select").chosen({width: '100%'});
        $(".member-form input.date").datepicker({format: 'dd.mm.yyyy'});
    },

    initialize: function() {

        $('.member-tab-nav a').click(function() {
            $(this).tab('show');
        });

        $('.addresses tr').formset({
            prefix: 'addresses',
            formCssClass: 'addresses-formset',
            formTemplate: $('.address.form-template tr'),
            added: this.initWidgets
        });

        $('.reachability tr').formset({
            prefix: 'reachabilities',
            formCssClass: 'reachability-formset',
            formTemplate: $('.reach.form-template tr'),
            added: this.initWidgets
        });

        $('.roles tr').formset({
            prefix: 'roles',
            formCssClass: 'roles-formset',
            formTemplate: $('.role.form-template tr'),
            added: this.initWidgets
        });

        $('.educations tr').formset({
            prefix: 'educations',
            formCssClass: 'education-formset',
            formTemplate: $('.education.form-template tr'),
            added: this.initWidgets
        });

        this.initWidgets();

    }
});

