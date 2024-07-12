from django.urls import path
from .views import TrainerPageView, TrainerDetailPageView, ProfileAddPageView, TrainerPortfolioView

urlpatterns = [
    path('trainer/PT_membership_management/profile/', TrainerPageView.as_view(), name='trainer_page'),
    path('trainer/PT_membership_management/profile/user_num/<int:id>/', TrainerDetailPageView.as_view(), name='trainer_detail_page'),
    path('trainer/PT_membership_management/profile/user_num/<int:id>/profile_add/', ProfileAddPageView.as_view(), name='profile_add_page'),
    # path('trainer/portflio/trainer_num/<int:id>/', TrainerPortfolioView.as_view(), name='trainer_portflio_page'),
]
