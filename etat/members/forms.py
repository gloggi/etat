
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from mptt.forms import TreeNodeChoiceField

from etat.commons import STEPS
from etat.utils.widgets import ImageWidget
from etat.departments.models import Department

import models


class MemberFilterForm(forms.Form):
    gender = forms.MultipleChoiceField(
        choices=models.Member.GENDER_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    roles = forms.ModelMultipleChoiceField(
        label=_('Roles'),
        queryset=models.RoleType.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'data-placeholder': _('All')}
        ))
    steps = forms.MultipleChoiceField(
        label=_('steps'),
        choices=STEPS,
        required=False,
        widget=forms.SelectMultiple(
            attrs={'data-placeholder': _('All')}
        ))
    educations = forms.ModelMultipleChoiceField(
        label=_('Educations'),
        queryset=models.EducationType.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'data-placeholder': _('All')}
        ))
    active = forms.BooleanField(required=False)
    inactive = forms.BooleanField(required=False)


class MemberForm(forms.ModelForm):
    portrait = forms.ImageField(widget=ImageWidget, required=False)

    class Meta:
        model = models.Member
        exclude = ('departments', 'user')
        widgets = {
            'gender': forms.RadioSelect
        }


class EducationInlineForm(forms.ModelForm):
    class Meta:
        model = models.Education
        widgets = {
            'date': forms.DateInput(attrs={'class': 'date'}),
        }


class OneRequiredFormset(BaseInlineFormSet):
    def clean(self):
        super(OneRequiredFormset, self).clean()
        if self.is_valid():
            self.saved_forms = []
            initial = self.initial_form_count()
            new = len(self.save_new_objects(commit=False))
            deleted = len(self.deleted_forms)
            if initial + new - deleted == 0:
                msg = _(u'%(parent)s must have at least one %(child)s!') % {
                    'parent': self.instance._meta.verbose_name,
                    'child': self.model._meta.verbose_name
                }
                raise ValidationError(msg)


class ReachabilitySelect(forms.Select):

    OPTION = '''<option value="{0}" class="{2}" {1}> {3} </option>'''

    def render_option(self, selected_choices, option_value, option_label):
            if option_value == None:
                option_value = ''
            option_value = force_text(option_value)
            if option_value in selected_choices:
                selected_html = mark_safe(' selected="selected"')
                if not self.allow_multiple_selected:
                    # Only allow for a single selection.
                    selected_choices.remove(option_value)
            else:
                selected_html = ''


            return mark_safe(self.OPTION.format(
                   option_value,
                   selected_html,
                   models.Reachability.icons.get(option_value),
                   force_text(option_label)
            ))


class ReachabilityForm(forms.ModelForm):
    class Meta:
        model = models.Reachability
        widgets = {
            'type': ReachabilitySelect
        }


AddressFormSet = inlineformset_factory(
    models.Member,
    models.Address,
    extra=0,
    formset=OneRequiredFormset
)



EducationFormSet = inlineformset_factory(
    models.Member,
    models.Education,
    extra=0,
    form=EducationInlineForm,
)

ReachabilityFormSet = inlineformset_factory(
    models.Member,
    models.Reachability,
    form=ReachabilityForm,
    extra=0
)

def limited_role_formset(editor, data=None, *args, **kwargs):
    """
    Creates a limited formset with for only departments the editor is a member of
    """

    try:
        departments = editor.member.editable_departments()
    except models.Member.DoesNotExist:
        departments = Department.objects.none()
    if editor.is_superuser:
        departments = Department.objects.all()

    class RoleInlineForm(forms.ModelForm):
        department = TreeNodeChoiceField(queryset=departments)

        class Meta:
            model = models.Role
            widgets = {
                'start': forms.DateInput(attrs={'class': 'date'}),
                'end': forms.DateInput(attrs={'class': 'date'}),
            }

    RoleFormset = inlineformset_factory(
        models.Member,
        models.Role,
        extra=0,
        form=RoleInlineForm,
        formset=OneRequiredFormset
    )

    editable_roles = models.Role.objects.filter(department__in=departments)
    kwargs['queryset'] = editable_roles

    return RoleFormset(data, *args, **kwargs)