from django.urls import path
from .views import TrainerPageView

urlpatterns = [
    path('trainer/', TrainerPageView.as_view(), name='trainer_page'),
]
