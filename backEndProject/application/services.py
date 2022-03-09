import requests, re, json

from bs4 import BeautifulSoup

from django.http import JsonResponse
import urllib3


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