"""eventportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from portal import views as general_views

urlpatterns = [
    path('', general_views.land, name='land'),
    path('home/', general_views.home, name='home'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('events/', include('portal.urls', namespace='events')),
    # path('login/', auth_views.login, {'template_name': 'portal/login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="portal/login.html"), name='logout'),
    # path('register/', general_views.register, name='register-user'),
    path('clubs/', general_views.clubs_list, name='club-list'),
    path('clubs/<int:club_id>', general_views.clubs_detail, name='club-detail'),
    url(r'^invite/(?P<team_id>\d+)/$', general_views.invite, name='invite'),
]
