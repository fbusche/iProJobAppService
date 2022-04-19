import json
import os
from tokenize import Token
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.authtoken.models import Token

from application.models import Application
from .serializers import UserSerializer

# Create your views here.

credential_file = os.path.join(os.path.dirname(__file__), '../settings/client_secret.json')
credentials = json.load((open(credential_file)))

client_id = credentials['web']['client_id']
api_url = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=http://localhost:8000&client_id=' + client_id


def login(request):
    if not request.user.is_authenticated or request.user.is_admin:
        return render(request, 'login.html')
    else:
        return render(request, 'trackerBoard.html')


@permission_classes([IsAuthenticated])
def profile(request):
    # token = Token.objects.get(user=user)
    user = request.user
    applications = Application.objects.filter(applicant=user)
    applied = applications.filter(status__name = "applied").count()
    interviewd = applications.filter(status__name = "interviewed").count()
    offered = applications.filter(status__name = "offer").count()
    return render(request, 'profile.html', {'user': user, 'applied': applied, 'interviwed':interviewd, 'offered':offered})
    # return JsonResponse({'user': UserSerializer(user).data, 'token': token.key})

@permission_classes([IsAuthenticated])
def edit_view(request):
    user = request.user
    return render(request, 'profile-edit.html')

# @api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_edit(request): # will merge with profile def later
    # if request.method == 'PUT':
    user = request.user
    # data = JSONParser().parse(request)
    print(request.POST)
    phone = request.POST.get('phone')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    age = request.POST.get('age')
    school_year = request.POST.get('school_year')
    gpa = request.POST.get('gpa')
    
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

    return HttpResponse('done')
    return render(request, 'profile.html')
    # return JsonResponse({'message':'SUCCESFULLY_UPDATED_USER', 'user':UserSerializer(user).data})