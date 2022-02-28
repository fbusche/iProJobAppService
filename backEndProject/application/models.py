from operator import mod
from pyexpat import model
from django.db import models

# Create your models here.

class Application(models.Model):
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    location = models.CharField(max_length=255) # should convert to PlainLocation Feild later
    date_created = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    # status = fk
    job_post = models.URLField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    # applicant = fk

class Status(models.Model):
    name = models.CharField(max_length=30)