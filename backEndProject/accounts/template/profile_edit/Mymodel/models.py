from django.db import models

# Create your models here.

class profile(models.Model):
    Name = models.CharField(max_length=20)
    College = models.CharField(max_length=30)
    Email = models.CharField(max_length=30)
    Year = models.CharField(max_length=30)
    Age = models.CharField(max_length=30)
    Address = models.CharField(max_length=30)
    JobsApplied = models.CharField(max_length=30)
    Interviews = models.CharField(max_length=30)
    Joboffers = models.CharField(max_length=30)
    img = models.CharField(max_length=200)
