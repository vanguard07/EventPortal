from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail

from .forms import MemberForm
from .models import Event, Profile, Clubs, Teams, Winner


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
    events = Event.objects.all().filter(attendees=user)
    list_clubs = Clubs.objects.all()
    events_list = Event.objects.all()
    print(events_list)
    context = {
        'first_name': user.user.first_name,
        'username': user.user.username,
        'events': events,
        'list_clubs': list_clubs,
        "event_list": events_list,
    }
    return render(request, 'portal/home.html', context)


def EventList(request):
    events_list = Event.objects.all()
    context = {"event_list": events_list}
    return render(request, "portal/index.html", context)


def EventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = event.attendees.all()
    if event.time_period() == "Past":
        winners = Winner.objects.all().filter(event=event_id)
        print(winners)
        context = {
            'event': event,
            'attendees': attendees,
            'winners': winners,
        }
    else:
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
    if event.time_period() == "Future":
        event.attendees.add(user)
        subject = event.name + " Registration"
        msg = "You are successfully registered for the event: " + event.name + "."
        recipient = [user.user.email]
        send_mail(subject, msg, settings.EMAIL_HOST_USER, recipient, fail_silently=False)
    return redirect('portal:detail', event_id)


@login_required(redirect_field_name='portal/detail.html', login_url='/')
def eventunregister(request, event_id):
    user_id = request.user.id
    user = get_object_or_404(Profile, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    if event.time_period() == "Future":
        event.attendees.remove(user)
        subject = event.name + " Registration"
        msg = "You are successfully unregistered for the event: " + event.name + "."
        recipient = [user.user.email]
        send_mail(subject, msg, settings.EMAIL_HOST_USER, recipient, fail_silently=False)
    return redirect("portal:detail", event_id)


def clubs_list(request):
    list_clubs = Clubs.objects.all()
    print(list_clubs)
    context = {'list_clubs': list_clubs}
    return render(request, 'portal/clublist.html', context)


def clubs_detail(request, club_id):
    club = get_object_or_404(Clubs, pk=club_id)
    event = Event.objects.all().filter(club=club_id)
    print(event)
    context = {
        'club': club,
        'event': event,
    }
    return render(request, 'portal/clubdetails.html', context)


@login_required(redirect_field_name='portal/teamregister.html', login_url='/')
def teamregister(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = get_object_or_404(Profile, pk=request.user.id)
    if user not in event.attendees.all():
        if request.method == 'POST':
            form = MemberForm(request.POST)
            if form.is_valid():
                obj = Teams()
                obj.team_name = form.cleaned_data['team_name']
                obj.event = event
                obj.members = user
                event.attendees.add(user)
                obj.save()
                obj.refresh_from_db()
                team = Teams.objects.filter(team_name=form.cleaned_data['team_name']).values_list('pk', flat=True)
                url = 'http://127.0.0.1:8000/invite/' + str(team[0])
                message = str(obj.members) + " has invited you to join the team " + str(obj.team_name) + \
                          " for the event " + str(event.name)
                msg = EmailMultiAlternatives(
                    'Invite for joining team ' + str(team[0]),
                    message,
                    settings.EMAIL_HOST_USER,
                    [request.POST.getlist('emailid')]
                )
                html_content = url
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                print(request.POST.getlist('emailid'))
                # team.save()
                return render(request, 'portal/index.html')
        else:
            form = MemberForm()
            context = {
                'form': form,
                'event': event,
                'range': range(1, event.team_size)
            }
            return render(request, 'portal/teamregister.html', context)
    else:
        return HttpResponse("Already registered")


@login_required(redirect_field_name='portal/teamregister.html', login_url='/')
def invite(request, team_id):
    team = get_object_or_404(Teams, pk=team_id)
    team.members.add("xyz")
    print(team.members)
    return render(request, 'home')


def winner(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    winners = Winner.objects.all().filter(event=event_id)
    context = {
        'winners': winners,
        'event': event,
    }
    return render(request, 'portal/winners.html', context)


def winnerlist(request):
    events_list_ids = []
    winner_list = []
    for event in Event.objects.all():
        if event.time_period() == "Past":
            events_list_ids.append(event.id)
            winner_list.append(Winner.objects.filter(event=event.id))
    events_list = Event.objects.filter(id__in=events_list_ids)
    context = {
        "events_list": events_list,
        "winner_list": winner_list,
    }
    return render(request, "portal/winners.html", context)
