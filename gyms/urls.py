from django.urls import path
from .views import TrainerPageView, OwnerPageView

urlpatterns = [
    path('trainer/', TrainerPageView.as_view(), name='trainer_page'),
    path('owner/', OwnerPageView.as_view(), name='owner_page'),
]
