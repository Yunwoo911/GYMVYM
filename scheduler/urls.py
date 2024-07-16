from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('eventData/', views.event_data, name='event_data'),
    path('saveEvent/', views.save_event, name='save_event'),
]
