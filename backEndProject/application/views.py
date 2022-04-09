from datetime import datetime
import re, json, os, datetime

from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import JSONParser

from accounts.serializers import UserSerializer
from accounts.models import Label

from .models import Application, Company, Status
from .services import linkedin_job_scrape
from .serializers import ApplicationSerializer
from .gmailapi import get_labels, get_new_mails, new_mail_detail

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
        
        try:
            company = Company.objects.get(name=job_info['company'])
        except:
            company = Company(name=job_info['company'])
            company.save()
        
        application = Application(
            company = company,
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
        company_email = data.get('company_email', None)

        if company != None:
            try:
                company = Company.objects.get(name=company)
            except:
                company = new_company = Company(name=company)
                new_company.save()
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
        if company_email != None:
            company = application.company
            company_email = re.search('(?<=@).*(?=\.)', company_email).group(0)
            company.company_email = company_email
            company.save()
        application.save()

        return JsonResponse({'application':ApplicationSerializer(application).data, 'message':'Succesfully updated application'})
    
    if request.method == 'DELETE':
        application.delete()
        return JsonResponse({'message': 'Deletion success.'})
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_label(request):
    user = request.user
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        label_name = data['label']
        label_info =  get_labels(request, label_name)
        new_label = Label()

        if label_info:
            new_label = Label(
                user = user,
                name = label_name,
                id = label_info
            )
            new_label.save()
            return JsonResponse({'message':f'Label "{label_name}" succesfully added.'})
        else:
            JsonResponse({'message':'Label does not exist. Make sure you have the label with the same name in your gmail account.'})
        

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_label(request, id):
    if request.method == 'DELETE':
        user_label = Label.objects.select_related().filter(user=request.user)
        label = user_label.get(id=id)
        label.delete()
        return JsonResponse({'message': 'Deletion success.'})


@permission_classes([IsAuthenticated])
def new_mail_checking(request):
    q = 'is:unread'

    applied_companies = Application.objects.select_related().filter(status=2).values_list('company__company_email')
    email_list = list(applied_companies)
    for email in email_list:
        if email[0] != '':
            q += f' from:{email[0]}'
    
    new = get_new_mails(q)
    new_messages = new.get('messages', [])
    total = new['resultSizeEstimate']

    if total > 1:
        print(f'New {total} follow-ups are waiting for you! Update your application status. {datetime.datetime.now()}')
        return JsonResponse({'message':f'New {total} follow-ups are waiting for you! Update your application status.'})
    else:
        new_message_info = new_mail_detail(new_messages[0]['id'])
        email = new_message_info['payload']['headers'][0]['value']
        # print(re.search('(?<=@).*(?=\.)', email).group(0))
        company = Company.objects.get(company_email=re.search('(?<=@).*(?=\.)', email).group(0))
        print(f'Check new message from {company.name}! {datetime.datetime.now()}')
        return JsonResponse({'meesage':f'Check new message from {company.name}!'})

