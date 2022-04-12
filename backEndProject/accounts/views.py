import json
import os
from tokenize import Token
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer

# Create your views here.

credential_file = os.path.join(os.path.dirname(__file__), '../settings/client_secret.json')
credentials = json.load((open(credential_file)))

client_id = credentials['web']['client_id']
api_url = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=http://localhost:8000&client_id=' + client_id


@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    if request.method == 'GET':
        token = Token.objects.get(user=user)
        return JsonResponse({'user': UserSerializer(user).data, 'token': token.key})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_eidt(request): # will merge with profile def later
    user = request.user
    if request.method == 'PUT':
        data = JSONParser().parse(request)

        phone = data.get('phone', None)
        first_name = data.get('first_name', None)
        last_name = data.get('lat_name', None)
        age = data.get('age', None)
        school_year = data.get('school_year', None)
        gpa = data.get('gpa', None)
        
        if phone != None:
            user.phone = phone
        if first_name != None:
            user.first_name = first_name
        if last_name != None:
            user.last_name = last_name
        if age != None:
            user.age = age
        if school_year != None:
            user.school_year = school_year
        if gpa != None:
            user.gpa = gpa
        user.save()

        return JsonResponse({'message':'SUCCESFULLY_UPDATED_USER', 'user':UserSerializer(user).data})