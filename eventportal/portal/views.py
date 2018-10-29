from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Event, Profile
from .forms import SignUpForm
# Create your views here.


def land(request):
    # print(request.user)
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'portal/login.html')


@login_required(redirect_field_name='portal/detail.html', login_url='/')
def home(request):
    user_id = request.user.id
    user = get_object_or_404(Profile, pk=user_id)
    context = {
        'first_name': user.user.first_name,
        'username': user.user.username,
    }
    return render(request, 'portal/home.html', context)


def EventList(request):
    events_list = Event.objects.all()
    context = {"event_list": events_list}
    return render(request, "portal/index.html", context)


def EventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = event.attendees.all()
    if request.method == 'POST':
        print(event.id)
    context = {
        'event': event,
        'attendees': attendees,
    }
    return render(request, 'portal/detail.html', context)


@login_required(redirect_field_name='portal/detail.html', login_url='/')
def EventRegister(request, event_id):
    user_id = request.user.id
    user = get_object_or_404(Profile, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    # attendees = event.attendees.all()
    event.attendees.add(user)
    return redirect('portal:detail', event_id)


@login_required(redirect_field_name='portal/detail.html', login_url='/')
def eventunregister(request, event_id):
    user_id = request.user.id
    user = get_object_or_404(Profile, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    event.attendees.remove(user)
    # attendees = event.attendees.all()
    return redirect("portal:detail", event_id)
    # return redirect('portal:index')
#
# def register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return HttpResponseRedirect(reverse("portal:index"))
#     else:
#         form = SignUpForm()
#     return render(request, 'portal/signup.html', {'form': form})



