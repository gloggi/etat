from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from suit.admin import SortableModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin
from etat.utils.widgets import SuitSelect

from .models import Department, DepartmentType

class DepartmentTypeAdmin(SortableModelAdmin):
    pass


class DepartmentAdminForm(forms.ModelForm):
    class Meta:
        model = Department
        widgets = {
            'parent': SuitSelect,
            'type': SuitSelect,
            'default_role': SuitSelect,
        }


class DepartmentAdmin(DjangoMpttAdmin):
    list_display = ('name_indented',)
    search_fields = ('name',)
    list_filter = ('type',)
    form = DepartmentAdminForm

    def name_indented(self, obj):
        indent = 10 * obj.level
        output = u'<span style="padding-left: %spx">%s</span>' % (indent, obj)
        return mark_safe(output)

admin.site.register(DepartmentType, DepartmentTypeAdmin)
admin.site.register(Department, DepartmentAdmin)
