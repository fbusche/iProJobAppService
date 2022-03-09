from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import JSONParser

from accounts.serializers import UserSerializer
from .models import Application, Status
from .services import linkedin_job_scrape
from .serializers import ApplicationSerializer

# Create your views here.

@permission_classes([IsAuthenticated])
def application(request):
    if request.method == 'GET':
        applications = Application.objects.select_related().filter(applicant=request.user)
        return JsonResponse({'application':ApplicationSerializer(applications, many=True).data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_application(request):
    if request.method == 'PUT':
        user = request.user
        data = JSONParser().parse(request)

        url = data['url']
        job_info = linkedin_job_scrape(url)

        application = Application(
            company = job_info['company'],
            position = job_info['position'],
            location = job_info['location'],
            status = Status.objects.get(id=1),
            job_post = url,
            applicant = user
        )
        application.save()

        return JsonResponse({'application': ApplicationSerializer(application).data, 'user':UserSerializer(user).data, 'message':'done'})

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_application(request, id):
    user = request.user
    applications = Application.objects.select_related().filter(applicant=user)
    application = applications.get(id=id)

    if request.method == 'PUT':
        data = JSONParser().parse(request)

        company = data.get('company', None)
        position = data.get('position', None)
        location = data.get('location', None)
        status = data.get('status', None)
        job_post = data.get('job_post', None)
        note = data.get('note', None)

        if company != None:
            application.company = company
        if position != None:
            application.position = position
        if location != None:
            application.location = location
        if status != None:
            application.status = Status.objects.get(name=status)
        if job_post != None:
            application.job_post = job_post
        if note != None:
            application.note = note
        application.save()

        return JsonResponse({'application':ApplicationSerializer(application).data, 'message':'Succesfully updated application'})
    
    if request.method == 'DELETE':
        application.delete()
        return JsonResponse({'message': 'Deletion success.'})
