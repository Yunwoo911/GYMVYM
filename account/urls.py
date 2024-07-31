from django.urls import path
from .views import RegisterView, LoginView, ProfileUpdateView, home_view, profile_view, check_email_duplicate, verify_email, send_verification_code, profile_update_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', home_view, name='home2'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update_view, name='profile_update'),
    path('profile/api/update/', ProfileUpdateView.as_view(), name='profile_update_api'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('check-email/', check_email_duplicate, name='check_email_duplicate'),
    path('verify-email/<int:user_id>/', verify_email, name='verify_email'),
    path('send-verification-code/', send_verification_code, name='send_verification_code'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
