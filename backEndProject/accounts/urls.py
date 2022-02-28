from django.urls import path
from . import views, googleapi

urlpatterns = [
    path('google/login', googleapi.google_login, name='google_login'),
    path('google/callback', googleapi.google_callback, name='google_callback'),
    path('google/login/finish/', googleapi.GoogleLogin.as_view(), name='google_login_todjango'),
]