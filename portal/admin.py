from django.contrib import admin
from .models import Event, Profile, Clubs, Winner, Teams
from django import forms

# Register your models here.


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'venue', 'start', 'end', 'attendees', 'creator', 'club', 'team_size', 'image')

    def clean(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        creator = self.cleaned_data.get('creator')
        club = self.cleaned_data.get('club')
        club_obj = Clubs.objects.get(pk=club.id)
        if start > end:
            raise forms.ValidationError("Dates are incorrect")
        elif not creator.user.is_staff:
            raise forms.ValidationError("Not a club secretary")
        elif club_obj.secretary.user != self.current_user:
            raise forms.ValidationError("Not this club's secretary")
        # print(club_obj.secretary.user == self.current_user)
        return self.cleaned_data


class EventAdmin(admin.ModelAdmin):
    form = EventForm

    def get_form(self, request, *args, **kwargs):
        form = super(EventAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form


class WinnerForm(forms.ModelForm):
    class Meta:
        model = Winner
        fields = ('event', 'first', 'second', 'third')

    def clean(self):
        event = self.cleaned_data.get('event')
        if event.club.secretary != self.current_user:
            raise forms.ValidationError("Only Secretary can declare winners.")
        if event.time_period() != 'Past':
            raise forms.ValidationError("Declare winners for past events only.")


class WinnerAdmin(admin.ModelAdmin):
    form = WinnerForm

    def get_form(self, request, *args, **kwargs):
        form = super(WinnerAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form


class ClubsForm(forms.ModelForm):
    class Meta:
        model = Clubs
        fields = ('name', 'about', 'secretary', 'joint_secretary', 'image', 'sec_image', 'jsec_image')

    def clean(self):
        sec = self.cleaned_data.get('secretary')
        jsec = self.cleaned_data.get('joint_secretary')
        if not sec.is_organizer:
            raise forms.ValidationError("Person assigned to secretary is not an organizer")
        if not jsec.is_organizer:
            raise forms.ValidationError("Person assigned to joint secretary is not an organizer")


class ClubsAdmin(admin.ModelAdmin):
    form = ClubsForm

    def get_form(self, request, *args, **kwargs):
        form = super(ClubsAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form


admin.site.register(Event, EventAdmin)
admin.site.register(Profile)
admin.site.register(Clubs, ClubsAdmin)
admin.site.register(Winner, WinnerAdmin)
admin.site.register(Teams)
