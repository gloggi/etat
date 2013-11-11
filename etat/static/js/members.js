
// Global members list$

// department tree compontent.
var DepartmentTree = Backbone.View.extend({
    // Get a list of all selected departments

    events: {
        'tree.click'            : 'treeClick',
    },

    getSelectedIds: function() {
        ids = [];
        _.forEach(this.$el.tree('getSelectedNodes'), function(node) {
            ids.push(node.id);
        });
        return ids;
    },

    keyStateChange: function(e) {
        this.shiftKey = e.shiftKey;
        this.ctrlKey = e.ctrlKey;
    },

    withAllSubNodes: function(action, node) {
        this.$el.tree(action, node);
        _.forEach(node.getData(), function(nodeData) {
            var node = this.$el.tree('getNodeById', nodeData.id);
            this.withAllSubNodes(action, node);
        }, this);
    },

    treeClick: function(e) {
        e.preventDefault();
        var node = e.node;
        if (document.shiftKey) {
            this.shiftClick(node);
        } else if (document.ctrlKey) {
            this.ctrlClick(node);
        } else {
            this.normalClick(node);
        }
        this.$el.trigger('selection_changed');
    },

    normalClick: function(node) {
        _.forEach(this.$el.tree('getSelectedNodes'), function(node) {
            this.$el.tree('removeFromSelection', node);
        }, this);
        this.$el.tree('selectNode', node);
    },

    shiftClick: function(node) {
        if (this.$el.tree('isNodeSelected', node)) {
            this.$el.tree('removeFromSelection', node);
        } else {
            this.$el.tree('addToSelection', node);
        }
    },

    ctrlClick: function(node) {
        var withAllSubNodes = _.bind(this.withAllSubNodes, this);
        if (this.$el.tree('isNodeSelected', node)) {
            withAllSubNodes('removeFromSelection', node);
            withAllSubNodes('closeNode', node);
        } else {
            withAllSubNodes('addToSelection', node);
            withAllSubNodes('openNode', node);
        }
    },

    initialize: function() {
        this.$el.tree({
            dataUrl: '/departments/data/',
            autoOpen: 3,
            saveState: true,
            useContextMenu: false,
            onCreateLi: function(node, $li) {
                var data = node.getData();
                $li.find('.jqtree-title').before('<i class="icon-group"></i> ');
            }
        });
    },

});


Etat.Views.MemberView = Backbone.View.extend({

    events: {
        "tree.init #department-tree"         : "loadMembers",
        "selection_changed #department-tree" : "loadMembers",
        "change #roles-filter"               : "loadMembers",
        "change #education-filter"           : "loadMembers",
        "change .status-filter input"        : "loadMembers",
        "keyup input[type=search]"           : "searchChanged",
        "click .clear-search"                : "clearSearch",
        "click .gender-filter button"        : "filterByGender",
        "click .member-add"                  : "addMember",
        "click .member-detail"               : "showMember",
        "click .member-edit"                 : "editMember",
    },

    initialize: function() {
        this.departmentTree = new DepartmentTree({el: $('#department-tree')});

        // list.js table of all members
        this.memberList = new List('member-list', {
            valueNames: ['first_name', 'last_name', 'scout_name', 'roles_display'],
            page: 1000
        });

        this.memberList.on('updated', _.bind(this.updateFilterBadges, this));
    },

    memberIdForEvent: function() {
        return $(event.target).parents('tr').find('td.id').text();
    },

    // Launch modal to create a new member
    addMember: function() {
        showModal('/members/add/', {width: '900px'});
    },

    // Display short stats of one member
    showMember: function(event) {
        var id = this.memberIdForEvent(event);
        showModal('/members/' + id + '/', {width: '700px'});
    },

    // Start editing a member
    editMember: function(event) {
        var id = this.memberIdForEvent(event);
        showModal('/members/' + id + '/edit/', {width: '900px'});
    },

    // File male or females in member list
    filterByGender: function(e) {
        var gender = $(e.currentTarget).data('gender');

        if (this.genderFilter === gender) {
            this.genderFilter = undefined;
            $(e.currentTarget).blur();
            this.memberList.filter();
        } else {
            this.genderFilter = gender;
            this.memberList.filter(function(member) {
                return member.values().gender == gender;
            });
        }
    },

    // Get all active filters to reload member list
    collectFilters: function() {
        var filterArgs = {};
        filterArgs['departments'] = this.departmentTree.getSelectedIds();

        filterArgs['roles'] = $('#roles-filter').val();
        filterArgs['education'] = $('#education-filter').val();

        var active = $('input[name=active]').prop('checked'),
            inactive = $('input[name=inactive]').prop('checked');
        if (active && !inactive) {
            filterArgs['status'] = 'active';
        } else if (inactive && !active) {
            filterArgs['status'] = 'inactive';
        } else if (!active && !inactive) {
            filterArgs['status'] = 'none';
        }

        return filterArgs;
    },

    // Reload member data form server an display them in member table
    loadMembers: function() {
        this.$el.find('input[type=search]').val('');
        var members = new Etat.Collections.Members();
        var memberList = this.memberList;

        members.fetch({
            data: this.collectFilters(),
            success: _.bind(this.updateMemberList, this),
        });
    },

    updateMemberList: function(members) {
        members = members.toJSON();
        this.memberList.clear();
        if (members.length) {
            this.appendRoles(members);
            this.memberList.add(members);
            this.memberList.search();
            this.memberList.sort('id', { asc: true });
        }
    },

    appendRoles: function(members) {
        var selected_departments = this.departmentTree.getSelectedIds();
            show_active = $('input[name=active]').prop('checked');
            show_inactive = $('input[name=inactive]').prop('checked');

        _.each(members, function(m) {
            roles = [];
            _.each(m.roles, function(r) {
                if (_.indexOf(selected_departments, r.department) != -1) {
                    if (r.active && show_active || !r.active && show_inactive) {
                        roles.push(r.type);
                    }
                }
            });
            m.roles_display = roles.join(', ');
        });
    },

    updateFilterBadges: function() {
        var list = this.memberList,
            $total = this.$el.find('span.total'),
            $slash = this.$el.find('span.slash'),
            $filtered = this.$el.find('span.filtered');

        $total.text(list.items.length);
        if (list.visibleItems.length != list.items.length) {
            $filtered.text(list.visibleItems.length);
            $slash.show();
        } else {
            $filtered.text('');
            $slash.hide();
        }
    },

    searchChanged: function(e) {
        $this = $(e.currentTarget);
        $icon = $this.parent().find('i.fa');
        if ($this.val() === '') {
            $icon.addClass('fa-search');
            $icon.removeClass('fa-times');
        } else {
            $icon.removeClass('fa-search');
            $icon.addClass('fa-times');
        }
    },

    clearSearch: function() {
        $('input[type=search]').val('');
        this.memberList.search();
    }
});


// Kick off things
$(function () {
    var memberView = new Etat.Views.MemberView({el:$('#member-view')});

    $('#ajax-modal').on('modal-saved', function() {
        memberView.loadMembers();
    });

    // monitor shift and ctrl keys
    $(document).on('keydown keyup', function(e) {
        document.shiftKey = e.shiftKey;
        document.ctrlKey = e.ctrlKey;
    });
});