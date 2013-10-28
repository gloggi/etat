from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from etat.utils.deletion import deletion_tree

from .models import Member, RoleType, EducationType
from .forms import (MemberForm, AddressFormSet, RoleFormSet, EducationFormSet,
    ReachabilityFormSet)


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