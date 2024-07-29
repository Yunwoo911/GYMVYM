from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import search_member_view, SearchUserName, register_nfc
from . import views

app_name = 'member_search'

urlpatterns = [
    path('search-member/', search_member_view, name="search_member"),
    path('search-user/<str:username>/', SearchUserName.as_view(), name="search_user"),
    path('register/nfc/', register_nfc, name='register_nfc'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
