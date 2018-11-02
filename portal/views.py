from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

from .models import Event, Profile, Clubs, Teams
from .forms import MemberForm


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

@login_required(redirect_field_name='portal/teamregister.html', login_url='/')
def teamregister(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            obj = Teams()
            obj.team_name = form.cleaned_data['team_name']
            obj.event = event
            user = get_object_or_404(Profile, pk=request.user.id)
            obj.members = user
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
                # request.POST.getlist('emailid')
                ['avtans@gmail.com']
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


@login_required(redirect_field_name='portal/teamregister.html', login_url='/')
def invite(request, team_id):
    team = get_object_or_404(Teams, pk=team_id)
    team.members.add("xyz")
    print(team.members)
    return HttpResponse("success")
