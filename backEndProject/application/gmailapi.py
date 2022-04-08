from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser

from googleapiclient.errors import HttpError
from google.cloud import pubsub_v1

from settings import credentials
from application.services import gmail_authenticate
from accounts.models import Label
from accounts.serializers import LabelSerializer

API_KEY = credentials.GOOGLE_API_KEY

def get_labels(request, label_name):
    # get the Gmail API service
    try:
        # Call the Gmail API
        service = gmail_authenticate()
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            return None
        for label in labels:
            if label['name'] == label_name:
                return label['id']
        return None

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        
    # return names
    # return JsonResponse({'lables':labels}) 

# def pub_sub(request):
#     # TODO(developer)
#     project_id = credentials.PROEJCT_ID
#     topic_id = credentials.TOPIC_ID

#     publisher = pubsub_v1.PublisherClient()
#     topic_path = publisher.topic_path(project_id, topic_id)

#     topic = publisher.create_topic(request={"name": topic_path})

#     print(f"Created topic: {topic.name}")

def get_new_mails(request, q):
    service = gmail_authenticate()
    user = request.user
    results = service.users().messages().list(userId='me', q=q).execute()
    return results

def new_mail_detail(request, id):
    service = gmail_authenticate()
    results = service.users().messages().get(userID='me', id=id).execute()