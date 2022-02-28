import json
import os
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser

# Create your views here.

credential_file = os.path.join(os.path.dirname(__file__), '../settings/client_secret.json')
credentials = json.load((open(credential_file)))

client_id = credentials['web']['client_id']
api_url = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=http://localhost:8000&client_id=' + client_id


def get_crednetials(request):
    scope = "https://www.googleapis.com/auth/gmail.readonly"
    url = api_url + ('&scope=' + scope)
    print(url)

    return HttpResponse('good')
