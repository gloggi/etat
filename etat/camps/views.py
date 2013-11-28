
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .models import Camp, CampType
from .forms import CampForm, ParticipantsFormset

def camp_list(request):
    camps = Camp.objects.values('id', 'title', 'type').annotate(Count('participants'))
    types = CampType.objects.all()

    return render(request, 'camps/list.html', {
        'camps': camps,
        'types': types,
    })


def camp_edit(request, c_id):
    camp = get_object_or_404(Camp, pk=c_id)

    if request.method == 'POST':
        form = CampForm(request.POST, instance=camp)
        participants = ParticipantsFormset(request.POST, instance=camp)
        if form.is_valid() and participants.is_valid():
            form.save()
            participants.save()
            return redirect('camp_list')
    else:
        form = CampForm(instance=camp)
        participants = ParticipantsFormset(instance=camp)

    return render(request, 'camps/form.html', {
        'form': form,
        'participants': participants
    })