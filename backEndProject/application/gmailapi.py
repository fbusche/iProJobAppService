from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser

from googleapiclient.errors import HttpError
from google.cloud import pubsub_v1

from settings import credentials
from application.services import gmail_authenticate
from accounts.models import Label
from accounts.serializers import LabelSerializer

API_KEY = credentials.GOOGLE_API_KEY
service = gmail_authenticate()

def get_labels(request, label_name):
    # get the Gmail API service
    try:
        # Call the Gmail API
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

def gmail_push(request):
    user = request.user
    if request.method == 'GET':
        label = Label.objects.get(user=user)
        # print(label.id)
        results = service.users().messages().list(userId='me', labelIds=[label.id], q='is:unread').execute()
        messages = results.get('messages', [])
        print(messages)
        # project_id = credentials.PROEJCT_ID
        # topic_id = credentials.TOPIC_ID
        # subscription_id = credentials.SUBSCRIPTION_ID

        # # TODO(developer)
        # # project_id = "your-project-id"
        # # topic_id = "your-topic-id"

        # publisher = pubsub_v1.PublisherClient()
        # topic_path = publisher.topic_path(project_id, topic_id)
        # subscriber = pubsub_v1.SubscriberClient()
        # subscription_path = subscriber.subscription_path(project_id, subscription_id)

        # topic = publisher.create_topic(request={"name": topic_path})

        # print(f"Created topic: {topic.name}")
        
        # user = request.user
        # label = Label.objects.select_related().get(user=user)
        # label_id = [label.id]
        # topic_name = credentials.TOPIC_NAME
        
        
        # body = {
        #     'labelIds': label_id,
        #     "labelFilterAction": 'include',
        #     'topicName': topic_name
        # }
        # result = service.users().watch(userId='me', body=body).execute()
        # print(result)

