import requests, re, os.path, pickle

from bs4 import BeautifulSoup

from django.http import JsonResponse
from django.core.exceptions import ValidationError
from settings import credentials

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors
from email.message import EmailMessage



def linkedin_job_scrape(url):
    # url = "https://www.linkedin.com/jobs/view/2882566805/?alternateChannel=search&refId=oeuThlhJUGw6MCN%2Fx3qkfw%3D%3D&trackingId=j48fIHAW5AAT6qQxLYiY8A%3D%3D&trk=d_flagship3_job_details"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_info = soup.title.contents[0]
    info_dic = {
        'company': re.search('.*(?= hiring)', job_info).group(0),
        'position': re.search('(?<= hiring ).*(?= in)', job_info).group(0),
        'location': re.search('(?<=in ).*(?= \|)', job_info).group(0)
    }
    print((info_dic))

    return info_dic

def gmail_authenticate():
    creds = None
    SCOPES = ['https://mail.google.com/']
    if os.path.exists('token.json'):
        # with open('token.json', "rb") as token:
        #     creds = pickle.load(token)
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credential_file = os.path.join(os.path.dirname(__file__), '../settings/client_secret.json')
            flow = InstalledAppFlow.from_client_secrets_file(credential_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open('token.json', 'w') as token:
            # pickle.dump(creds, token)
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


# def google_get_access_token(request):
#     code = request.GET.get('code')
#     client_id = credentials.GOOGLE_OAUTH2_CLIENT_ID
#     client_secret = credentials.GOOGLE_OAUTH2_CLIENT_SECRET
#     BASE_URL = 'http://localhost:8000/'
#     GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'
#     state = credentials.STATE
    
#     token_response = requests.post(
#         f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
#     print(token_response.json())

#     if not token_response.ok:
#         raise ValidationError('google_token is invalid')
    
#     access_token = token_response.json().get('access_token')
    
#     return access_token
