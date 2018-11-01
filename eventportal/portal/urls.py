from django.urls import path, include
from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.EventList, name='index'),
    path('<int:event_id>/', views.EventDetail, name='detail'),
    path('<int:event_id>/register', views.EventRegister, name='register'),
    path('<int:event_id>/unregister', views.eventunregister, name='unregister'),
    path('<int:event_id>/teamregister', views.teamregister, name='teamregister'),
]
