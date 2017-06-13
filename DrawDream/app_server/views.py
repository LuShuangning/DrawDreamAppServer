from django.shortcuts import render
from app_server import models
import json
from django.core import serializers

# Create your views here.


def login(request):
    accounts = models.Account.objects.all()
    login_dict = {}
    print(serializers.serialize('json', models.Account.objects.all()))

    return render(request, 'app_server/login.html', {'account': accounts})
