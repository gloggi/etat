from django.contrib import admin

from suit.admin import SortableModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

import models


class AddressAdminInline(admin.StackedInline):
    model = models.Address
    extra = 0


class RoleAdminInline(admin.TabularInline):
    model = models.Role
    extra = 0


class EducationAdminInline(admin.TabularInline):
    model = models.Education
    extra = 0


class ReachabilityAdminInline(admin.TabularInline):
    model = models.Reachability
    extra = 0


class MemberAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('scout_name', 'first_name', 'last_name')
    search_fields = ('scout_name', 'first_name', 'last_name')

    inlines = [
        RoleAdminInline,
        EducationAdminInline,
        AddressAdminInline,
        ReachabilityAdminInline,
    ]

    fieldsets = (
        (None, {
            'fields': ('scout_name', 'first_name', 'last_name', 'portrait',
                'gender', 'birthday', 'user')
        }),
        ('Notes', {
            'classes': ('collapse',),
            'fields': ('notes',),
        }),
    )


class RoleTypeAdmin(SortableModelAdmin):
    sortable = 'order'


class EducationTypeAdmin(SortableModelAdmin):
    sortable = 'order'


admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.RoleType, RoleTypeAdmin)
admin.site.register(models.EducationType, EducationTypeAdmin)