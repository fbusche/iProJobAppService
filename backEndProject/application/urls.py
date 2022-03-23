from django.urls import path
from . import views, gmailapi, quickstart

urlpatterns = [
    path('job/', views.application),
    path('addjob/', views.add_application),
    path('editjob/<int:id>/', views.edit_application),
    path('labels/', gmailapi.get_labels),
    path('redirect/', gmailapi.test_redirect)
]