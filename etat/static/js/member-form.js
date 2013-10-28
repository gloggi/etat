
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
        // preselect new role deparmtent and type (if possible) for new roles
        // if (this.$el.hasClass('add')) {
        //     var selected = _(DepartmentTree.getSelectedIds()).first();
        //     if (selected) {
        //         var dep = $('#department_tree #' + selected);
        //         var id = dep.attr('id');
        //         var default_role = dep.data('default_role');

        //         var dep_select = $('#roles select[name$=department]:first');
        //         if (dep_select.val() === '') dep_select.val(id);

        //         var type_select = $('#roles select[name$=type]:first');
        //         if (type_select.val === '') type_select.val(default_role);

        //         var start_input = $('#roles input[name$=start]:first');
        //         if (start_input.val() === '') start_input.val(this.currentDate());
        //     }
        // }

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

        console.log($('.education.form-template tr'));

        this.initWidgets();

    }
});

