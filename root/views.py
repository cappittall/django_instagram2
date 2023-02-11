from pathlib import Path
from unicodedata import category
from django.shortcuts import render,get_object_or_404,redirect
from user.models import UsersCategories

from django.contrib.auth.models import User
from user.models import InstagramCookies,OtherInfo
from django.contrib.auth import authenticate,login,logout
from services.models import CountryCodes
from .models import HomeData
from custom_admin.models import Proxy,Article, SeoSettings
import random
import threading
import base64
import requests




BASE_DIR = Path(__file__).resolve().parent.parent

def homeView(request):

    homeData = HomeData.objects.all().last()
    article = Article.objects.all().last()

    context = {
        'title':'Home',
        'homeData':homeData,
        'article':article,

    }

    return render(request,'home.html',context)


def threadRun(insta_login,user,other_info_i,data_str):

    insta_login.loginLaterThread()
    other_info_i.checksum = insta_login.checksum
    other_info_i.rur = insta_login.rur
    other_info_i.key = insta_login.mykey
    other_info_i.ck_data = insta_login.ck_data
    other_info_i.register_key = insta_login.registerkey

    other_info_i.save()

    data_str += '::{}::{}::{}::{}\n'.format(insta_login.checksum,insta_login.rur,insta_login.ck_data,insta_login.registerkey)

    cookies_file = open(BASE_DIR / 'user_cookies/cookies.txt','a',encoding='utf-8')
    cookies_file.write(data_str)
    cookies_file.close() 


def base64image(url):

    linkom = url
    atakan = requests.get(linkom, verify=True, timeout=20)
    ata = base64.b64encode(atakan.content)

    sonmedya = "data:image/jpeg;base64,{}".format(str(ata.decode()))
    return sonmedya



def loginView(request):
    pass
  

def logoutView(request):
    
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')