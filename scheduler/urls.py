from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('eventData/', views.event_data, name='event_data'),
    path('user_eventData/', views.user_event_data, name='user_event_data'),
    path('saveEvent/', views.save_event, name='save_event'),
    path('saveDelete/', views.delete_event, name='delete_event'),
]
