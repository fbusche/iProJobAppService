from django.shortcuts import render
from Mymodel.models import profile


def Profile(request):
    List = profile.objects.get(id=1)
    Data = {
        "name": List.Name,
        "email": List.Email,
        "img": List.img,
        "age": List.Age,
        "college": List.College,
        "address": List.Address,
        "interviews": List.Interviews,
        "year": List.Year,
        "joboffers": List.Joboffers,
        "jobsapplied": List.JobsApplied,
    }
    return render(request, 'profile.html', Data)


def Editprofile(request):
    List = profile.objects.get(id=1)
    Data = {
        "img": List.img,
        "interviews": List.Interviews,
        "joboffers": List.Joboffers,
        "jobsapplied": List.JobsApplied,
    }
    return render(request, 'profile-edit.html', Data)