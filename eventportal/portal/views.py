from django.shortcuts import render, get_object_or_404
from .models import Event, Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def EventList(request):
    events_list = Event.objects.all()
    context = {"event_list":events_list}
    return render(request, "portal/index.html", context)

def EventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        print(event.id)
    context = {
        'event': event
    }
    return render(request, 'portal/detail.html', context)

def EventRegister(request, event_id):
    user_id = request.user.id
    user = Profile.objects.get(pk=user_id)
    event = Event.objects.get(pk=event_id)
    event.attendees.add(user)
    return HttpResponseRedirect(reverse("portal:detail", args=(event_id, )))

