import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
from settings import credentials

API_KEY = credentials.GOOGLE_API_KEY


def get_labels(request):
    user = request.user
    print(user.email)
    # scope = 'https://www.googleapis.com/auth/gmail.modify'
    scope = f"https://gmail.googleapis.com/gmail/v1/users/{user.email}/labels?key={API_KEY}"
    rd = requests.get(scope).text

    return HttpResponse(rd)