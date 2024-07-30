from django.urls import path
from .views import ProfilePageView, TrainerDetailPageView, ProfileAddPageView, TrainerPortfolioView, search, PtMembershipManagementPageView, profile_save
#from .views import TrainerPageView, OwnerPageView, TrainerRequestSuccessView
from . import views


app_name = 'gyms'

urlpatterns = [
    #path('trainer/', TrainerPageView.as_view(), name='trainer_page'),
    #path('owner/', OwnerPageView.as_view(), name='owner_page'),
    
    path('trainer/PT_management/', PtMembershipManagementPageView.as_view(), name='pt_membership_management_page'),
    path('trainer/PT_management/profile/', ProfilePageView.as_view(), name='profile_page'),
    path('trainer/PT_management/profile/user_num/<int:id>/', TrainerDetailPageView.as_view(), name='trainer_detail_page'),
    path('trainer/PT_management/profile_add/user_num/<int:id>/', ProfileAddPageView.as_view(), name='profile_add_page'),
    path('trainer/PT_management/profile_save/<int:id>/', profile_save, name='user_profile_save'),
    # path('trainer/portflio/', TrainerPortfolioView.as_view(), name='trainer_portflio_page'),
    # path('trainer/PT_membership_management/profile/search/', search, name='member_profile_search_page'),
    path('trainer/request-trainer-role/', views.request_trainer_role, name='request_trainer_role'),
    path('trainer/approve-trainer-request/<int:request_id>/', views.approve_trainer_request, name='approve_trainer_request'),
    #path('trainer/request-success/', views.TrainerRequestSuccessView.as_view(), name='trainer_request_success'),
]
