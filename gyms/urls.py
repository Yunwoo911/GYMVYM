from django.urls import path
from .views import ProfilePageView, TrainerDetailPageView, ProfileAddPageView, TrainerPortfolioView, search, PtMembershipManagementPageView

urlpatterns = [
    path('trainer/PT_membership_management/', PtMembershipManagementPageView.as_view(), name='pt_membership_management_page'),
    path('trainer/PT_membership_management/profile/', ProfilePageView.as_view(), name='profile_page'),
    path('trainer/PT_membership_management/profile/user_num/<int:id>/', TrainerDetailPageView.as_view(), name='trainer_detail_page'),
    path('trainer/PT_membership_management/profile/user_num/<int:id>/profile_add/', ProfileAddPageView.as_view(), name='profile_add_page'),
    # path('trainer/portflio/trainer_num/<int:id>/', TrainerPortfolioView.as_view(), name='trainer_portflio_page'),
    # path('trainer/PT_membership_management/profile/search/', search, name='member_profile_search_page'),
]
