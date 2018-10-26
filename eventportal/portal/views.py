from django.shortcuts import render, get_object_or_404
from .models import Event
# Create your views here.

def EventList(request):
    events_list = Event.objects.all()
    context = {"event_list":events_list}
    return render(request, "portal/index.html", context)

def EventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event
    }
    return render(request, 'portal/detail.html', context)


