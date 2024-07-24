from django.urls import path
from .views import RegisterView, LoginView, home_view, profile_view, check_email_duplicate, update_nfc_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('check-email/', check_email_duplicate, name='check_email_duplicate'),
    # path('verify-email/<int:user_id>/', verify_email, name='verify_email'),
    # path('send-verification-code/', send_verification_code, name='send_verification_code'),
    path('update_nfc/', update_nfc_view, name='update_nfc'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
