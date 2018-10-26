from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Event, Profile
from .forms import SignUpForm
# Create your views here.


def EventList(request):
    events_list = Event.objects.all()
    context = {"event_list": events_list}
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
    user = get_object_or_404(Profile, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    print(user_id)
    event.attendees.add(user)
    return HttpResponseRedirect(reverse("portal:detail", args=(event_id, )))


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse("portal:home"))
    else:
        form = SignUpForm()
    return render(request, 'portal/signup.html', {'form': form})


def home(request):
    return render(request, 'portal/index.html')

