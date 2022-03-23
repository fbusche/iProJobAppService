import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
from application import quickstart
from settings import credentials
from application.services import gmail_authenticate


API_KEY = credentials.GOOGLE_API_KEY

# def test(request):
#     quickstart
#     return Http


def get_labels(request):
    # get the Gmail API service
    service = gmail_authenticate()
    label_list = service.users().lables().list()
    print(label_list)
    # return JsonResponse({'label list':})

def test_redirect(request):
    HttpResponse('Success')