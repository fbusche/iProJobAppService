from django.urls import path
from . import views, gmailapi, quickstart

urlpatterns = [
    path('job/', views.application),
    path('addjob/', views.add_application),
    path('editjob/<int:id>/', views.edit_application),
    path('labels/', gmailapi.get_labels),
    path('labels/add/', views.add_label),
    path('labels/delete/<int:id>', views.delete_label),
    path('notification/', gmailapi.gmail_push),
]