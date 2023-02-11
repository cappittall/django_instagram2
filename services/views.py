from os import stat, stat_result
import time
from django.contrib import auth
from django.contrib.auth.models import User
import requests

from user.models import OtherInfo,InstagramCookies
from requests import api
from services.models import Services
from django.http import response
from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ServicesSerializer,UserSerializer
from .models import HostKeys, Services, Keys, Orders
from custom_admin.models import Proxy
import random
import threading
from custom_admin.models import Proxy,SeoSettings,AutoLikeUser,GetFollowDataLog
from .models import Affirmations
from pathlib import Path
from core.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from services.models import ServicesSuccessfulLog
import uuid
from custom_admin.models import VideoSayacLog
BASE_DIR = Path(__file__).resolve().parent.parent


def sendMailFile(subject,content,email,attach,attach2,follow_user):
    msg = EmailMessage(subject,content,EMAIL_HOST_USER, [email])

    msg.attach('{}_follower_list_username.txt'.format(follow_user), attach.read(), 'text/plain')
    msg.attach('{}_follower_list_user_id.txt'.format(follow_user), attach2.read(), 'text/plain')
    
    msg.send()

def sendMail2(subject,content,email):
    msg = EmailMessage(subject,content,EMAIL_HOST_USER, [email])
    msg.send()

def sendMail(subject,content,email):
    msg = EmailMultiAlternatives(subject,content,EMAIL_HOST_USER, [email])
    msg.attach_alternative(content, "text/html")
    msg.send(fail_silently=False)


def orderCancelControl(id):

    order_ = Orders.objects.filter(id=id).last()
    if order_:

        return order_.cancelled

    else:
        return False
def get_followers_data(username,quantity):
    pass

def getServices(request):
    pass

def generateKey(request):
    pass
def outData(request):
    pass
def outUserInfo(request):
    pass
