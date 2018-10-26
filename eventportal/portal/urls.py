from django.urls import path, include
from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.EventList, name='index'),
    path('<int:event_id>', views.EventDetail, name='detail'),
]