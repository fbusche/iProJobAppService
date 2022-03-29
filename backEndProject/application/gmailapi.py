import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
from application import quickstart
from settings import credentials, service_account_credentials
from application.services import gmail_authenticate
from googleapiclient.errors import HttpError
from google.cloud import pubsub_v1

API_KEY = credentials.GOOGLE_API_KEY


def get_labels(request):
    # get the Gmail API service
    email = request.user
    print(email)
    try:
        # Call the Gmail API
        service = gmail_authenticate()
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        
    return JsonResponse({'lables':labels})

def gmail_push(request):
    # TODO(developer)
    project_id = service_account_credentials.pro
    topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    topic = publisher.create_topic(request={"name": topic_path})

    print(f"Created topic: {topic.name}")
