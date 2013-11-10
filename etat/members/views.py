import json

from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from etat.utils.deletion import deletion_tree

from .models import Member, Role, RoleType, EducationType
from .forms import (MemberForm, AddressFormSet, RoleFormSet, EducationFormSet,
    ReachabilityFormSet)


def member_data(request):
    filter_args = []
    departments = request.GET.getlist('departments[]')
    roles = request.GET.getlist('roles[]')
    education = request.GET.getlist('education[]')
    status = request.GET.get('status')
    gender = request.GET.get('gender')

    if departments:
        filter_args.append(Q(departments__id__in=departments))

    if roles:
        filter_args.append(Q(roles__type__id__in=roles))

    if education:
        filter_args.append(Q(educations__type__id__in=education))

    if gender:
        filter_args.append(Q(gender=gender))

    if status == 'active':
        filter_args.append(Q(roles__active=True))
    elif status == 'inactive':
        filter_args.append(Q(roles__active=False))
    elif status == 'none':
        filter_args.append(Q(roles__active=None))

    members = Member.objects.filter(*filter_args).distinct()
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


def member_list(request):
    return render(request, 'members/list.html', {
        'roles': RoleType.objects.all(),
        'educations': EducationType.objects.all(),
    })


def member_view(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    return render(request, 'members/view.html', {
        'member': member,
    })


class MemberFormsets():

    def __init__(self, data=None, *args, **kwargs):
        self.context = {
            'address_formset': AddressFormSet(data, *args, **kwargs),
            'roles_formset': RoleFormSet(data, *args, **kwargs),
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
    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES or {})
        formsets = MemberFormsets(request.POST)

        if member_form.is_valid():
            member = member_form.save(commit=False)
            formsets = MemberFormsets(request.POST, instance=member)

            if formsets.all_valid():
                member.save()
                formsets.save()
                return HttpResponse('Saved', status=204)
    else:
        member_form = MemberForm()
        formsets = MemberFormsets()

    context = {'member_form': member_form}
    context.update(formsets.context)
    return render(request, 'members/form.html', context)


def member_edit(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES or {}, instance=member)
        formsets = MemberFormsets(request.POST, instance=member)

        if member_form.is_valid() and formsets.all_valid():
            member_form.save()
            formsets.save()
            return HttpResponse('Saved', status=204)
    else:
        member_form = MemberForm(instance=member)
        formsets = MemberFormsets(instance=member)

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