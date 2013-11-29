
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Camp, CampType, Participant
from .forms import CampForm, ParticipantForm

def camp_list(request):
    camps = Camp.objects.values('id', 'title', 'type').annotate(Count('participants'))
    types = CampType.objects.all()

    return render(request, 'camps/camp_list.html', {
        'camps': camps,
        'types': types,
    })


def camp_edit(request, c_id):
    camp = get_object_or_404(Camp, pk=c_id)
    if request.method == 'POST':
        form = CampForm(request.POST, instance=camp)
        if form.is_valid():
            form.save()
            return redirect('camp_edit', c_id=camp.id)
    else:
        form = CampForm(instance=camp)

    return render(request, 'camps/camp_form.html', {
        'camp': camp,
        'form': form,
    })


def participant_list(request, c_id):
    camp = get_object_or_404(Camp, pk=c_id)
    participants = camp.participants.select_related()

    return render(request, 'camps/participant_list.html', {
        'camp': camp,
        'participants': participants,
    })


def participant_edit(request, p_id):
    participant = get_object_or_404(Participant, pk=p_id)

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return HttpResponse('Saved', status=204)
    else:
        form = ParticipantForm(instance=participant)

    return render(request, 'camps/participant_form.html', {
        'participant': participant,
        'form': form
    })


def participant_delete(request, p_id):
    participant = get_object_or_404(Participant, pk=p_id)
    if request.method == 'POST':
        participant.delete()
        return HttpResponse('Deleted', status=204)

    return render(request, 'confirm_delete.html', {
        'object': participant
    })

