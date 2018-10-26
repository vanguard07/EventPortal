from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'portal'
urlpatterns = [
    path('', views.EventList, name='index'),
    path('<int:event_id>', views.EventDetail, name='detail'),
    path('<int:event_id>/register', views.EventRegister, name='register'),
    path('login/', auth_views.login, {'template_name': 'portal/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'portal/logout.html'}, name='logout'),
    path('register/', views.register, name='register-user'),
    path('home/', views.home, name='home')
]