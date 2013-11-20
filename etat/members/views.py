import json
import unicodecsv

from django.http import HttpResponse, Http404
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.utils.translation import ugettext as _

from etat.departments.models import Department
from etat.utils.deletion import deletion_tree

from .models import Member, Address, Reachability, Role
from .forms import (MemberFilterForm, MemberForm, AddressFormSet,
    EducationFormSet, limited_role_formset, ReachabilityFormSet)

def member_list(request):
    try:
        editable = request.user.member.editable_departments()
        departments = editable.values_list('id', flat=True)
    except Member.DoesNotExist:
        departments = []

    if request.user.is_superuser:
        departments = Department.objects.all().values_list('id', flat=True)

    return render(request, 'members/list.html', {
        'filter_form': MemberFilterForm,
        'editable_departments': list(departments),
    })


def _member_filter(request):
    filter_args = []
    departments = request.REQUEST.getlist('departments')
    filter_args.append(Q(departments__in=departments))

    filter_form = MemberFilterForm(request.REQUEST)
    if not filter_form.is_valid():
        return HttpResponse(json.dumps(filter_form.errors),
            mimetype="application/json", status=403)
    f = filter_form.cleaned_data

    if f['roles']:
        filter_args.append(Q(roles__type__in=f['roles']))
    if f['educations']:
        filter_args.append(Q(educations__type__in=f['educations']))
    if f['steps']:
        filter_args.append(Q(departments__step__in=f['steps']) |
                           Q(roles__type__step__in=f['steps']))
    if f['active'] and not f['inactive']:
        filter_args.append(Q(roles__active=True))
    if not f['active'] and f['inactive']:
        filter_args.append(Q(roles__active=False))
    if not f['active'] and not f['inactive']:
        filter_args.append(Q(roles__active=None))

    return Member.objects.filter(*filter_args).distinct()


def member_data(request):
    members = _member_filter(request)
    member_values = ('id', 'scout_name', 'first_name', 'last_name', 'gender')
    member_data = members.values(*member_values)

    member_ids = members.values_list('id', flat=True)
    member_dict = dict((m['id'], m) for m in member_data)
    roles = Role.objects.filter(member_id__in=member_ids)

    for role in roles.values('member', 'department', 'type__name', 'active'):
        m = member_dict[role['member']]
        if 'roles' not in m:
            m['roles'] = []
        m['roles'].append({
            'department': role['department'],
            'type': role['type__name'],
            'active': role['active'],
        })

    return HttpResponse(
        json.dumps(list(member_data)),
        mimetype='application/json'
    )


def member_export(request):
    member_fields = ['scout_name', 'first_name', 'last_name', 'gender', 'birthday']
    address_fields = ['street', 'postal_code', 'city']

    members = _member_filter(request).values_list('id', *member_fields)
    member_dict = dict((m[0], list(m[1:])) for m in members)
    addresses = Address.objects.filter(main=True, member_id__in=member_dict.keys())

    for adr in addresses.values_list('member_id', *address_fields):
        member_dict[adr[0]].extend(adr[1:])

    member_reach = {}
    reach = Reachability.objects.filter(member_id__in=member_dict.keys)
    for r in reach:
        if r.member_id not in member_reach:
            member_reach[r.member_id] = {}
        m = member_reach[r.member_id]
        if r.type == 'phone' and 'phone' not in m:
            m['phone'] = r.value
        if r.type == 'email' and 'email' not in m:
            m['email'] = r.value

    for m_id, v in member_reach.items():
        member_dict[m_id].extend(v.values())

    header_row = []
    for mf in member_fields:
        field = Member._meta.get_field(mf)
        header_row.append(field.verbose_name.upper())

    for af in address_fields:
        field = Address._meta.get_field(af)
        header_row.append(field.verbose_name.upper())

    header_row.extend([r.upper() for r in (_('Phone'), _('Email'))])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'
    writer = unicodecsv.writer(response)
    writer.writerow(header_row)
    for member in member_dict.values():
        writer.writerow(member)

    return response


def member_view(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    return render(request, 'members/view.html', {
        'member': member,
    })


class MemberFormsets():

    def __init__(self, editor, data=None, *args, **kwargs):
        self.context = {
            'address_formset': AddressFormSet(data, *args, **kwargs),
            'roles_formset': limited_role_formset(editor, data, *args, **kwargs),
            'education_formset': EducationFormSet(data, *args, **kwargs),
            'reachability_formset': ReachabilityFormSet(data, *args, **kwargs)
        }

    def all_valid(self):
        all_valid = True
        for formset in self.context.values():
            formset.full_clean()
            if not formset.is_valid():
                formset.has_errors = True
                all_valid = False
        return all_valid

    def save(self):
        for formset in self.context.values():
            formset.save()


def member_add(request):
    editor = request.user

    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES or {})
        formsets = MemberFormsets(editor, request.POST)

        if member_form.is_valid():
            member = member_form.save(commit=False)
            formsets = MemberFormsets(request.POST, instance=member)

            if formsets.all_valid():
                member.save()
                formsets.save()
                return HttpResponse('Saved', status=204)
    else:
        member_form = MemberForm()
        formsets = MemberFormsets(editor)

    context = {'member_form': member_form}
    context.update(formsets.context)
    return render(request, 'members/form.html', context)


def has_permission_to_edit(editor, member):
    """ Returns true if the editor is allowed to edit this member """
    if editor.is_superuser:
        return True
    try:
        editable_departments = editor.member.editable_departments()
    except Member.DoesNotExist:
        return False

    editable_department_ids = editable_departments.values_list('id', flat=True)
    member_department_ids = member.departments.values_list('id', flat=True)

    return any(d in member_department_ids for d in editable_department_ids)


def member_edit(request, m_id):
    editor = request.user
    member = get_object_or_404(Member, pk=m_id)

    if not has_permission_to_edit(editor, member):
        return render(request, 'permission_denied.html', {
            'object': member
        }, status=403)

    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES or {}, instance=member)
        formsets = MemberFormsets(editor, request.POST, instance=member)

        if member_form.is_valid() and formsets.all_valid():
            member_form.save()
            formsets.save()
            return HttpResponse('Saved', status=204)
    else:
        member_form = MemberForm(instance=member)
        formsets = MemberFormsets(editor, instance=member)

    context = {
        'member': member,
        'member_form': member_form
    }
    context.update(formsets.context)
    return render(request, 'members/form.html', context)


def member_delete(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    if request.method == 'POST':
        member.delete()
        return HttpResponse('Deleted', status=204)

    return render(request, 'members/delete.html', {
        'member': member,
        'to_delete': deletion_tree(member),
    })


def account_create(request, m_id):
    member = get_object_or_404(Member, pk=m_id)

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = member.first_name
            user.last_name = member.last_name
            try:
                user.email = member.reachabilities.filter(type='email')[0].value
            except:
                pass
            user.save()
            member.user = user
            member.save()
            return redirect('member_edit', m_id=m_id)
    else:
        form = UserCreationForm()

    return render(request, 'members/account_form.html', {
        'member': member,
        'form': form
    })


def account_change_password(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    try:
        user = member.user
    except:
        raise Http404

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('member_edit', m_id=m_id)
    else:
        form = SetPasswordForm(user)

    return render(request, 'members/account_form.html', {
        'member': member,
        'form': form
    })


def account_delete(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    try:
        user = member.user
    except:
        raise Http404

    if request.method == 'POST':
        user.delete()
        return redirect('member_edit', m_id=m_id)

    return render(request, 'confirm_delete.html', {
        'object': user
    })