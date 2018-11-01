from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .models import Event, Profile, Clubs, Teams
from .forms import TeamForm


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
    event.attendees.add(user)
    return redirect('portal:detail', event_id)


@login_required(redirect_field_name='portal/detail.html', login_url='/')
def eventunregister(request, event_id):
    user_id = request.user.id
    user = get_object_or_404(Profile, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    event.attendees.remove(user)
    return redirect("portal:detail", event_id)


def clubs_list(request):
    list_clubs = Clubs.objects.all()
    print(list_clubs)
    context = {'list_clubs': list_clubs}
    return render(request, 'portal/clubslist.html', context)


def clubs_detail(request, club_id):
    club = get_object_or_404(Clubs, pk=club_id)
    event = Event.objects.all().filter(pk=club_id)
    context = {
        'club': club,
        'event': event,
    }
    return render(request, 'portal/clubdetails.html', context)


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


def teamregister(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            obj = Teams()
            obj.team_name = form.cleaned_data['team_name']
            obj.event = event
            obj.save()
            print(obj)
            # team.save()
            obj.refresh_from_db()
            return render(request, 'index.html')
    else:
        form = TeamForm()
        return render(request, 'portal/teamregister.html', {'form': form, 'event': event})
