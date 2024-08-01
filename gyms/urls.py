from django.urls import path
from .views import TrainerDetailPageView, ProfileAddPageView, search, profile_save, profile_page, TrainerPortfolioView
from . import views

app_name = 'gyms'

urlpatterns = [    
    path('trainer/profile/', profile_page, name='profile_page'),
    path('trainer/profile/user_num/<int:id>/', TrainerDetailPageView.as_view(), name='trainer_detail_page'),
    path('trainer/profile_add/user_num/<int:id>/', ProfileAddPageView.as_view(), name='profile_add_page'),
    path('trainer/profile_save/<int:id>/', profile_save, name='user_profile_save'),
    path('trainer/portflio/', TrainerPortfolioView.as_view(), name='trainer_portflio_page'),
    path('trainer/profile/search/', search, name='member_profile_search_page'),
    path('trainer/request-trainer-role/', views.request_trainer_role, name='request_trainer_role'),
    path('trainer/approve-trainer-request/<int:trainer_request_id>/', views.approve_trainer_request, name='approve_trainer_request'),
    path('trainer/request-success/', views.TrainerRequestSuccessView.as_view(), name='trainer_request_success'),
    path('trainer/reject_trainer_request/<int:trainer_request_id>/', views.reject_trainer_request, name='reject_trainer_request'),
    # path('trainer-requests/', TrainerRequestListView.as_view(), name='trainer_requests_list'),
]
