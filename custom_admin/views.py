from hashlib import new
from django.db.models.fields import IntegerField

from django.contrib import auth
import requests
from requests import api

from root.models import HomeData
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect

from user.models import InstagramCookies,OtherInfo,UsersCategories
from django.contrib.auth.models import User
import threading
from services.models import CountryCodes, Genders, HostKeys, Orders,Keys, ServiceCategory, Services, UserPackpages,ServicesSuccessfulLog,Affirmations
import binascii,os
from .forms import ImportFileForm, UpdatePackpageform,UpdateServiceform, UserCategoriesForm,seoFilesForm,ArticleForm,MentionForm,UsersScannerForm
from django.core.paginator import Paginator
import random
from django.http import Http404
from django.contrib.auth import authenticate,login,logout
import time
import json
from .forms import SmtpForm
from .models import MailSMTPInfo

import os


from custom_admin.models import AutoLikeUser
import base64
from .models import AutoFollowUser, ImportFiles,Proxy, SeoSettings,GetFollowDataLog,Article,Mentions, UsersScanner
import datetime
from core.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from pathlib import Path
from django.db.models import F


BASE_DIR = Path(__file__).resolve().parent.parent

## my codes hc
from api.models import InstagramAccounts, OrderList, InstagramVersions, Profil
from collections import defaultdict
from api.static.choices import choices
from api.static.choices import apps_islemleri
from rest_framework.authtoken.models import Token

# django decoration @ for login required and user is superuser
from django.contrib.auth.decorators import login_required, user_passes_test
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio
            
            
            
 
 
def send_order_to_phones(data):
   
    message={
        "action":"serverAction",
        "sender":data.pop('sender'),
        "receivers": data.pop('receivers'),
        "message": data,        
    }
    room_group_name = 'inchat'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'chat_message',
            'message': message,
        }
    )  
        
    
        
    
         
def threadingProceedOrder(data, comments, quantity, order):    
    data['receivers']= []
    subLocality = data.get('subLocality', None)
    locality = data.get('locality', None)
    country= data.get('country', None)
    # get instagram accounts
    if subLocality:
        instagram_accounts= InstagramAccounts.objects.filter(subLocality=subLocality)
    elif locality:
        instagram_accounts= InstagramAccounts.objects.filter(locality=locality)
    elif country:
        instagram_accounts= InstagramAccounts.objects.filter(country=country)
    else:
        instagram_accounts= InstagramAccounts.objects.all()
        
    # sort instagram accounts by user profil update_time (last recent first)
    sorted_instagram_accounts = instagram_accounts.order_by('-profil__update_time')

    insta_counter=0 
    total_instagram_acc_count = sorted_instagram_accounts.count()
    OrderList.objects.filter( id=int(data['order_id']) ).update(start_count=total_instagram_acc_count)
    user_ids = defaultdict(list)
    xx=[user_ids[str(x.profil.user.id)].append(x.id) for x in sorted_instagram_accounts]
    print('>> user ids...: ', xx, user_ids, ' -> ',list(user_ids.keys()))
        
    # if the number of accounts is less than the quantity, send to all accounts
    if total_instagram_acc_count < quantity:
        #remove dublicate ids.
        data['receivers'] = [int(i) for i in user_ids.keys()]
        if comments:
            commentsObj={}
            cnr=0
            #ias: instagram accounts array, uid: user id
            for uid, ias in user_ids.items(): 
                for ia in ias:
                    commentsObj[str(ia)]=comments[cnr]
                    # check if comments array finished then start from first comment
                    cnr += 1
                    if cnr < len(comments)-1:
                        cnr=0
            data['comments']=commentsObj 
        ## Initial send request to websocket server

        asyncio.run_coroutine_threadsafe(send_order_to_phones(data))
        
    # if the number of accounts is more than the quantity, send to the first accounts equaly to the quantity
    else:
        commentsObj, cc=({},0)
        # looping user_ids: {user_id: [insta_id, insta_id, ...], user_id: [insta_id, insta_id, ...], ...}
        temp_user_ids = user_ids.copy()
        for key, value in user_ids.items():
            data['receivers'].append(int(key))
            if comments:
                # create: {insta_id: comment, insta_id: comment, ...}
                for val in value:
                    print('>>>>>>>',val, comments, cc)
                    commentsObj[str(val)]=comments[cc]
                    cc += 1
                    if cc > len(comments)-1: cc=0
                
            insta_counter += len(value)
            # remove selected ids from user_ids
            del temp_user_ids[key]
            if insta_counter >= quantity:
                break
        user_ids = temp_user_ids
        # set comments to data
        data['comments']=commentsObj
        ## Initial send request to websocket server
        asyncio.run_coroutine_threadsafe(send_order_to_phones(data))
        
        while user_ids:
            # wait for 60 seconds in order to check order is completed or not
            time.sleep(60)
            data['receivers']= []
            # check the order is completed or not
            remain = OrderList.objects.filter(id=order.id).last().remains
            # if remain is 0, the order is completed
            if remain <= 0: break
            insta_counter=0
            commentsObj, cc=({},0)
            
            # looping user_ids: {user_id: [insta_id, insta_id, ...], user_id: [insta_id, insta_id, ...], ...}
            temp_user_ids = user_ids.copy()
            for key, value in user_ids.items():
                data['receivers'].append(int(key))
                if comments:
                    # create: {insta_id: comment, insta_id: comment, ...}
                    for val in value:
                        commentsObj[str(val)]=comments[cc]
                        cc += 1
                        if cc > len(comments)-1: cc=0
                
                insta_counter += len(value)
                # remove selected ids from user_ids
                del temp_user_ids[key]
                if insta_counter >= remain:
                    break  
            user_ids = temp_user_ids.copy() 
            # set comments to data
            data['comments']=commentsObj
            asyncio.run_coroutine_threadsafe(send_order_to_phones(data))
    # render instagramSiparisler page



@login_required
@user_passes_test(lambda u: u.is_superuser)
def instagramGenel(request):
    starting = False
    instagram_accounts= InstagramAccounts.objects.all()
    context = {
        'title':'İnstagram Genel İşlemler',
        'start_count': instagram_accounts.count(),
        'country': list(instagram_accounts.values('country').distinct()),
        'locality': list(instagram_accounts.values('locality').distinct()),
        'subLocality': list(instagram_accounts.values('subLocality').distinct()),
        'starting':starting,
        'service_lists':choices,
        'filtered_accounts':[],
        'instagram_accounts':json.dumps(list(InstagramAccounts.objects.values('country_code', 'country', 'locality', 'subLocality')))
    }
    if "btnStart" in request.POST:
        
        print(request.POST)
        action = request.POST['islem_turu'] 
        link = request.POST['link'] if 'link' in request.POST else ''
        country = request.POST['country_name'] if 'country_name' in request.POST else None
        locality = request.POST['locality_name'] if 'locality_name' in request.POST else None
        subLocality = request.POST['sublocality_name'] if 'sublocality_name' in request.POST else None
        comments_text = request.POST['comments'] if 'comments' in request.POST else ''
        comments = comments_text.splitlines() if comments_text else []
        quantity = int(request.POST['takipci_quantity'])  or len(comments)
        start_count = int(request.POST['start_count_input']) if 'start_count_input' in request.POST else 0
        is_free = bool(request.POST['isFree']) if 'isFree' in request.POST else False
        apikey = request.user.profil.token   
        data={}
        print("action: ", action, "isFree", is_free,  "link: ", link, "comments: ", comments, "quantity: ", quantity, "start_count: ", start_count, "apikey: ", apikey)
        # image or video file
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file'] 
            # save file content to local
            file_path = os.path.join(BASE_DIR, 'static', 'files', uploaded_file.name)
            data['filepath']=file_path
            # data['filebinary']=uploaded_file
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
                        
        order = OrderList.objects.create(user=request.user.profil,  action= action, service=choices[action], status="Pending" , 
                                              start_count=start_count, comments=comments_text, quantity=quantity, remains=quantity, link=link, key=apikey)
        
        # initial sets
        data['country']= country
        data['locality']= locality
        data['subLocality']= subLocality
        data['apikey']= apikey
        data['action']= action 
        data['sender']= [0]
        data['order_id']= order.id
        data['isFree']= is_free 
        data['link'] = link     
        message= threading.Thread(target=threadingProceedOrder, args=(data, comments, quantity, order,)).start()
        return redirect('custom_admin:instagram-siparisler')
                
    return render(request,'custom_admin/instagram_tools/instagram-genel.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def instagramSiparisler(request):
    instagrams= OrderList.objects.filter(user=request.user.profil)

    context={}
    context['title']='İşlem durumu... '
    context['sayisi']= instagrams.filter(status='Completed').count()
    context['successful_log_data']=instagrams
    return render(request,'custom_admin/instagram_tools/instagram-siparisler.html', context)

def deleteOrder(request, id):

    print('Silinecek order numarası : ',id) 
    print('Silinecek order numarası : ', request.POST) 
    OrderList.objects.filter(id=id).delete()
    return redirect('custom_admin:instagram-siparisler')

def sendMail2(subject,content,email):
    msg = EmailMessage(subject,content,EMAIL_HOST_USER, [email])
    msg.send()


def instagramApps(request):
    versions = InstagramVersions.objects.all().order_by('-id')[0]
    # for the first time
    if not versions: InstagramVersions.objects.create(version='0.0.0')
        
    context={
        "title":"Instagram App işlemleri",
        "apps_islemleri": apps_islemleri,
        "version": versions.version,
        "error":None,
    }
    print('Instagram apps context: ',context)
    if "btnStart" in request.POST:
        islem_turu= request.POST.get('islem_turu', None)
        version = request.POST.get('version', None)
        print('What is islem_turu : ',islem_turu,' version: ', version)
        
        if version:
            
            newversion= InstagramVersions.objects.create(version=version)
            if newversion: context['version']=version
            data={
                "action": islem_turu,
                "version": version,
                "sender": [0],
                "receivers": [0],
            }
            
            send_order_to_phones(data)
    return render(request,'custom_admin/instagram_tools/instagram-apps.html', context)
    

def dashboardView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        
        accounts = InstagramAccounts.objects.all() # (user__is_superuser=False)
        erkekUsers = accounts.filter(gender="1").count()
        kadinUsers = accounts.filter(gender="2").count()
        login_required_users = accounts.filter(error__isnull=False).count()
        all_country_codes = accounts.values('country_code').distinct()

        get_users_categories = UsersCategories.objects.all()
        category_users_len = []
        for x in get_users_categories:
            my_dict = {'total_users':0,'challenge_users':0,'feedback_users':0,'checkpoint_users':0,'active_users':0,'pasif_users':0}

            get_users = User.objects.filter(is_superuser=False,otherinfo__category=x.id)
            my_dict['total_users'] = get_users.count()
            my_dict['challenge_users'] = get_users.filter(instagramcookies__challenge=True).count()
            my_dict['feedback_users'] = get_users.filter(instagramcookies__feedback=True).count()
            my_dict['login_required_users'] = get_users.filter(instagramcookies__login_required=True).count()
            my_dict['checkpoint_users'] = get_users.filter(instagramcookies__checkpoint=True).count()
            my_dict['active_users'] = get_users.filter(instagramcookies__active=True).count()
            my_dict['pasif_users'] = get_users.filter(instagramcookies__active=False).count()

            category_users_len.append(my_dict)
        

        countryCodeList = []
        for x in all_country_codes:
            print('Checktht >>> ',x['country_code'])
            mydict = {
                'total_user':accounts.filter(country_code=x["country_code"]).count(),
                'erkek_user':accounts.filter(country_code=x["country_code"],gender="1").count(),
                'kadin_user':accounts.filter(country_code=x["country_code"],gender="2").count(),
                'country_code':x["country_code"],
                }

            countryCodeList.append(mydict)
        
        if 'btnCheckMyKey' in request.POST:
            pass


        context = {
            'title':'Kullanıcı Verileri',
            'erkek':erkekUsers,
            'kadin':kadinUsers,
            'total':len(accounts),
            'bot':len(accounts.filter(bot_user=True)),
            'reel':len(accounts.filter(default_user=True)),
            'countryCodeList':countryCodeList,
            'anonym':len(accounts) - (erkekUsers+kadinUsers),
            'user_categories_data':zip(get_users_categories,category_users_len),
            'login_required_users':login_required_users,

        }

        return render(request,'custom_admin/dashboard.html',context)
    else:
        raise Http404('not found')
    
    
    
    
    
    
    

def orderCancelControl(id):
    
    order_ = Orders.objects.filter(id=id).last()
    if order_:

        return order_.cancelled

    else:
        return False

def threadRunSavePost(us,auth_proxy,ip_port_proxy,x,quantity,total_quantity,order,user_media,errorFile,textUser):
    pass

def threadSavePost(quantity,user_order,photo_media,users_categories):
    savephotolog = {}
    
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  
    total_quantity = int(quantity)
    if len(userCookies) < quantity:
        total_quantity = len(userCookies)

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)

    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    print('total_quantity : ',total_quantity)
    
    if total_quantity < 1 :
        user_order.status = "Partial"
        user_order.remains = int(quantity) - user_order.successful_value
        user_order.cancelled = True
        user_order.save()

    userSayac = 0
    for x in range(0, total_quantity):

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]


        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        thread =  threading.Thread(target=threadRunSavePost,args=(us,process_auth_proxy,process_ip_port_proxy,x,quantity,total_quantity,user_order,photo_media,errorFile,us.user.username),daemon=True)  
        savephotolog[x] = thread
        savephotolog[x].start()

        threads.append(thread)
        
        cancellStatus = orderCancelControl(user_order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join()
                threads.clear()

        elif cancellStatus:
            user_order.status = "Partial"
            user_order.remains = int(quantity) - user_order.successful_value
            user_order.cancelled = True
            user_order.save()
            
            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(user_order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(user_order.successful_value))
            
            break



def savePhotoView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        
        if 'btnSend' in request.POST:
            photo_media = request.POST.get('media_link', None)
            quantity = request.POST.get('quantity', None)
            users_categories = request.POST.getlist('user_category')
            sv = get_object_or_404(Services, category__category_name="Fotoğraf Kaydetme")

            user_order = Orders.objects.create(user=request.user,target=photo_media,status="Pending",service=sv,charge=float(sv.rate),user_order=True)

            def orderControl(user_order):
                last_seo = SeoSettings.objects.all().last()
                whileStatus = True
                while whileStatus:
                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:
                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()

                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadSavePost,args=(int(quantity),user_order,photo_media,users_categories))
                                t1.start()
                                whileStatus = False

                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True

        context = {
            'title':'Fotoğraf Kaydetme',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/savephotos.html',context)


def threadRunLiveWatch(us,auth_proxy,ip_port_proxy,x,order,live_user,quantity,total_quantity,watch_type,errorFile,textUser):
    pass

def threadLiveWatch(quantity,order,username,watch_type,users_categories):
    livewatchlog = {}
    quantity = int(quantity)      
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    total_quantity = quantity
    if len(userCookies) < quantity:
        total_quantity = len(userCookies)

    login_after_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_after_proxy=True)
    login_after_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_after_proxy=True)
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    
    print('total_quantity : ',total_quantity)
    
    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
        print("işlem no : ",str(x))

        login_after_ip_port_proxy = None
        login_after_auth_proxy = None

        if login_after_ip_port_proxy_list:

            login_after_ip_port_proxy = login_after_ip_port_proxy_list[random.randrange(len(login_after_ip_port_proxy_list))]
        if login_after_auth_proxy_list:

            login_after_auth_proxy = login_after_auth_proxy_list[random.randrange(len(login_after_auth_proxy_list))]


        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        livewatchlog[x]=  threading.Thread(target=threadRunLiveWatch,args=(us,login_after_auth_proxy,login_after_ip_port_proxy,x,order,username,quantity,total_quantity,watch_type,errorFile,us.user.username))
        livewatchlog[x].start()



def sendWatchLiveView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            username = request.POST.get('username', None)
            quantity = request.POST.get('quantity', None)
            watch_type = int(request.POST['watch_type'])


            if username.find('.com/') != -1:
                username = username.split('.com/')[1].replace('/','')
                username = username.split('?igshid')[0]
            else:
                username = username.replace('/','')
        
            sv = get_object_or_404(Services, category__category_name="Canlı Yayın İzleme {} Dakika".format(watch_type))

            order = Orders.objects.create(user=request.user,target=username,service=sv,charge=float(sv.rate),status="Pending",user_order=True)
                
            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:
                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break
                    orderLast = Orders.objects.filter(status='Pending').last()
                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:
                        
                        if order.id == orderLast.id or last_seo.process_queue_disabled:

                            if order.cancelled:
                                order.status = 'Partial'
                                order.remains = quantity
                                order.save()
                                whileStatus = False
                            else:
                                order.status = 'In Progress'
                                t1 = threading.Thread(target=threadLiveWatch,args=(quantity,order,username,watch_type,users_categories),daemon=True)
                                t1.start()
                                whileStatus = False

                    time.sleep(5)

            t_o = threading.Thread(target=orderControl,args=(order,),daemon=True)
            t_o.start()  

            print('order oluşturuldu.',order.status)
            starting = True
    

        context = {
            'title':'Watch Live Stream',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/watch-live.html',context)



def threadRunLiveLike(us,auth_proxy,ip_port_proxy,x,order,live_user,quantity,total_quantity,errorFile,textUser):
    pass


def threadLiveLike(quantity,user_order,username,users_categories):
    pass
    livelikelog = {}
    last_seo = SeoSettings.objects.all().last()                  
    
    if users_categories:
        
        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
    
    quantity = int(quantity)
    total_quantity = quantity
    if len(userCookies) < quantity:
        total_quantity = len(userCookies)

    login_after_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    login_after_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    userSayac = 0    
    threads = []

    print('total_quantity : ',total_quantity)
    
    if total_quantity < 1 :
        user_order.status = "Partial"
        user_order.remains = int(quantity) - user_order.successful_value
        user_order.cancelled = True
        user_order.save()

    for x in range(0, total_quantity):

        login_after_ip_port_proxy = None
        login_after_auth_proxy = None

        if login_after_ip_port_proxy_list:

            login_after_ip_port_proxy = login_after_ip_port_proxy_list[random.randrange(len(login_after_ip_port_proxy_list))]
        if login_after_auth_proxy_list:

            login_after_auth_proxy = login_after_auth_proxy_list[random.randrange(len(login_after_auth_proxy_list))]


        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        thread =  threading.Thread(target=threadRunLiveLike,args=(us,login_after_auth_proxy,login_after_ip_port_proxy,x,user_order,username,quantity,total_quantity,errorFile,us.user.username))
        livelikelog[x] = thread
        livelikelog[x].start()

        threads.append(thread)
        
        cancellStatus = orderCancelControl(user_order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join()
                threads.clear()

        elif cancellStatus:
            user_order.status = "Partial"
            user_order.remains = int(quantity) - user_order.successful_value
            user_order.cancelled = True
            user_order.save()
            
            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(user_order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(user_order.successful_value))


            break


def sendLikeLiveView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        starting = False

        get_user_categories = UsersCategories.objects.all()
    
        if 'btnSend' in request.POST:

            username = request.POST.get('username', None)

            if username.find('.com/') != -1:
                username = username.split('.com/')[1].replace('/','')
                username = username.split('?igshid')[0]
            else:
                username = username.replace('/','')

            quantity = request.POST.get('quantity', None)
            sv = get_object_or_404(Services, category__category_name="Canlı Yayın Beğeni")

            user_order = Orders.objects.create(user=request.user,target=username,service=sv,charge=float(sv.rate),status="Pending",user_order=True)
            users_categories = request.POST.getlist('user_category')
            def orderControl(user_order):
                last_seo = SeoSettings.objects.all().last()   
                whileStatus = True
                while whileStatus:
                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False

                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadLiveLike,args=(quantity,user_order,username,users_categories))
                                t1.start()
                                whileStatus = False

                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
    

        context = {
            'title':'Like Live Stream',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }
        return render(request,'custom_admin/instagram_tools/like-live.html',context)

def threadRunLiveComment(us,auth_proxy,ip_port_proxy,x,comm,order,live_user,quantity,total_quantity,errorFile,textUser,users_categories):
    pass


def threadLiveComment(quantity,comment_list,order,live_user,users_categories):
    pass
def sendCommentLiveView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        starting = False

        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            username = request.POST.get('username', None)

            if username.find('.com/') != -1:
                username = username.split('.com/')[1].replace('/','')
                username = username.split('?igshid')[0]
            else:
                username = username.replace('/','')

            comments = request.POST.get('comments', None)
              
            comment_list = comments.splitlines()
            quantity = len(comment_list)
            sv = get_object_or_404(Services, category__category_name="Canlı Yayın Yorum")

            user_order = Orders.objects.create(user=request.user,target=username,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                last_seo = SeoSettings.objects.all().last()
                whileStatus = True
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break
                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadLiveComment,args=(quantity,comment_list,user_order,username,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True

        context = {
            'title':'Canlı Yayın Yorum',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/comment-live.html',context)


def threadRunDMMessage(us,auth_proxy,ip_port_proxy,x,order,quantity,total_quantity,dm_user,comm,errorFile,textUser,users_categories):
    pass


def threadDMMessage(quantity,comment_list,dm_user,order,users_categories):

    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    if quantity > len(userCookies):
        total_quantity = len(userCookies)

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    
    print('total_quantity : ',total_quantity)
    
    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        comm = comment_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,order,quantity,total_quantity,dm_user,comm,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break

def sendDMMessageView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
    
            username = request.POST.get('username', None)
            users_categories = request.POST.getlist('user_category')
            username = username.replace('https://www.instagram.com/','')
            username = username.replace('/','')

            messages = request.POST.get('messages', None)
            comment_list = messages.splitlines()
            quantity = len(comment_list)
            sv = get_object_or_404(Services, category__category_name="DM Mesaj")

            user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=username,status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMMessage,args=(quantity,comment_list,username,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True

        context = {
            'title':('DM Mesaj Gönder'),
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dm-message.html',context)


def threadRunDMIgTvTopluMessage(us,auth_proxy,ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass


def threadRunDMVideoTopluMessage(us,auth_proxy,ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass


def threadDMVideoTopluMessage(quantity,users_list,link,message,order,users_categories):
    dmmessagelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if quantity > len(userCookies):
        total_quantity = len(userCookies)

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        thread =  threading.Thread(target=threadRunDMVideoTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()
            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))

            break


def threadDMIgTvTopluMessage(quantity,users_list,link,message,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if quantity > len(userCookies):
        total_quantity = len(userCookies)

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMIgTvTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break


def threadRunDMReelTopluMessage(us,auth_proxy,ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass


def threadDMReelTopluMessage(quantity,users_list,link,message,order,users_categories):
    dmmessagelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if quantity > len(userCookies):
        total_quantity = len(userCookies)

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        thread =  threading.Thread(target=threadRunDMReelTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break



def threadRunDMResimTopluMessage(us,auth_proxy,ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass


def threadDMResimTopluMessage(quantity,users_list,link,message,order,users_categories):
    dmmessagelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if quantity > len(userCookies):
        total_quantity = len(userCookies)

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMResimTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break



def threadRunDMTopluMessage(us,auth_proxy,ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass


def threadDMTopluMessage(quantity,users_list,link,message,order,users_categories):
    pass

def sendDMTopluMessageView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            users = request.POST.get('users', None)

            link = request.POST.get('link', None)
            link = link.replace('https://','')
            link = link.replace('http://','')

            users_categories = request.POST.getlist('user_category')

            message = request.POST.get('message', None)
            users_list = users.splitlines()
            quantity = len(users_list)
            sv = get_object_or_404(Services, category__category_name="DM Toplu Link Mesaj")

            user_order = Orders.objects.create(user=request.user,target=link,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMTopluMessage,args=(quantity,users_list,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM Toplu Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dm-toplu-message.html',context)



def sendDMReelTopluMessageView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users = request.POST.get('users', None)
            link_message = request.POST.get('link_message', None)

            link_message = link_message.replace('https://','')
            link_message = link_message.replace('http://','')

            link_message_split = link_message.split(":")
            link = link_message_split[0]
            message = link_message_split[1]
            users_categories = request.POST.getlist('user_category')
            users_list = users.splitlines()
            quantity = len(users_list)
            sv = get_object_or_404(Services, category__category_name="DM Toplu Reel Mesaj")

            user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=link,status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMReelTopluMessage,args=(quantity,users_list,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM Reel Video Toplu Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dmreel-toplu-message.html',context)



def sendDMIgTvTopluMessageView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users = request.POST.get('users', None)
            link_message = request.POST.get('link_message', None)

            link_message = link_message.replace('https://','')
            link_message = link_message.replace('http://','')

            link_message_split = link_message.split(":")
            link = link_message_split[0]
            message = link_message_split[1]
            users_categories = request.POST.getlist('user_category')
            users_list = users.splitlines()
            quantity = len(users_list)
            sv = get_object_or_404(Services, category__category_name="DM Toplu IGTV Mesaj")

            user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=link,status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMIgTvTopluMessage,args=(quantity,users_list,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM IGTV Toplu Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dmigtv-toplu-message.html',context)




def sendDMVideoTopluMessageView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            users = request.POST.get('users', None)
            link_message = request.POST.get('link_message', None)
            
            link_message = link_message.replace('https://','')
            link_message = link_message.replace('http://','')

            link_message_split = link_message.split(":")
            link = link_message_split[0]
            message = link_message_split[1]

            users_list = users.splitlines()
            quantity = len(users_list)
            sv = get_object_or_404(Services, category__category_name="DM Toplu Videolu Mesaj")

            user_order = Orders.objects.create(user=request.user,target=link,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMVideoTopluMessage,args=(quantity,users_list,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM Video Toplu Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dmvideo-toplu-message.html',context)


def sendDMResimTopluMessageView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            users = request.POST.get('users', None)
            users_categories = request.POST.getlist('user_category')
            link_message = request.POST.get('link_message', None)
            link_message = link_message.replace('https://','')
            link_message = link_message.replace('http://','')

            link_message_split = link_message.split(":")
            link = link_message_split[0]
            message = link_message_split[1]

            users_list = users.splitlines()
            quantity = len(users_list)
            sv = get_object_or_404(Services, category__category_name="DM Toplu Resimli Mesaj")

            user_order = Orders.objects.create(user=request.user,target=link,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMResimTopluMessage,args=(quantity,users_list,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM Resim Toplu Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dmresim-toplu-message.html',context)


def threadRunLike(us,auth_proxy,ip_port_proxy,x,order,like_media,media_id,quantity,total_quantity,errorFile,textUser):
    pass


def threadLike(quantity,user_order,user_media,user_media_id,users_categories):
    userlikelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if len(userCookies) < quantity:
        total_quantity = len(userCookies)    

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    userSayac = 0
    print('total_quantity : ',total_quantity)
    
    if total_quantity < 1 :
        user_order.status = "Partial"
        user_order.remains = int(quantity) - user_order.successful_value
        user_order.cancelled = True
        user_order.save()       
    
    for x in range(0, total_quantity):
        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]


        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        
        thread =  threading.Thread(target=threadRunLike,args=(us,process_auth_proxy,process_ip_port_proxy,x,user_order,user_media,user_media_id,quantity,total_quantity,errorFile,us.user.username))
        userlikelog[x] = thread
        userlikelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(user_order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            user_order.status = "Partial"
            user_order.remains = int(quantity) - user_order.successful_value
            user_order.cancelled = True
            user_order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(user_order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(user_order.successful_value))


            break


def sendPostLikeView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if "btnStart" in request.POST:
           
            users_categories = request.POST.getlist('user_category')

            media_link = request.POST.get('media_link')
            media_link = 'www.instagram.com/' + media_link.split('.com/')[1]

            quantity = int(request.POST['quantity'])
            sv = get_object_or_404(Services, category__category_name="Beğeni")

            user_order = Orders.objects.create(user=request.user,target=media_link,service=sv,charge=float(sv.rate),status="Pending",user_order=True)
            media_link_id = None
            def orderControl(user_order):
                last_seo = SeoSettings.objects.all().last()
                whileStatus = True
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:
                        orderLast = Orders.objects.filter(status='Pending').last()

                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False

                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadLike,args=(quantity,user_order,media_link,media_link_id,users_categories))
                                t1.start()
                                whileStatus = False

                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True

        context = {
            'title':'Beğeni Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/send-postlike.html',context)


def threadRunComment(us,auth_proxy,ip_port_proxy,x,comm,quantity,comment_media,media_id,total_quantity,comment_list,user_order,errorFile,textUser,users_categories):
    pass



def threadComment(quantity,comment_list,comment_media,media_id,user_order,users_categories):
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if quantity > len(userCookies):
        total_quantity = len(userCookies)

    print(total_quantity)
    postcomlog = {}


    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    userSayac = 0    
    print('total_quantity : ',total_quantity)
    
    if total_quantity < 1 :
        user_order.status = "Partial"
        user_order.remains = int(quantity) - user_order.successful_value
        user_order.cancelled = True
        user_order.save()

    for x in range(0, total_quantity):
        comm = comment_list[x]
        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]


        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        thread = threading.Thread(target=threadRunComment,args=(us,process_auth_proxy,process_ip_port_proxy,x,comm,quantity,comment_media,media_id,total_quantity,comment_list,user_order,errorFile,us.user.username,users_categories))
        postcomlog[x] = thread
        postcomlog[x].start()

        threads.append(thread)

        
        cancellStatus = orderCancelControl(user_order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            user_order.status = "Partial"
            user_order.remains = int(quantity) - user_order.successful_value
            user_order.cancelled = True
            user_order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(user_order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(user_order.successful_value))


            break


def sendPostCommentView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        starting = False

        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')

            comment_media = request.POST.get('media_link', None)
            comment_media = 'https://www.instagram.com/' + comment_media.split('.com/')[1]
            comments = request.POST.get('comments', None)
            media_id = None
            comment_list = comments.splitlines()
            quantity = len(comment_list)
            sv = get_object_or_404(Services, category__category_name="Yorum")

            user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=comment_media,status="Pending",user_order=True)

            def orderControl(user_order):
                
                last_seo = SeoSettings.objects.all().last() 
                whileStatus = True
                while whileStatus:
                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:
                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadComment,args=(quantity,comment_list,comment_media,media_id,user_order,users_categories))
                                t1.start()
                                whileStatus = False

                    
                    time.sleep(5)


            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True

        context = {
            'title':'Yorum Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/send-postcomment.html',context)


def multiRunFollow(us,auth_proxy,ip_port_proxy,x,user_order,quantity,total_quantity,follow_user,errorFile,textUser):
     pass


def threadFollow(quantity,user_order,follow_user,users_categories):
    followislemlog = {}
    userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
    cleaned_up_list = []

    for somemodel in userCookies:
        if somemodel not in cleaned_up_list:
            cleaned_up_list.append(somemodel)

    userCookies = cleaned_up_list

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if len(userCookies) < total_quantity:
        total_quantity = len(userCookies)

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []

    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    userSayac = 0    

    if len(userCookies) == 0:

        user_order.status = "Partial"
        user_order.remains = int(quantity) - user_order.successful_value
        user_order.cancelled = True
        user_order.save()

    for x in range(0, total_quantity):

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]


        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        thread =  threading.Thread(target=multiRunFollow,args=(us,process_auth_proxy,process_ip_port_proxy,x,user_order,quantity,total_quantity,follow_user,errorFile,us.user.username))
        followislemlog[x] = thread
        followislemlog[x].start()

        threads.append(thread)
        
        cancellStatus = orderCancelControl(user_order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            user_order.status = "Partial"
            user_order.remains = int(quantity) - user_order.successful_value
            user_order.cancelled = True
            user_order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(user_order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(user_order.successful_value))

            break


def sendFollowView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if "btnStart" in request.POST:
            
            insta_user= request.POST['username']

            users_categories = request.POST.getlist('user_category')

            if insta_user.find('.com/') != -1:
                insta_user = insta_user.split('.com/')[1].replace('/','')
                insta_user = insta_user.split('?igshid')[0]
            else:
                insta_user = insta_user.replace('/','')
                



            quantity = int(request.POST['quantity'])
            sv = get_object_or_404(Services, category__category_name="Takipçi")

            user_order = Orders.objects.create(user=request.user,target=insta_user,service=sv,charge=float(sv.rate),status="Pending",user_order=True)
            

            def orderControl(user_order):
                last_seo = SeoSettings.objects.all().last()
                whileStatus = True
                while whileStatus:
                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False

                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadFollow,args=(quantity,user_order,insta_user,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'Takipçi Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/send-follow.html',context)
    else:
        raise Http404('not found')


def try4login(user_oi,login_after_ip_port_proxy_list,login_after_auth_proxy_list,login_ip_port_proxy_list,login_auth_proxy_list):
    pass       

def forClearUsers(error_users):
    threads = []
    clearlog = {}
    syx = 0
    login_after_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_after_proxy=True)
    login_after_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_after_proxy=True)
    login_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_proxy=True)
    login_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_proxy=True)
    for user_oi in error_users:
        print("kontrol sağlanıyor... : ",user_oi.user.username)

        thread = threading.Thread(target=try4login,args=(user_oi,login_after_ip_port_proxy_list,login_after_auth_proxy_list,login_ip_port_proxy_list,login_auth_proxy_list),daemon=True)
        clearlog[syx] = thread
        clearlog[syx].start()
        syx += 1
        threads.append(thread)
        
        if len(threads) >= 40:
            for t in threads:
                t:threading.Thread
                t.join()
                threads.clear()


def clearAccountsView(request):
    if request.user.is_authenticated and request.user.is_superuser:
        accountsChecked = False
        error_users = InstagramCookies.objects.filter(active=False)

        if 'btnDeleteAccounts' in request.POST:

            for x in error_users:

                user = get_object_or_404(User,id=x.user.id)
                user.delete()

            return redirect('custom_admin:clear-accounts')

        elif 'btnCheckAccounts' in request.POST:
            print('kontrol başladı...')
            accountsChecked = True
            error_users = InstagramCookies.objects.filter(active=True,error_count=4)
            t = threading.Thread(target=forClearUsers,args=(error_users,),daemon=True)
            t.start()
            error_users = InstagramCookies.objects.filter(active=False)
            
        context = {
            'title':'Hesap Temizliği',
            'accountsChecked':accountsChecked,
            'error_users':error_users,
        }

        return render(request,'custom_admin/clear-accounts.html',context)

def activeUsersThread(get_categories_ids,get_select_status):


    for x in get_categories_ids:
                
        if get_select_status == '0':
            get_users = User.objects.filter(otherinfo__category=x,instagramcookies__active=False)
            
            for y in get_users:
                if y.instagramcookies.login_required == False:

                    y.instagramcookies.active = True
                    y.instagramcookies.challenge = False
                    y.instagramcookies.feedback = False
                    y.instagramcookies.checkpoint = False
                    y.instagramcookies.save()

        elif get_select_status == '1':

            get_users = User.objects.filter(otherinfo__category=x,instagramcookies__challenge=True)
            for y in get_users:
                y.instagramcookies.active = True
                y.instagramcookies.challenge = False
                y.instagramcookies.save()

        elif get_select_status == '2':
            
            get_users = User.objects.filter(otherinfo__category=x,instagramcookies__feedback=True) 
            for y in get_users:
                y.instagramcookies.active = True
                y.instagramcookies.feedback = False
                y.instagramcookies.save()    

        elif get_select_status == '3':

            get_users = User.objects.filter(otherinfo__category=x,instagramcookies__checkpoint=True)
            for y in get_users:
                y.instagramcookies.active = True
                y.instagramcookies.checkpoint = False
                y.instagramcookies.save()


def usersActivePasifView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        
        startingActive = False
        if 'btnActive' in request.POST:

            get_categories_ids = request.POST.getlist('user_category')
            get_select_status = request.POST.get('select_status')

            active_thread = threading.Thread(target=activeUsersThread,args=(get_categories_ids,get_select_status),daemon=True)
            active_thread.start()
            startingActive = True

            
        get_users_categories = UsersCategories.objects.all()
        category_users_len = []
        for x in get_users_categories:
            my_dict = {'total_users':0,'challenge_users':0,'feedback_users':0,'checkpoint_users':0,'active_users':0,'pasif_users':0}

            get_users = User.objects.filter(otherinfo__category=x.id)
            my_dict['total_users'] = get_users.count()
            my_dict['challenge_users'] = get_users.filter(instagramcookies__challenge=True).count()
            my_dict['feedback_users'] = get_users.filter(instagramcookies__feedback=True).count()
            my_dict['login_required_users'] = get_users.filter(instagramcookies__login_required=True).count()
            my_dict['checkpoint_users'] = get_users.filter(instagramcookies__checkpoint=True).count()
            my_dict['active_users'] = get_users.filter(instagramcookies__active=True).count()
            my_dict['pasif_users'] = get_users.filter(instagramcookies__active=False).count()

            category_users_len.append(my_dict)

        get_user_categories = UsersCategories.objects.all()
        context = {
            'title':'Kullanıcıları Aktif Yap',
            'get_user_categories':get_user_categories,
            'startingActive':startingActive,
            'user_categories_data':zip(get_users_categories,category_users_len),
            

        }

        return render(request,'custom_admin/active-pasif-users.html',context)


def loginView(request):

    if request.user.is_authenticated == False:
        if 'btnLogin' in request.POST:

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            login(request, user)
            if request.user.is_superuser:

                return redirect('custom_admin:dashboard')
            else:
                return redirect('custom_admin:dashboard')

        context = {
            'title':'Admin Login'
        }

        return render(request, "custom_admin/login.html", context)
    else:
        if request.user.is_superuser:
            return redirect('custom_admin:dashboard')
        else:
            raise Http404('not found')


def threadRun(insta_login,other_info_i,data_str):

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

     
def addusersthread(u,lq,user_len,last_user,login_after_ip_port_proxy_list,login_after_auth_proxy_list,login_ip_port_proxy_list,login_auth_proxy_list,get_categories,new_account,login_required_funct):
    pass

def addInstaUsersThread(lq,users,get_categories,new_account,login_required_funct):
    pass


def addInstagramUsers(request):
    pass


def successfulValueView(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        successful_log_data = ServicesSuccessfulLog.objects.all()

        total_value = 0
        for x in successful_log_data:
            total_value += x.successful_value
        context = {
            'title':'Başarılı İşlem Kayıtları',
            'successful_log_data':successful_log_data,
            'total_value':total_value,
        }

        return render(request,'custom_admin/successful-value.html',context)
    else:
        raise Http404('not found')


def successfulValueEditView(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        successful_log_data = ServicesSuccessfulLog.objects.all()

        total_value = 0
        for x in successful_log_data:
            total_value += x.successful_value

        if request.method == 'POST':

            if 'btnDeleteLogAll' in request.POST:
                for x in successful_log_data:
                    x.successful_value = 0
                    x.save()
                return redirect('custom_admin:successful-value-edit')
            else:

                for x in successful_log_data:
                    btnName = 'btnDeleteLog' + str(x.id)

                    if btnName in request.POST:
                        x.successful_value = 0
                        x.save()
                        return redirect('custom_admin:successful-value-edit')

        context = {
            'title':'Başarılı İşlem Kayıtları',
            'successful_log_data':successful_log_data,
            'total_value':total_value,
        }

        return render(request,'custom_admin/successful-value-edit.html',context)
    else:
        raise Http404('not found')

def successfulValueEditServiceView(request,id):

    get_service_log = get_object_or_404(ServicesSuccessfulLog,id=id)

    if request.method == 'POST':
        if 'btnSave' in request.POST:
            get_value = request.POST.get('value',0)
            
            if int(get_value) > int(get_service_log.successful_value):
                get_value = int(get_service_log.successful_value)
                
            get_service_log.successful_value -= int(get_value)
            get_service_log.save()

            return redirect('custom_admin:successful-value-edit')

    context = {
        'title':'İşlem Kaydını Düzenle',
        'get_service_log':get_service_log,
    }

    return render(request,'custom_admin/successful-value-edit-service.html',context)

def apiOrdersView(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        q = None
        if request.method == "GET":
            q = request.GET.get('q')
            if q:
                orders = Orders.objects.filter(target=q)
            else:
                orders = Orders.objects.all()
        else:
            orders = Orders.objects.all()

                    
        for x in orders:

            btnName = 'btn' + str(x.id)

            if btnName in request.POST:

                x.cancelled = True
                x.status = 'Partial'
                x.save()
                break

        paginator1 = Paginator(orders,25) 
        page = request.GET.get('page')

        p_orders = paginator1.get_page(page)

        context = {
            'orders':p_orders,
            'title':'Api Sipariş Yönetimi',
            'q':q,
        }

        return render(request,'custom_admin/api-orders.html',context)
    else:
        raise Http404('not found')
        

def instagramUsersList(request):
    if request.user.is_authenticated and request.user.is_superuser:
        q = None
        deleteUsers = False

        if 'btndDelete' in request.POST:
            User.objects.filter(is_superuser=False).delete()
            deleteUsers = True
        if request.method == "GET":
            q = request.GET.get('q')
            if q:

                users = User.objects.filter(is_superuser=False,username=q).order_by("-id")
                oi = OtherInfo.objects.filter(user__is_superuser=False,user__username=q).order_by("-id")
                oii = InstagramCookies.objects.filter(user__is_superuser=False,user__username=q).order_by("-id")              
            
            else:
                users = User.objects.filter(is_superuser=False).order_by("-id")
                oi = OtherInfo.objects.filter(user__is_superuser=False).order_by("-id")
                oii = InstagramCookies.objects.filter(user__is_superuser=False).order_by("-id")                
        else:

            users = User.objects.filter(is_superuser=False).order_by("-id")
            oi = OtherInfo.objects.filter(user__is_superuser=False).order_by("-id")
            oii = InstagramCookies.objects.filter(user__is_superuser=False).order_by("-id")

        paginator1 = Paginator(users,50) 
        paginator2 = Paginator(oi,50)
        paginator3 = Paginator(oii,50)

        page = request.GET.get('page')

        p_users = paginator1.get_page(page)
        p_oi = paginator2.get_page(page)
        p_oii = paginator3.get_page(page)


        context = {
            'users':zip(p_users,p_oi,p_oii),
            'p_users':p_users,
            'title':'Instagram Kullanıcı Listesi',
            "q":q,
            'deleteUsers':deleteUsers,
        }

        return render(request,'custom_admin/instagram-users-list.html',context)
    else:
        raise Http404('not found')


def changeCategoriesThread(get_users,get_u_categories):

    for x in get_users:
        x.otherinfo.category.clear()
        x.otherinfo.category.add(*get_u_categories)
        x.save()

def usersCategoriesUserList(request,id):

    if request.user.is_authenticated and request.user.is_superuser:

        get_user_cat = get_object_or_404(UsersCategories,id=id)
        get_user_categories = UsersCategories.objects.all()
        deleteUsers = False
        changeCats = False
        if 'btnDelete' in request.POST:

            get_selected_users = request.POST.getlist('selectedUsers')
            User.objects.filter(id__in=get_selected_users).delete()

            deleteUsers = True

        elif 'btnChangeCategories' in request.POST:
            
            user_category_ids = request.POST.getlist('user_category')
            get_selected_users = request.POST.getlist('selectedUsers')
            get_users = User.objects.filter(id__in=get_selected_users)
            get_u_categories = UsersCategories.objects.filter(id__in=user_category_ids)
            changec_thread = threading.Thread(target=changeCategoriesThread,args=(get_users,get_u_categories),daemon=True)
            changec_thread.start()
            changeCats = True

        users = User.objects.filter(otherinfo__category=get_user_cat)

        paginator1 = Paginator(users,250) 

        page = request.GET.get('page')

        p_users = paginator1.get_page(page)


        context = {
            'title': get_user_cat.category_name + " " +'Kategorisi Kullanıcı Listesi',
            'users':p_users,
            'p_users':p_users,
            'deleteUsers':deleteUsers,
            'changeCats':changeCats,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/cat-user-list.html',context)    

    else:
        raise Http404('not found')


def editUserPackpagesView(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        packpages = get_object_or_404(UserPackpages,id=id)
        
        form = UpdatePackpageform(request.POST or None,instance=packpages)

        if form.is_valid():
            form.save()

            return redirect('custom_admin:user-packpages')
        context = {
            'title':'Kullanıcı Paketi Düzenle' + '{}'.format(packpages.name),
            'form':form,
        }
        return render(request,'custom_admin/edit-packpages.html',context)    

    else:
        raise Http404('not found')

def userPackpagesView(request):
    if request.user.is_authenticated and request.user.is_superuser:

        creating = False
        user_categories_list = UsersCategories.objects.all()
        genders_db = Genders.objects.all()
        country_codes_db = CountryCodes.objects.all()
        all_packpages = UserPackpages.objects.all()

        for x in all_packpages:
            btnName = "btn{}".format(x.id)
            if btnName in request.POST:
                x.delete()
                return redirect('custom_admin:user-packpages')
        if 'btnCreate' in request.POST:

            packpageName = request.POST['packpageName']


            gender = request.POST.get('selectGender',None)
            country_code = request.POST.get('selectCountry',None)
            get_user_cateogories_ids = request.POST.getlist('user_category',None)
            get_categories = None
            if get_user_cateogories_ids:
                get_categories = UsersCategories.objects.filter(id__in=get_user_cateogories_ids)

            gend = None
            country = None
            if gender:

                gend = get_object_or_404(Genders,id=int(gender))
            if country_code:

                country = get_object_or_404(CountryCodes,id=int(country_code))

            us_p = UserPackpages.objects.create(name=packpageName,gender=gend,country_code=country)
            if get_categories:
                us_p.category.add(*get_categories)
                us_p.save()

            return redirect('custom_admin:user-packpages')            

        context = {
            'title':'Api Kullanıcı Paketleri',
            'genders':genders_db,
            'country_codes':country_codes_db,
            'all_packpages':all_packpages,
            'user_categories_list':user_categories_list,
        }
        return render(request,'custom_admin/user-packpages.html',context)

    else:
        raise Http404('not found')


def usersDataView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        
        users = OtherInfo.objects.filter(user__is_superuser=False)
        erkekUsers = users.filter(gender="1").count()
        kadinUsers = users.filter(gender="2").count()
        all_country_codes = CountryCodes.objects.all()

        countryCodeList = []
        for x in all_country_codes:

            mydict = {
                'total_user':users.filter(country_code=x.name).count(),
                'erkek_user':users.filter(country_code=x.name,gender="1").count(),
                'kadin_user':users.filter(country_code=x.name,gender="2").count(),
                'country_code':x.name,
                }

            countryCodeList.append(mydict)

        context = {
            'title':'Kullanıcı Verileri',
            'erkek':erkekUsers,
            'kadin':kadinUsers,
            'total':erkekUsers+kadinUsers,
            'countryCodeList':countryCodeList,
        }

        return render(request,'custom_admin/users-data.html',context)

    else:
        raise Http404('not found')

def servicesview(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user_packpages_db = UserPackpages.objects.all()
        category_db = ServiceCategory.objects.all()
        
        all_services = Services.objects.all()

        for x in all_services:
            btnName = "btn{}".format(x.service)
            if btnName in request.POST:
                x.delete()
                return redirect('custom_admin:services')

        if 'btnCreate' in request.POST:


            name = request.POST['name']
            user_packpages = request.POST.get('user_packpages',None)
            category = request.POST['category']
            min_ = request.POST['min']
            max_ = request.POST['max']
            rate_ = request.POST['rate']


            packpages = None
            if user_packpages:

                packpages = get_object_or_404(UserPackpages,id=int(user_packpages))

            category = get_object_or_404(ServiceCategory,id=int(category))

            Services.objects.create(name=name,packpages=packpages,category=category,min=min_,max=max_,rate=rate_)
            return redirect('custom_admin:services')
        
        context = {
            
            'title':'Servisler',
            'user_packpages_db':user_packpages_db,
            'category_db':category_db,
            'services':all_services,
        }

        return render(request,'custom_admin/services.html',context)
    else:
        raise Http404('not found')

def editServicesView(request,id):
    
    if request.user.is_authenticated and request.user.is_superuser:
        service = get_object_or_404(Services,service=id)
        form = UpdateServiceform(request.POST or None,instance=service)

        if form.is_valid():
            form.save()

            return redirect('custom_admin:services')
        context = {
            'title':'Servis Düzenle' + " " +  '{}'.format(service.name),
            'service':service,
            'form':form,
        }
        return render(request,'custom_admin/edit-services.html',context)
    
    else:
        raise Http404('not found')

def apiSettingsView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        

        createdkey = None
        
        if 'btnCreate' in request.POST:
            createdkey = binascii.hexlify(os.urandom(20)).decode()
            Keys.objects.all().delete()
            api = Keys.objects.create(
                createdby=request.user, key=createdkey)
            api.save()

        elif request.method == 'POST':
            search_user = request.POST['search_user']
            
            return redirect('user:user-page',username=search_user)

        context = {
            'api_key': createdkey,
            'title':'Api Ayarları'
        }
        return render(request, 'custom_admin/api-settings.html', context)
    else:
        raise Http404('not found')
def importThread(file,get_categories):


    with open(file.file.path,encoding="utf-8") as f:

        data = f.readline()
        data = base64.b64decode(data).decode('utf-8')
        data = data.splitlines()

        for u in data:

            userData = u.split("::")
            username = userData[1]
            password = userData[2]
            print(username)
            email = userData[3]
            picture_url = userData[4]
            
            if userData[5] == 'None':
                country_code = None
            else:
                country_code = userData[5]

            if country_code:
                countryControl = CountryCodes.objects.filter(name=country_code)
                if len(countryControl) == 0:
                    CountryCodes.objects.create(name=country_code) 
            gender = userData[6]
            phone = userData[7]
            balance = 0
            default_user = userData[9]

            if default_user == 'True':
                default_user = True

            else:
                default_user = False

            bot_user = userData[10]

            if bot_user == 'True':
                bot_user = True

            else:
                bot_user = False

            userid = userData[11]
            authorization = userData[12]
            claim = userData[13]
            phoneid = userData[14]
            pigeonid = userData[15]
            rur = userData[16]
            mid = userData[17]
            waterfallid = userData[18]
            deviceid = userData[19]
            androidid = userData[20]
            user_agent = userData[21]
            checksum = userData[22]
            active = userData[23]

            if active == 'True':
                active = True
            else:
                active = False

            device_type = userData[24]
            brand = userData[25]
            manufacturer = userData[26]
            os_type = userData[27]
            os_ver = userData[28]
            guid = userData[29]
            adid = userData[30]
            key = userData[31]
            
            try:
                new_account = userData[32]
            except:
                new_account = 'True'

            if new_account == 'True':
                new_account = True
                old_account = False
            else:
                new_account = False
                old_account = True

            ck_data = userData[33]
            register_key = userData[34]
                
            org_user = User.objects.filter(username=username).last()

            if org_user:
                oii = get_object_or_404(InstagramCookies,user=org_user)

                oii.userid = userid
                oii.authorization = authorization
                oii.claim = claim
                oii.phoneid = phoneid
                oii.pigeonid = pigeonid
                oii.rur = rur
                oii.mid = mid
                oii.user_agent = user_agent
                oii.checksum = checksum
                oii.active = active
                oii.device_type = device_type
                oii.brand = brand
                oii.manufacturer = manufacturer
                oii.os_type = os_type
                oii.os_ver = os_ver
                oii.guid = guid
                oii.adid = adid
                oii.key = key
                oii.new_account = new_account
                oii.old_account = old_account
                oii.ck_data = ck_data
                oii.register_key = register_key
                oii.save()
                print('kullanici güncellendi')

            else:
                new_user = User.objects.create_user(username=username,password=password,email=email)
                create_oi = OtherInfo.objects.create(user=new_user,picture_url=picture_url,country_code=country_code,gender=gender,phone=phone,
                                balance=balance,default_user=default_user,bot_user=bot_user,)
                create_oi.category.add(*get_categories)
                create_oi.save()
                InstagramCookies.objects.create(user=new_user,userid=userid,authorization=authorization,claim=claim,default_password=password,
                                phoneid=phoneid,pigeonid=pigeonid,waterfallid=waterfallid,androidid=androidid,deviceid=deviceid,rur=rur,mid=mid,user_agent=user_agent,checksum=checksum,active=active,
                                device_type=device_type,brand=brand,manufacturer=manufacturer,os_type=os_type,os_ver=os_ver,guid=guid,adid=adid,key=key,new_account=new_account,old_account=old_account,ck_data=ck_data,register_key=register_key)
    file.delete()

def importUsersView(request):
    if request.user.is_authenticated and request.user.is_superuser:

        form  = ImportFileForm(request.POST or None,request.FILES or None)
        fileData = ImportFiles.objects.all()
        get_user_categories = UsersCategories.objects.all()

        loadingFile = False
        importUsers = False

        if form.is_valid():
            form.save()
            fileData = ImportFiles.objects.all()
            loadingFile = True


        if 'btnImport' in request.POST:
            getFileID = request.POST.get('fileName',None)

            file = get_object_or_404(ImportFiles,id=int(getFileID))

            users_categories = request.POST.getlist('user_category')
            get_categories = UsersCategories.objects.filter(id__in=users_categories)
            t = threading.Thread(target=importThread,args=(file,get_categories),daemon=True)
            t.start()
            importUsers = True

        context = {
            'importUsers': importUsers,
            'loadingFile':loadingFile,
            'title':'Kullanıcıları İçe Aktar',
            'form':form,
            'fileData':fileData,
            'get_user_categories':get_user_categories,
        }
        return render(request, 'custom_admin/import-users.html', context)
    else:
        raise Http404('not found')


def exportUsersView(request):
    if request.user.is_authenticated and request.user.is_superuser:
        get_user_categories = UsersCategories.objects.all()

        importing = False
        genders_db = Genders.objects.all()
        country_codes_db = CountryCodes.objects.all()

        if 'btnExportUserPass' in request.POST:
            user_data_set = ""

            gender = request.POST.get('selectGender',None)
            country_code = request.POST.get('selectCountry',None)
            users_categories = request.POST.getlist('user_category')
            userCookies = User.objects.filter(otherinfo__category__id__in=users_categories,instagramcookies__active=True)
            cleaned_up_list = []

            for somemodel in userCookies:
                if somemodel not in cleaned_up_list:
                    cleaned_up_list.append(somemodel)

            user_data = cleaned_up_list


            gend = None
            country = None

            deleteUser = False
            if 'deleteUser' in request.POST :
                deleteUser = True

            if gender:

                gend = get_object_or_404(Genders,id=int(gender))
            if country_code:

                country = get_object_or_404(CountryCodes,id=int(country_code))


            for x in user_data:
                
                if gend and country:

                    if user_data.otherinfo.gender == str(gend) and user_data.otherinfo.country_code == str(country):

                        user_data_set += (f"""{x.username}:{x.instagramcookies.default_password}\n""")
   
       
                elif gend:
                    if user_data.otherinfo.gender == str(gend):
    
                        user_data_set += (f"""{x.username}:{x.instagramcookies.default_password}\n""")

               
                elif country:

                    if user_data.otherinfo.country_code == str(country):
    
                        user_data_set += (f"""{x.username}:{x.instagramcookies.default_password}\n""")

                else:
                    user_data_set += (f"""{x.username}:{x.instagramcookies.default_password}\n""")
                    
            if deleteUser:
                userCookies.delete()

            
            file_data = user_data_set

            response = HttpResponse(file_data, content_type='application/text charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="users.instatogether"'
            return response

        elif 'btnExport' in request.POST:

            user_data_set = ""

            gender = request.POST.get('selectGender',None)
            country_code = request.POST.get('selectCountry',None)

            users_categories = request.POST.getlist('user_category')
            userCookies = User.objects.filter(otherinfo__category__id__in=users_categories,instagramcookies__active=True)
            cleaned_up_list = []

            for somemodel in userCookies:
                if somemodel not in cleaned_up_list:
                    cleaned_up_list.append(somemodel)

            user_data = cleaned_up_list
    
            gend = None
            country = None

            deleteUser = False
            if 'deleteUser' in request.POST :
                deleteUser = True

            if gender:

                gend = get_object_or_404(Genders,id=int(gender))
            if country_code:

                country = get_object_or_404(CountryCodes,id=int(country_code))


            for x in user_data:
                
                if gend and country:
        
                    if x.otherinfo.gender == str(gend) and x.otherinfo.country_code == str(country):

                        user_data_set += (f"""{x.id}::{x.username}::{x.instagramcookies.default_password}::{x.email}::{x.otherinfo.picture_url}::{x.otherinfo.country_code}::{x.otherinfo.gender}::{x.otherinfo.phone}::{x.otherinfo.balance}::{x.otherinfo.default_user}::{x.otherinfo.bot_user}::{x.instagramcookies.userid}::{x.instagramcookies.authorization}::{x.instagramcookies.claim}::{x.instagramcookies.phoneid}::{x.instagramcookies.pigeonid}::{x.instagramcookies.rur}::{x.instagramcookies.mid}::{x.instagramcookies.waterfallid}::{x.instagramcookies.deviceid}::{x.instagramcookies.androidid}::{x.instagramcookies.user_agent}::{x.instagramcookies.checksum}::{x.instagramcookies.active}::{x.instagramcookies.device_type}::{x.instagramcookies.brand}::{x.instagramcookies.manufacturer}::{x.instagramcookies.os_type}::{x.instagramcookies.os_ver}::{x.instagramcookies.guid}::{x.instagramcookies.adid}::{x.instagramcookies.key}::{x.instagramcookies.new_account}::{x.instagramcookies.ck_data}::{x.instagramcookies.register_key}\n""")

       
                elif gend:
                    if x.otherinfo.gender == str(gend):
    
                        user_data_set += (f"""{x.id}::{x.username}::{x.instagramcookies.default_password}::{x.email}::{x.otherinfo.picture_url}::{x.otherinfo.country_code}::{x.otherinfo.gender}::{x.otherinfo.phone}::{x.otherinfo.balance}::{x.otherinfo.default_user}::{x.otherinfo.bot_user}::{x.instagramcookies.userid}::{x.instagramcookies.authorization}::{x.instagramcookies.claim}::{x.instagramcookies.phoneid}::{x.instagramcookies.pigeonid}::{x.instagramcookies.rur}::{x.instagramcookies.mid}::{x.instagramcookies.waterfallid}::{x.instagramcookies.deviceid}::{x.instagramcookies.androidid}::{x.instagramcookies.user_agent}::{x.instagramcookies.checksum}::{x.instagramcookies.active}::{x.instagramcookies.device_type}::{x.instagramcookies.brand}::{x.instagramcookies.manufacturer}::{x.instagramcookies.os_type}::{x.instagramcookies.os_ver}::{x.instagramcookies.guid}::{x.instagramcookies.adid}::{x.instagramcookies.key}::{x.instagramcookies.new_account}::{x.instagramcookies.ck_data}::{x.instagramcookies.register_key}\n""")
               
               
                elif country:

                    if x.otherinfo.country_code == str(country):
    
                        user_data_set += (f"""{x.id}::{x.username}::{x.instagramcookies.default_password}::{x.email}::{x.otherinfo.picture_url}::{x.otherinfo.country_code}::{x.otherinfo.gender}::{x.otherinfo.phone}::{x.otherinfo.balance}::{x.otherinfo.default_user}::{x.otherinfo.bot_user}::{x.instagramcookies.userid}::{x.instagramcookies.authorization}::{x.instagramcookies.claim}::{x.instagramcookies.phoneid}::{x.instagramcookies.pigeonid}::{x.instagramcookies.rur}::{x.instagramcookies.mid}::{x.instagramcookies.waterfallid}::{x.instagramcookies.deviceid}::{x.instagramcookies.androidid}::{x.instagramcookies.user_agent}::{x.instagramcookies.checksum}::{x.instagramcookies.active}::{x.instagramcookies.device_type}::{x.instagramcookies.brand}::{x.instagramcookies.manufacturer}::{x.instagramcookies.os_type}::{x.instagramcookies.os_ver}::{x.instagramcookies.guid}::{x.instagramcookies.adid}::{x.instagramcookies.key}::{x.instagramcookies.new_account}::{x.instagramcookies.ck_data}::{x.instagramcookies.register_key}\n""")

                else:
                    user_data_set += (f"""{x.id}::{x.username}::{x.instagramcookies.default_password}::{x.email}::{x.otherinfo.picture_url}::{x.otherinfo.country_code}::{x.otherinfo.gender}::{x.otherinfo.phone}::{x.otherinfo.balance}::{x.otherinfo.default_user}::{x.otherinfo.bot_user}::{x.instagramcookies.userid}::{x.instagramcookies.authorization}::{x.instagramcookies.claim}::{x.instagramcookies.phoneid}::{x.instagramcookies.pigeonid}::{x.instagramcookies.rur}::{x.instagramcookies.mid}::{x.instagramcookies.waterfallid}::{x.instagramcookies.deviceid}::{x.instagramcookies.androidid}::{x.instagramcookies.user_agent}::{x.instagramcookies.checksum}::{x.instagramcookies.active}::{x.instagramcookies.device_type}::{x.instagramcookies.brand}::{x.instagramcookies.manufacturer}::{x.instagramcookies.os_type}::{x.instagramcookies.os_ver}::{x.instagramcookies.guid}::{x.instagramcookies.adid}::{x.instagramcookies.key}::{x.instagramcookies.new_account}::{x.instagramcookies.ck_data}::{x.instagramcookies.register_key}\n""")
                

            if deleteUser:
                userCookies.delete()
                print('kullanıcı silindi')

            
            file_data = user_data_set
            file_data = base64.b64encode(file_data.encode())

            response = HttpResponse(file_data, content_type='application/text charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="users.instatogether"'
            return response


        context = {
            'importing': importing,
            'title':'Kullanıcıları Dışa Aktar',
            'genders':genders_db,
            'get_user_categories':get_user_categories,
            'country_codes':country_codes_db,
        }
        return render(request, 'custom_admin/export-users.html', context)

    else:
        raise Http404('not found')

def seoSettingsView(request):


    if request.user.is_authenticated and request.user.is_superuser:
        
        filesForm = seoFilesForm(request.POST or None, request.FILES or None)
        last_seo = SeoSettings.objects.all().last()
        if last_seo:
            filesForm = seoFilesForm(request.POST or None, request.FILES or None,instance=last_seo)

        if 'seoCreate' in request.POST:
            filesForm.save()
            #SeoSettings.objects.create(google_tag=request.POST['google_tag'],ana_title=request.POST['ana_title'],description=request.POST['description'],keywords=request.POST['keywords'])
            return redirect('custom_admin:seo-settings')

        elif 'lastSeoUpdate' in request.POST:
            filesForm.save()

            return redirect('custom_admin:seo-settings')

        context = {
            'title':'Seo Ayarları',
            'last_seo':last_seo,
            'filesForm':filesForm,
        }

        return render(request,'custom_admin/seo-settings.html',context)
    else:
        raise Http404('not found')



def smtpSettingsView(request):
    

    if request.user.is_authenticated and request.user.is_superuser:
        
        smtp_form = SmtpForm(request.POST or None, request.FILES or None)
        last_seo = MailSMTPInfo.objects.all().last()
        smtp_test_status = False
        mailSend = False
        mailError = False

        if last_seo:
            smtp_form = SmtpForm(request.POST or None, request.FILES or None,instance=last_seo)
            smtp_test_status = True

        if 'btnSave' in request.POST and smtp_form.is_valid():
            smtp_form.save()

        elif 'btnSendMail' in request.POST:
            mailSend = True

            subject = request.POST['sending_subject']
            content = request.POST['sending_content']
            email = request.POST['sending_email']
            try:
                sendMail2(subject,content,email)
                return redirect('custom_admin:smtp-settings')
            except Exception as e :
                print(e)
                mailError = True

        context = {
            'title':'SMTP Mail Ayarları',
            'smtp_form':smtp_form,
            'smtp_test_status':smtp_test_status,
            'mailError':mailError,
            'mailSend':mailSend,
        }

        return render(request,'custom_admin/smtp-settings.html',context)
    else:
        raise Http404('not found')



def homeManagerView(request):

    if request.user.is_authenticated and request.user.is_superuser:


        last_home = HomeData.objects.all().last()
        if 'btnCreate' in request.POST:
    
            HomeData.objects.create(title=request.POST['title'],explanation=request.POST['explanation'],button1=request.POST['button1'],
                                    button1_link=request.POST['button1_link'],button2=request.POST['button2'],button2_link=request.POST['button2_link'])
            return redirect('custom_admin:home-manager')
        elif 'lastHomeUpdate' in request.POST:

            last_home.title = request.POST['title']
            last_home.explanation = request.POST['explanation']
            last_home.button1 = request.POST['button1']
            last_home.button1_link = request.POST['button1_link']
            last_home.button2 = request.POST['button2']
            last_home.button2_link = request.POST['button2_link']
            last_home.save()
            return redirect('custom_admin:home-manager')

        context = {
            'title':'Ana Sayfa Yönetimi',
            'last_home':last_home,
        }

        return render(request,'custom_admin/home-manager.html',context)
    else:

        raise Http404('not found')

def threadAddProxy(request):

    print('proxyler ekleniyor...')
    login_after_proxy = request.POST.get('login_after_proxy_list',None)
    login_after_type = request.POST.get('login_after_proxy_type',None)
    if login_after_proxy and login_after_type:

        proxy_list = login_after_proxy.splitlines()

        if login_after_type == "1":
            
            for p in proxy_list:
                Proxy.objects.create(proxy=p,ip_port_proxy=True,login_after_proxy=True)

        elif login_after_type == "2":

            for p in proxy_list:
                Proxy.objects.create(proxy=p,auth_proxy=True,login_after_proxy=True)

    login_proxy = request.POST.get('login_proxy_list',None)
    login_select_type = request.POST.get('login_proxy_type',None)

    if login_proxy and login_select_type:

        proxy_list = login_proxy.splitlines()

        if login_select_type == "1":
            
            for p in proxy_list:
                Proxy.objects.create(proxy=p,ip_port_proxy=True,login_proxy=True)

        elif login_select_type == "2":

            for p in proxy_list:
                Proxy.objects.create(proxy=p,auth_proxy=True,login_proxy=True)

    process_proxy = request.POST.get('process_proxy_list',None)
    process_type = request.POST.get('process_proxy_type',None)

    if process_proxy and process_type:

        proxy_list = process_proxy.splitlines()

        if process_type == "1":
            
            for p in proxy_list:
                Proxy.objects.create(proxy=p,ip_port_proxy=True,process_proxy=True)

        elif process_type == "2":

            for p in proxy_list:
                Proxy.objects.create(proxy=p,auth_proxy=True,process_proxy=True)


    video_proxy = request.POST.get('video_proxy_list',None)
    video_type = request.POST.get('video_proxy_type',None)

    if video_proxy and video_type:

        proxy_list = video_proxy.splitlines()

        if video_type == "1":
            
            for p in proxy_list:
                Proxy.objects.create(proxy=p,ip_port_proxy=True,video_proxy=True)

        elif video_type == "2":

            for p in proxy_list:
                Proxy.objects.create(proxy=p,auth_proxy=True,video_proxy=True)


    process_proxy = request.POST.get('auto_process_proxy_list',None)
    process_type = request.POST.get('auto_process_proxy_type',None)

    if process_proxy and process_type:

        proxy_list = process_proxy.splitlines()

        if process_type == "1":
            
            for p in proxy_list:
                Proxy.objects.create(proxy=p,ip_port_proxy=True,auto_process_proxy=True)

        elif process_type == "2":

            for p in proxy_list:
                Proxy.objects.create(proxy=p,auth_proxy=True,auto_process_proxy=True)


def addProxyView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        server_ip = request.META['REMOTE_ADDR']
        addStatus = False
        deleteStatus = False
        allDeleteStatus = False
        filter_proxy1 = None
        filter_proxy2 = None

        all_proxy = Proxy.objects.all()

        if 'deleteAllProxy' in request.POST:

            all_proxy.delete()
            allDeleteStatus = True

        for x in all_proxy:
            btnName = "btn{}".format(x.id)
            if btnName in request.POST:
                x.delete()
                deleteStatus = True
                break

        
        all_proxy = Proxy.objects.all()


        if 'addProxy' in request.POST:
            
            addStatus = True

            t = threading.Thread(target=threadAddProxy,args=(request,))
            t.start()



        if 'btnFilter' in request.POST:
            filter_proxy = request.POST.get('filter_proxy',None)
            filter_proxy_type = request.POST.get('filter_proxy_type',None)
            if filter_proxy == "0":
                filter_proxy1 = '0'

                login_p = False
                login_after_p = False
                process_p = False
                auto_process_p = False
                video_p = False

                if filter_proxy_type == "0":
                    filter_proxy2 = '0'
                else:

                    if filter_proxy_type == "1":
                        login_p = True
                        filter_proxy2 = '1'

                    elif filter_proxy_type == "2":
                        login_after_p = True
                        filter_proxy2 = '2'
                    elif filter_proxy_type == "3":
                        process_p = True
                        filter_proxy2 = '3'
                    elif filter_proxy_type == "4":
                        auto_process_p = True
                        filter_proxy2 = '4'
                    elif filter_proxy_type == "5":
                        video_p = True
                        filter_proxy2 = '5'


                    all_proxy = Proxy.objects.filter(video_proxy=video_p,auto_process_proxy=auto_process_p,process_proxy=process_p,login_proxy=login_p,login_after_proxy=login_after_p)                    


            if filter_proxy == "1":
                filter_proxy1 = '1'

                login_p = False
                login_after_p = False
                process_p = False
                auto_process_p = False
                video_p = False

                if filter_proxy_type == "0":
                    all_proxy = Proxy.objects.filter(ip_port_proxy=True,auth_proxy=False)
                    filter_proxy2 = '0'                    

                else:
                    if filter_proxy_type == "1":
                        filter_proxy2 = '1'
                        login_p = True
                    elif filter_proxy_type == "2":
                        login_after_p = True
                        filter_proxy2 = '2'
                    elif filter_proxy_type == "3":
                        process_p = True
                        filter_proxy2 = '3'
                    elif filter_proxy_type == "4":
                        auto_process_p = True
                        filter_proxy2 = '4'
                    elif filter_proxy_type == "5":
                        video_p = True
                        filter_proxy2 = '5'
                    all_proxy = Proxy.objects.filter(video_proxy=video_p,auto_process_proxy=auto_process_p,ip_port_proxy=True,auth_proxy=False,process_proxy=process_p,login_proxy=login_p,login_after_proxy=login_after_p)                    

            elif filter_proxy == "2":
                filter_proxy1 = '2'


                login_p = False
                login_after_p = False
                process_p = False
                auto_process_p = False
                video_p = False

                if filter_proxy_type == "0":
                    all_proxy = Proxy.objects.filter(ip_port_proxy=False,auth_proxy=True)  
                    filter_proxy2 = '0'                  

                else:
                    if filter_proxy_type == "1":
                        filter_proxy2 = '1'
                        login_p = True
                    elif filter_proxy_type == "2":
                        filter_proxy2 = '2'
                        login_after_p = True
                    elif filter_proxy_type == "3":
                        process_p = True
                        filter_proxy2 = '3'
                    elif filter_proxy_type == "4":
                        auto_process_p = True
                        filter_proxy2 = '4'
                    elif filter_proxy_type == "5":
                        video_p = True
                        filter_proxy2 = '5'
                    all_proxy = Proxy.objects.filter(video_proxy=video_p,auto_process_proxy=auto_process_p,ip_port_proxy=False,auth_proxy=True,process_proxy=process_p,login_proxy=login_p,login_after_proxy=login_after_p)
        paginator = Paginator(all_proxy,100) 
        page = request.GET.get('page')

        p_all_proxy = paginator.get_page(page)
        context = {
            'title':'Service Proxy',
            'addStatus':addStatus,
            'all_proxy':p_all_proxy,
            'deleteStatus':deleteStatus,
            'allDeleteStatus':allDeleteStatus,
            'server_ip':server_ip,
            'filter_proxy1':filter_proxy1,
            'filter_proxy2':filter_proxy2,
        }

        return render(request,'custom_admin/add_proxy.html',context)
    else:
        raise Http404('not found')


def webApiContactView(request):

    allHosts = HostKeys.objects.all()

    context = {
        'title':'Web Api İletişimleri',
        'hosts':allHosts,
    }

    return render(request,'custom_admin/api-contact.html',context)

def addApiData(userdata,api_url,host,request):

    userdata  = requests.get(api_url,data={'key':host.key,'host':request.get_host()},timeout=45)
    print(userdata.status_code)
    if userdata.status_code == 200:

        userdata = userdata.json()
        userdata = base64.b64decode(userdata['data'])
        userdata = json.loads(userdata)

        for x in userdata:
            username = x['username']
            if not User.objects.filter(username=username):
                print("kaydediliyor... , ",username)
                password = x['instagramcookies']['default_password']
                email = x['email']

                picture_url = x['otherinfo']['picture_url']
                country_code = x['otherinfo']['country_code']
                gender = x['otherinfo']['gender']
                phone = x['otherinfo']['phone']
                balance = 300
                default_user = x['otherinfo']['default_user']
                bot_user = x['otherinfo']['bot_user']

                userid = x['instagramcookies']['userid']
                authorization = x['instagramcookies']['authorization']
                phoneid = x['instagramcookies']['phoneid']
                pigeonid = x['instagramcookies']['pigeonid']
                rur = x['instagramcookies']['rur']
                mid = x['instagramcookies']['mid']
                waterfallid = x['instagramcookies']['waterfallid']
                deviceid = x['instagramcookies']['deviceid']
                androidid = x['instagramcookies']['androidid']
                user_agent = x['instagramcookies']['user_agent']
                claim = x['instagramcookies']['claim']
                checksum = x['instagramcookies']['checksum']
                active = True
                device_type = x['instagramcookies']['device_type']
                brand = x['instagramcookies']['brand']
                manufacturer = x['instagramcookies']['manufacturer']
                os_type = x['instagramcookies']['os_type']
                os_ver = x['instagramcookies']['os_ver']
                guid = x['instagramcookies']['guid']
                adid = x['instagramcookies']['adid']
                key = x['instagramcookies']['key']
                error_count = 0

                new_user = User.objects.create_user(username=username,password=password,email=email)
                OtherInfo.objects.create(user=new_user,picture_url=picture_url,country_code=country_code,gender=gender,phone=phone,
                                        balance=balance,default_user=default_user,bot_user=bot_user,)
                InstagramCookies.objects.create(user=new_user,userid=userid,authorization=authorization,claim=claim,default_password=password,
                                        phoneid=phoneid,pigeonid=pigeonid,waterfallid=waterfallid,androidid=androidid,deviceid=deviceid,rur=rur,mid=mid,user_agent=user_agent,checksum=checksum,active=active,
                                        device_type=device_type,brand=brand,manufacturer=manufacturer,os_type=os_type,os_ver=os_ver,guid=guid,adid=adid,key=key)

def webApiContactManage(request,host):
    if request.user.is_authenticated and request.user.is_superuser:
    
        userinfo = 0
        userdata = None
        userReq = False
        userReq2 = False

        host = get_object_or_404(HostKeys,host=host)
        
        if 'btnGetData' in request.POST:

            userReq = True
            api_url = 'https://' + host.host + '/api/out_user_info/'
            print(api_url)
            userinfo  = requests.get(api_url,data={'key':host.key})

            if userinfo.status_code == 200:
                userinfo = userinfo.json()['users']

        elif 'btnGetUserData' in request.POST:
            userReq2 = True

            api_url = 'https://' + host.host + '/api/out_data/'
            print(api_url)

            t = threading.Thread(target=addApiData,args=(userdata,api_url,host,request))
            t.start()
            
        context = {
            'title':'Web Api İletişimleri',
            'host':host,
            'userinfo':userinfo,
            'userReq':userReq,
            'userReq2':userReq2,
        }

        return render(request,'custom_admin/api-contact-manage.html',context)

    else:
        return Http404()


def notLoginUsersView(request):

    if request.user.is_authenticated and request.user.is_superuser:

        updateModel = False
        
        try:

            allNotLoginFile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users.txt'),'r')
            allNotLogins = allNotLoginFile.readlines()
            allNotLoginFile.close()

            allNotLoginChallengeFile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users_challenge.txt'),'r')
            allNotLoginsChallenge = allNotLoginChallengeFile.readlines()
            allNotLoginChallengeFile.close()

            if 'btnDelete' in request.POST:
                if allNotLogins:
                        
                    clearfile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users.txt'),'w')
                    clearfile.write('')
                    allNotLogins = []
                    updateModel = True

            if 'btnDeleteChallenge' in request.POST:
                if allNotLoginsChallenge:
                        
                    clearfile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users_challenge.txt'),'w')
                    clearfile.write('')
                    allNotLoginsChallenge = []
                    updateModel = True

        except:
            allNotLogins = []



        context = {
            'title':'Girişte Hata ile Karşılaşan Yeni Hesaplar',
            'allNotLogins':allNotLogins,
            'allNotLoginsChallenge':allNotLoginsChallenge,
            'updateModel':updateModel,
        }

        return render(request,'custom_admin/notlogin-users.html',context)





def notLoginOldUsersView(request):

    if request.user.is_authenticated and request.user.is_superuser:

        updateModel = False
        
        try:

            allNotLoginFile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users_old.txt'),'r')
            allNotLogins = allNotLoginFile.readlines()
            allNotLoginFile.close()

            allNotLoginChallengeFile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users_old_challenge.txt'),'r')
            allNotLoginsChallenge = allNotLoginChallengeFile.readlines()
            allNotLoginChallengeFile.close()

            allNotLoginCheckpointFile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users_old_checkpoint.txt'),'r')
            allNotLoginsCheckpoint = allNotLoginCheckpointFile.readlines()
            allNotLoginCheckpointFile.close()
            if 'btnDelete' in request.POST:
                if allNotLogins:
                        
                    clearfile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users_old.txt'),'w')
                    clearfile.write('')
                    allNotLogins = []
                    updateModel = True

            if 'btnDeleteChallenge' in request.POST:
                if allNotLoginsChallenge:
                        
                    clearfile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users_old_challenge.txt'),'w')
                    clearfile.write('')
                    allNotLoginsChallenge = []
                    updateModel = True

            if 'btnDeleteCheckpoint' in request.POST:
                if allNotLoginsCheckpoint:
                        
                    clearfile = open((BASE_DIR / 'static/notlogin_userlogs/not_login_users_old_checkpoint.txt'),'w')
                    clearfile.write('')
                    allNotLoginsCheckpoint = []
                    updateModel = True

        except:
            allNotLogins = []



        context = {
            'title':'Girişte Hata ile Karşılaşan Eski Hesaplar',
            'allNotLogins':allNotLogins,
            'allNotLoginsChallenge':allNotLoginsChallenge,
            'allNotLoginsCheckpoint':allNotLoginsCheckpoint,
            'updateModel':updateModel,
        }

        return render(request,'custom_admin/notlogin-old-users.html',context)





def threadGetUserFollowData(username,process_log):
    pass


def getUserFollowDataView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        process = False
        if 'btnStart' in request.POST:

            username = request.POST['username']
            process_log = GetFollowDataLog.objects.create(username=username)
            t = threading.Thread(target=threadGetUserFollowData,args=(username,process_log))
            t.start()
            process = True
            
        all_process = GetFollowDataLog.objects.all()

        for p in all_process:
        
            btnName =  'btnCancel' + '{}'.format(p.id)

            if btnName in request.POST:

                p.cancelled = True
                p.save()
                return redirect('custom_admin:get-user-followdata')

        for p in all_process:
    
            btnName =  'btnDelete' + '{}'.format(p.id)

            if btnName in request.POST:

                p.delete()
                return redirect('custom_admin:get-user-followdata')
            
      
        for p in all_process:
            btnName =  'downloadUsernameData' + '{}'.format(p.id)

            if btnName in request.POST:

                response = HttpResponse(p.users_list_username, content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="{}_followers_username_data.txt"'.format(p.username)
                return response
        
        for p2 in all_process:
            btnName =  'downloadUseridData' + '{}'.format(p2.id)

            if btnName in request.POST:

                response = HttpResponse(p2.users_list_user_id, content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="{}_followers_userid_data.txt"'.format(p2.username)
                return response


        context = {
            'title':'Kullanıcı Takipçi Verilerini Çek',
            'process':process,
            'all_process':all_process,
        }

        return render(request,'custom_admin/get-user-followdata.html',context)





def sendAutoPostLikeView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False

        if "btnAddAutoLike" in request.POST:
           
            username = request.POST['username']
            quantity = int(request.POST['quantity'])
            timeout = int(request.POST['timeout'])

            sv = get_object_or_404(Services, category__category_name="Oto Beğeni {}".format(timeout))
            order = Orders.objects.create(user=request.user,target=username,service=sv,charge=float(sv.rate),status='Completed',auto_process=True,user_order=True)
            AutoLikeUser.objects.create(username=username,quantity=quantity,timeout=timeout,order=order)

        allAutoLikeUsers = AutoLikeUser.objects.all()
        for x in allAutoLikeUsers:

            btnName = "btnDelete{}".format(x.id)

            if btnName in request.POST:
                x.delete()
                deleteStatus = True
                break


        allAutoLikeUsers = AutoLikeUser.objects.all()
        context = {
            'title':'Oto Beğeni Emri Oluştur',
            'starting':starting,
            'auto':allAutoLikeUsers,
        }

        return render(request,'custom_admin/instagram_tools/send-auto-postlike.html',context)


def articleView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        
        form = ArticleForm(request.POST or None, request.FILES or None)
        last_article = Article.objects.all().last()
        if last_article:
            form = ArticleForm(request.POST or None, request.FILES or None,instance=last_article)

        if 'articleCreate' in request.POST:
            form.save()
            return redirect('custom_admin:article')

        elif 'lastArticleUpdate' in request.POST:
            form.save()

            return redirect('custom_admin:article')

        context = {
            'title':'Makale',
            'last_article':last_article,
            'form':form,
        }

        return render(request,'custom_admin/article.html',context)
    else:
        raise Http404('not found')


def threadRunMention(x,last_user,dblog,ip_port_proxy,auth_proxy):
    pass

def getMentionData(userdata,dblog):

    startControl = True
    while startControl:
        last_control = Mentions.objects.filter(status=False).last()

        if last_control.id == dblog.id:
            startControl = False
            break

        time.sleep(30)
    threads = []
    last_user = userdata[-1]

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)


    for x in userdata:
        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        thread =  threading.Thread(target=threadRunMention,args=(x,last_user,dblog,process_ip_port_proxy,process_auth_proxy))
        thread.start()
        threads.append(thread)

         
        if len(threads) >= 40:
            for t in threads:
                t:threading.Thread
                
                t.join()
                threads.clear()


def mentionControlView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        file_error = False
        form = MentionForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form = form.save()
            print(form.rootfile.path)
            mentionfiledata  = open(form.rootfile.path,'r').read().splitlines()
            th = threading.Thread(target=getMentionData,args=(mentionfiledata,form))
            th.start()
            return redirect('custom_admin:mention-control')


        mentionControls = Mentions.objects.all()

        for x in mentionControls:
            btnName = f"errorUsersData{x.id}"
            if btnName in request.POST:
                try:

                    errorfile = open((BASE_DIR / 'static/mentionlogs/error_users_{}.txt'.format(x.id)),'r')
                    errorfiledata = errorfile.read()
                    errorfile.close()
                    response = HttpResponse(errorfiledata, content_type='application/text charset=utf-8')
                    response['Content-Disposition'] = 'attachment; filename="mention_error_users_file_no_{}.txt"'.format(x.id)
                    return response
                except:
                    file_error = True
                break

        for y in mentionControls:
            btnName2 = f"successUsersData{y.id}"
            if btnName2 in request.POST:
                try:

                    successfile = open((BASE_DIR / 'static/mentionlogs/succes_users_{}.txt'.format(y.id)),'r')
                    successfiledata = successfile.read()
                    successfile.close()
                    response = HttpResponse(successfiledata, content_type='application/text charset=utf-8')
                    response['Content-Disposition'] = 'attachment; filename="mention_success_users_file_no_{}.txt"'.format(y.id)
                    return response
                except:
                    file_error = True
                
                break

        for z in mentionControls:
            btnName2 = f"delete{z.id}"
            if btnName2 in request.POST:
                z.delete()
                return redirect('custom_admin:mention-control')



        context = {
            'title':'Mention Control',
            'form':form,
            'mentionControls':mentionControls,
            'file_error':file_error,
        }


        return render(request,'custom_admin/mention-control.html',context)
    else:
        raise Http404('not found')




def threadRunScanner(x,last_user,dblog,ip_port_proxy,auth_proxy):
    pass
                

def userScannerThread(userdata,dblog):

    startControl = True
    while startControl:
        last_control = UsersScanner.objects.filter(status=False).last()

        if last_control.id == dblog.id:
            startControl = False
            break

        time.sleep(30)
    threads = []
    last_user = userdata[-1]

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_after_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_after_proxy=True)


    for x in userdata:
        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        thread =  threading.Thread(target=threadRunScanner,args=(x,last_user,dblog,process_ip_port_proxy,process_auth_proxy))
        thread.start()
        threads.append(thread)

         
        if len(threads) >= 40:
            for t in threads:
                t:threading.Thread
                
                t.join()
                threads.clear()



def usersScannerView(request):

    if request.user.is_authenticated and request.user.is_superuser:
        file_error = False
        form = UsersScannerForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form = form.save()
            print(form.rootfile.path)
            usersdata  = open(form.rootfile.path,'r').read().splitlines()
            th = threading.Thread(target=userScannerThread,args=(usersdata,form))
            th.start()
            return redirect('custom_admin:users-scanner')


        usersscannerdata = UsersScanner.objects.all()

        for x in usersscannerdata:
            btnName = f"errorUsersData{x.id}"
            if btnName in request.POST:
                try:

                    errorfile = open((BASE_DIR / 'static/usersscannerlogs/error_users_{}.txt'.format(x.id)),'r')
                    errorfiledata = errorfile.read()
                    errorfile.close()
                    response = HttpResponse(errorfiledata, content_type='application/text charset=utf-8')
                    response['Content-Disposition'] = 'attachment; filename="error_users_file_no_{}.txt"'.format(x.id)
                    return response
                except:
                    file_error = True
                break

        for y in usersscannerdata:
            btnName2 = f"successUsersData{y.id}"
            if btnName2 in request.POST:
                try:

                    successfile = open((BASE_DIR / 'static/usersscannerlogs/succes_users_{}.txt'.format(y.id)),'r')
                    successfiledata = successfile.read()
                    successfile.close()
                    response = HttpResponse(successfiledata, content_type='application/text charset=utf-8')
                    response['Content-Disposition'] = 'attachment; filename="success_users_file_no_{}.txt"'.format(y.id)
                    return response
                except:
                    file_error = True
                
                break

        for z in usersscannerdata:
            btnName2 = f"delete{z.id}"
            if btnName2 in request.POST:
                z.delete()
                return redirect('custom_admin:users-scanner')



        context = {
            'title':'Kullanıcıları Tarama',
            'form':form,
            'usersscannerdata':usersscannerdata,
            'file_error':file_error,
        }


        return render(request,'custom_admin/users-scanner.html',context)
    else:
        raise Http404('not found')


def threadupdatetxt():

    all_users = InstagramCookies.objects.all()

    if all_users:
        os.remove(BASE_DIR / 'user_cookies/cookies.txt')

        file = open(BASE_DIR / 'user_cookies/cookies.txt','a+',encoding='utf-8')
        for z in all_users:

            data_str = f'{z.userid}::{z.authorization}::{z.claim}::{z.phoneid}::{z.waterfallid}::{z.guid}::{z.adid}::{z.deviceid}::{z.androidid}::{z.user_agent}::{z.pigeonid}::{z.mid}::{z.checksum}::{z.rur}\n'
            file.write(data_str)

        file.close()
        print(1)
        time.sleep(10)
        print(2)

    else:
        os.remove(BASE_DIR / 'user_cookies/cookies.txt')  

def updateTxtCookieView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        working = False
        if 'btnUpdateCookies' in request.POST:
            t = threading.Thread(target=threadupdatetxt,daemon=True)
            t.start()
            working = True            


        context = {
            'title':'Cookie TXT Yenile',
            'working':working,
        }

        return render(request,'custom_admin/add_cookie_data_txt.html',context)
    else:
        raise Http404('not found')


def sendAutoFollowView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:

        if "btnAutoFollow" in request.POST:
           
            username = request.POST['username']
            quantity = int(request.POST['quantity'])

            sv = get_object_or_404(Services, category__category_name="Oto Takipçi")
            order = Orders.objects.create(user=request.user,target=username,service=sv,charge=float(sv.rate),status='Completed',auto_process=True,user_order=True)
            AutoFollowUser.objects.create(username=username,quantity=quantity,order=order)

        allAutoFollowUsers = AutoFollowUser.objects.all()
        for x in allAutoFollowUsers:

            btnName = "btnDelete{}".format(x.id)

            if btnName in request.POST:
                x.delete()
                break


        allAutoFollowUsers = AutoFollowUser.objects.all()
        context = {
            'title':'Oto Takip Edileni Takip',
            'auto':allAutoFollowUsers,
        }

        return render(request,'custom_admin/instagram_tools/auto_follow.html',context)



def threadRunDMIgTvLinkDM(us,auth_proxy,ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass



def threadIgtvLinkDM(quantity,users_list,media_link,message1,link,message2,order,users_categories):
    dmmessagelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if quantity > len(userCookies):
        total_quantity = len(userCookies)

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMIgTvLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break



def sendIgtvLinkDmView(request):

    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False

        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            users = request.POST['users'].splitlines()

            users_categories = request.POST.getlist('user_category')

            format_data = request.POST['format']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')
            try:
                quantity = len(users)
                media_link = format_msg[0]
                message1 = format_msg[1]
                link = format_msg[2]
                message2 = format_msg[3]
                print(media_link,message1,link,message2)

                sv = get_object_or_404(Services, category__category_name="Igtv+Mesaj Link+Mesaj Toplu DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=media_link,status="Pending",user_order=True)

                def orderControl(user_order):
                    last_seo = SeoSettings.objects.all().last()
                    whileStatus = True
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False
                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadIgtvLinkDM,args=(quantity,users,media_link,message1,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False


                        time.sleep(5)
                    

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True


            except:
                formatError = True


            
        context = {
            'title':'Igvtv Link Mesaj Toplu DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/igtvlinkdm.html',context)



def startControlReelLink(c,users_categories):
    whileStatus = True
    while whileStatus:

        user_order = get_object_or_404(Orders,id=c.order.id)
        print('kontroller sağlanıyor...',user_order.cancelled)
        if user_order.cancelled:
                                    
            user_order.status = "Partial"
            user_order.remains = c.users_value
            user_order.save()
            whileStatus = False
            break

        if Orders.objects.filter(status='In Progress').count() == 0:

            if user_order.cancelled:
                                
                user_order.status = "Partial"
                user_order.remains = c.users_value
                user_order.save()
                whileStatus = False
                break
            orderLast = Orders.objects.filter(status='Pending').last()
                
            if user_order.id == orderLast.id:

                if user_order.cancelled:
                            
                    user_order.status = "Partial"
                    user_order.remains = c.users_value
                    user_order.save()
                    whileStatus = False
                else:
                    user_order.status = 'In Progress'
                    user_order.save()
                    print(c.users)
                    if c.user_follower_scanner:
                        users_list = get_followers_data(c.target_user,int(c.users_value))
                        print('users_list get_followers_data out : ',users_list)
                    else:
                        users_list = json.loads(str(c.users).replace("\'", "\""))
                    t1 = threading.Thread(target=threadReelLinkDM,args=(c.users_value,users_list,c.media_link,c.message1,c.link,c.message2,user_order,users_categories))
                    t1.start()
                    whileStatus = False


        time.sleep(5)

def startControlPostImageLink(c,users_categories):
    whileStatus = True
    while whileStatus:

        user_order = get_object_or_404(Orders,id=c.order.id)
        print('kontroller sağlanıyor...',user_order.cancelled)
        if user_order.cancelled:
                                    
            user_order.status = "Partial"
            user_order.remains = c.users_value
            user_order.save()
            whileStatus = False
            break

        if Orders.objects.filter(status='In Progress').count() == 0:

            if user_order.cancelled:
                                
                user_order.status = "Partial"
                user_order.remains = c.users_value
                user_order.save()
                whileStatus = False
                break
            orderLast = Orders.objects.filter(status='Pending').last()
                
            if user_order.id == orderLast.id:

                if user_order.cancelled:
                            
                    user_order.status = "Partial"
                    user_order.remains = c.users_value
                    user_order.save()
                    whileStatus = False
                else:
                    user_order.status = 'In Progress'
                    user_order.save()
                    print(c.users)
                    if c.user_follower_scanner:
                        users_list = get_followers_data(c.target_user,int(c.users_value))
                        print('users_list get_followers_data out : ',users_list)
                    else:
                        users_list = json.loads(str(c.users).replace("\'", "\""))
                    t1 = threading.Thread(target=threadImageLinkDM,args=(c.users_value,users_list,c.media_link,c.message1,c.link,c.message2,user_order,users_categories))
                    t1.start()
                    whileStatus = False


        time.sleep(5)


def startControlPostVideoLink(c,users_categories):
    whileStatus = True
    while whileStatus:

        user_order = get_object_or_404(Orders,id=c.order.id)
        print('kontroller sağlanıyor...',user_order.cancelled)
        if user_order.cancelled:
                                    
            user_order.status = "Partial"
            user_order.remains = c.users_value
            user_order.save()
            whileStatus = False
            break

        if Orders.objects.filter(status='In Progress').count() == 0:

            if user_order.cancelled:
                                
                user_order.status = "Partial"
                user_order.remains = c.users_value
                user_order.save()
                whileStatus = False
                break
            orderLast = Orders.objects.filter(status='Pending').last()
                
            if user_order.id == orderLast.id:

                if user_order.cancelled:
                            
                    user_order.status = "Partial"
                    user_order.remains = c.users_value
                    user_order.save()
                    whileStatus = False
                else:
                    user_order.status = 'In Progress'
                    user_order.save()
                    print(c.users)
                    if c.user_follower_scanner:
                        users_list = get_followers_data(c.target_user,int(c.users_value))
                        print('users_list get_followers_data out : ',users_list)
                    else:
                        users_list = json.loads(str(c.users).replace("\'", "\""))
                    t1 = threading.Thread(target=threadVideoLinkDM,args=(c.users_value,users_list,c.media_link,c.message1,c.link,c.message2,user_order,users_categories))
                    t1.start()
                    whileStatus = False


        time.sleep(5)



def startControlIgTvLink(c,users_categories):
    whileStatus = True
    while whileStatus:

        user_order = get_object_or_404(Orders,id=c.order.id)
        print('kontroller sağlanıyor...',user_order.cancelled)
        if user_order.cancelled:
                                    
            user_order.status = "Partial"
            user_order.remains = c.users_value
            user_order.save()
            whileStatus = False
            break

        if Orders.objects.filter(status='In Progress').count() == 0:

            if user_order.cancelled:
                                
                user_order.status = "Partial"
                user_order.remains = c.users_value
                user_order.save()
                whileStatus = False
                break
            orderLast = Orders.objects.filter(status='Pending').last()
                
            if user_order.id == orderLast.id:

                if user_order.cancelled:
                            
                    user_order.status = "Partial"
                    user_order.remains = c.users_value
                    user_order.save()
                    whileStatus = False
                else:
                    user_order.status = 'In Progress'
                    user_order.save()
                    print(c.users)
                    if c.user_follower_scanner:
                        users_list = get_followers_data(c.target_user,int(c.users_value))
                        print('users_list get_followers_data out : ',users_list)
                    else:
                        users_list = json.loads(str(c.users).replace("\'", "\""))
                    t1 = threading.Thread(target=threadIgtvLinkDM,args=(c.users_value,users_list,c.media_link,c.message1,c.link,c.message2,user_order,users_categories))
                    t1.start()
                    whileStatus = False


        time.sleep(5)
    

def threadRunDMReelLinkDM(us,auth_proxy,ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass





def threadReelLinkDM(quantity,users_list,media_link,message1,link,message2,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    print('userCookies : ',len(userCookies))

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    total_quantity = len(users_list)

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMReelLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break





def sendReelLinkDmView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')

            users = request.POST['users'].splitlines()
            format_data = request.POST['format']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')

            try:
                quantity = len(users)
                media_link = format_msg[0]
                message1 = format_msg[1]
                link = format_msg[2]
                message2 = format_msg[3]
                print(media_link,message1,link,message2)

                sv = get_object_or_404(Services, category__category_name="ReelVideo+Mesaj Link+Mesaj Toplu DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=media_link,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False
                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadReelLinkDM,args=(quantity,users,media_link,message1,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False


                        time.sleep(5)
                    

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True


            except:
                formatError = True


            
        context = {
            'title':'ReeL Video Ve Link Mesaj Toplu DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/reelvideolinkdm.html',context)



def threadRunProfileMessageDM(us,auth_proxy,ip_port_proxy,x,username,user_profile,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass


def threadRunProfileMessageLinkDM(us,auth_proxy,ip_port_proxy,x,username,user_profile,message,link,message2,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass



def threadProfilMessageLinkDM(quantity,users_list,user_profile,message,link,message2,order,users_categories):
    pass





def threadProfilMessageDM(quantity,users_list,user_profile,message,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    print('userCookies : ',len(userCookies))

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunProfileMessageDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,user_profile,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break



def threadProfilMessageDMFollowers(quantity,target_user,user_profile,message,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    print('userCookies : ',len(userCookies))

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    users_list = get_followers_data(target_user,quantity)
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)
    userSayac = 0

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunProfileMessageDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,user_profile,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break



def sendProfilMessageDmView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')

            users = request.POST['users'].splitlines()
            format_data = request.POST['format']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')

            try:
                quantity = len(users)
                user_profile = format_msg[0]
                message = format_msg[1]

                print(user_profile,message)

                sv = get_object_or_404(Services, category__category_name="Profil Sayfası + Mesaj Toplu DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=user_profile,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False

                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadProfilMessageDM,args=(quantity,users,user_profile,message,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False

                        time.sleep(5)

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True

            except Exception as e:
                print(e)
                formatError = True


            
        context = {
            'title':'Profil + Mesaj DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/profilpaylasmadm.html',context)




def sendProfilMessageDmLinkView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')

            users = request.POST['users'].splitlines()
            format_data = request.POST['format']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')

            try:
                quantity = len(users)
                user_profile = format_msg[0]
                message = format_msg[1]
                link = format_msg[2]
                message2 = format_msg[3]


                sv = get_object_or_404(Services, category__category_name="Profil Sayfası + Mesaj + Link Toplu DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=user_profile,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False

                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadProfilMessageLinkDM,args=(quantity,users,user_profile,message,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False

                        time.sleep(5)

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True

            except:
                formatError = True


            
        context = {
            'title':'Profil + Mesaj + Link DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/profilpaylasmadmlink.html',context)



def threadRunDMVideoLinkDM(us,auth_proxy,ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass



def threadVideoLinkDM(quantity,users_list,media_link,message1,link,message2,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMVideoLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break




def sendPostVideoLinkDmView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            users = request.POST['users'].splitlines()
            format_data = request.POST['format']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')
            try:
                quantity = len(users)
                media_link = format_msg[0]
                message1 = format_msg[1]
                link = format_msg[2]
                message2 = format_msg[3]
                print(media_link,message1,link,message2)

                sv = get_object_or_404(Services, category__category_name="PostVideo+Mesaj Link+Mesaj Toplu DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=media_link,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False
                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadVideoLinkDM,args=(quantity,users,media_link,message1,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False


                        time.sleep(5)
                    

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True


            except:
                formatError = True


            
        context = {
            'title':'Post Video Ve Link Mesaj Toplu DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/postvideolinkdm.html',context)



def threadRunDMImageLinkDM(us,auth_proxy,ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass




def threadImageLinkDM(quantity,users_list,media_link,message1,link,message2,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMImageLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break




def sendPostImageLinkDmView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            users = request.POST['users'].splitlines()
            format_data = request.POST['format']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')
            try:
                quantity = len(users)
                media_link = format_msg[0]
                message1 = format_msg[1]
                link = format_msg[2]
                message2 = format_msg[3]
                print(media_link,message1,link,message2)

                sv = get_object_or_404(Services, category__category_name="PostImage+Mesaj Link+Mesaj Toplu DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=media_link,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False
                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadImageLinkDM,args=(quantity,users,media_link,message1,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False


                        time.sleep(5)
                    

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True


            except:
                formatError = True


            
        context = {
            'title':'Post Resim Ve Link Mesaj Toplu DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,

        }

        return render(request,'custom_admin/instagram_tools/postimagelinkdm.html',context)




def affirmationsView(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        affirmations_list = Affirmations.objects.all()
        
        for c in affirmations_list:


            btnName = 'btnConfirm' + str(c.id)
            if btnName in request.POST:
                if c.service.category.category_name == 'ReelVideo+Mesaj Link+Mesaj Toplu DM':
                    sv = c.service
                    if sv.packpages:
                        users_categories = [x.id for x in sv.packpages.category.all()]
                    else:
                        users_categories= []

                    t_o = threading.Thread(target=startControlReelLink,args=(c,users_categories),daemon=True)
                    t_o.start()

                elif c.service.category.category_name == 'Igtv+Mesaj Link+Mesaj Toplu DM':
                    sv = c.service
                    if sv.packpages:
                        users_categories = [x.id for x in sv.packpages.category.all()]
                    else:
                        users_categories= []

                    t_o = threading.Thread(target=startControlIgTvLink,args=(c,users_categories),daemon=True)
                    t_o.start()

                elif c.service.category.category_name == 'PostVideo+Mesaj Link+Mesaj Toplu DM':
                    sv = c.service
                    if sv.packpages:
                        users_categories = [x.id for x in sv.packpages.category.all()]
                    else:
                        users_categories= []

                    t_o = threading.Thread(target=startControlPostVideoLink,args=(c,users_categories),daemon=True)
                    t_o.start()

                elif c.service.category.category_name == 'PostImage+Mesaj Link+Mesaj Toplu DM':
                    sv = c.service
                    if sv.packpages:
                        users_categories = [x.id for x in sv.packpages.category.all()]
                    else:
                        users_categories= []

                    t_o = threading.Thread(target=startControlPostImageLink,args=(c,users_categories),daemon=True)
                    t_o.start()

                elif c.service.category.category_name == 'PostImage+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM':
                    sv = c.service
                    if sv.packpages:
                        users_categories = [x.id for x in sv.packpages.category.all()]
                    else:
                        users_categories= []

                    t_o = threading.Thread(target=startControlPostImageLink,args=(c,users_categories),daemon=True)
                    t_o.start()


                elif c.service.category.category_name == 'PostVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM':
                    sv = c.service
                    if sv.packpages:
                        users_categories = [x.id for x in sv.packpages.category.all()]
                    else:
                        users_categories= []

                    t_o = threading.Thread(target=startControlPostVideoLink,args=(c,users_categories),daemon=True)
                    t_o.start()

                elif c.service.category.category_name == 'Igtv+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM':
                    sv = c.service
                    if sv.packpages:
                        users_categories = [x.id for x in sv.packpages.category.all()]
                    else:
                        users_categories= []

                    t_o = threading.Thread(target=startControlIgTvLink,args=(c,users_categories),daemon=True)
                    t_o.start()


                elif c.service.category.category_name == 'ReelVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM':
                    sv = c.service
                    if sv.packpages:
                        users_categories = [x.id for x in sv.packpages.category.all()]
                    else:
                        users_categories= []

                    t_o = threading.Thread(target=startControlReelLink,args=(c,users_categories),daemon=True)
                    t_o.start()

                print('order in progress.',c.order.status)
                starting = True
                c.delete()

                return redirect('custom_admin:api-order-affirmations')


            btnName2 = 'btnCancel' + str(c.id)
            if btnName2 in request.POST:

                c.order.status = 'Partial'
                c.order.remains = c.users_value
                c.order.save()

                c.delete()
                return redirect('custom_admin:api-order-affirmations')


        context = {
            'title':'Api Sipariş Onaylamaları',
            'affirmations_list':affirmations_list,
        }

        return render(request,'custom_admin/api-order-affirmations.html',context)





def userCategoryView(request):
    if request.user.is_authenticated and request.user.is_superuser:

        user_categories_list = UsersCategories.objects.all()
        form = UserCategoriesForm(request.POST or None)

        if 'btnSave' in request.POST and form.is_valid():

            form.save()

            return redirect('custom_admin:user-categories')
        else:
            if request.method == 'POST':

                for x in user_categories_list:
                    btnName = 'btnDelete' + str(x.id)
                    if btnName in request.POST:
                        x.delete()
                        return redirect('custom_admin:user-categories')

        context = {
            'title':'Kullanıcı Kategorileri',
            'user_categories_list':user_categories_list,
            'form':form,
        }

        return render(request,'custom_admin/user-category-list.html',context)



def editUserCategoryView(request,id):
    if request.user.is_authenticated and request.user.is_superuser:

        user_categories = get_object_or_404(UsersCategories,id=id)
        form = UserCategoriesForm(request.POST or None,instance=user_categories)

        if 'btnSave' in request.POST and form.is_valid():
            form.save()

            return redirect('custom_admin:user-categories')


        context = {
            'title':'Kullanıcı Kategori Düzenle',
            'form':form,
        }

        return render(request,'custom_admin/edit-user-category.html',context)





def errorUsersView(request):
    pass


def get_followers_data(username,quantity):
    pass


def threadDMTopluMessageFollowers(quantity,target_username,link,message,order,users_categories):
    dmmessagelog = {}
    users_list = []
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []

    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    users_list = get_followers_data(target_username,quantity)
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]
    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)
    userSayac = 0

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        print('username : ',username)

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1
        
        thread =  threading.Thread(target=threadRunDMTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break




def sendDMTopluMessageFollowersView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            quantity = int(request.POST.get('quantity', None))

            link = request.POST.get('link', None)
            link = link.replace('https://','')
            link = link.replace('http://','')
            split_link = link.split(':')

            target_username = split_link[0]
            link = split_link[1]
            message = split_link[2]

            users_categories = request.POST.getlist('user_category')

            sv = get_object_or_404(Services, category__category_name="DM Toplu Link Kullanıcı Takipçi Taramalı Mesaj")

            user_order = Orders.objects.create(user=request.user,target=target_username,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMTopluMessageFollowers,args=(quantity,target_username,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM Toplu Takipçi Taramalı Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dm-toplu-message-followers.html',context)


def threadDMResimTopluMessageFollowers(quantity,target_user,link,message,order,users_categories):
    dmmessagelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    users_list = get_followers_data(target_user,total_quantity)
    print("users_list : ",users_list)
    userSayac = 0

    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()


    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMResimTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break


def sendDMResimTopluMessageFollowersView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            quantity = int(request.POST.get('quantity', None))

            link = request.POST.get('link', None)
            link = link.replace('https://','')
            link = link.replace('http://','')
            split_link = link.split(':')

            target_username = split_link[0]
            link = split_link[1]
            message = split_link[2]

            users_categories = request.POST.getlist('user_category')

            sv = get_object_or_404(Services, category__category_name="DM Resim Toplu Kullanıcı Takipçi Taramalı Mesaj")

            user_order = Orders.objects.create(user=request.user,target=target_username,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMResimTopluMessageFollowers,args=(quantity,target_username,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM Resim Toplu Takipçi Taramalı Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dmresim-toplu-message-followers.html',context)



def threadRunDMVideoTopluMessage(us,auth_proxy,ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass



def threadDMVideoTopluMessageFollowers(quantity,target_user,link,message,order,users_categories):
    dmmessagelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    users_list = get_followers_data(target_user,total_quantity)
    print("users_list : ",users_list)
    userSayac = 0
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMVideoTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break



def sendDMVideoTopluMessageFollowersView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            quantity = int(request.POST.get('quantity', None))

            link = request.POST.get('link', None)
            link = link.replace('https://','')
            link = link.replace('http://','')
            split_link = link.split(':')

            target_username = split_link[0]
            link = split_link[1]
            message = split_link[2]

            users_categories = request.POST.getlist('user_category')

            sv = get_object_or_404(Services, category__category_name="DM Video Toplu Kullanıcı Takipçi Taramalı Mesaj")

            user_order = Orders.objects.create(user=request.user,target=target_username,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMVideoTopluMessageFollowers,args=(quantity,target_username,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM Video Toplu Takipçi Taramalı Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dmvideo-toplu-message-followers.html',context)




def threadRunDMIGTVTopluMessage(us,auth_proxy,ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass





def threadDMIGTVTopluMessageFollowers(quantity,target_user,link,message,order,users_categories):
    dmmessagelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    users_list = get_followers_data(target_user,total_quantity)
    print("users_list : ",users_list)
    userSayac = 0
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)
    
    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()    
    
    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMIGTVTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break




def sendDMIgtvTopluMessageFollowersView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            quantity = int(request.POST.get('quantity', None))

            link = request.POST.get('link', None)
            link = link.replace('https://','')
            link = link.replace('http://','')
            split_link = link.split(':')

            target_username = split_link[0]
            link = split_link[1]
            message = split_link[2]

            users_categories = request.POST.getlist('user_category')

            sv = get_object_or_404(Services, category__category_name="DM IGTV Toplu Kullanıcı Takipçi Taramalı Mesaj")

            user_order = Orders.objects.create(user=request.user,target=target_username,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMIGTVTopluMessageFollowers,args=(quantity,target_username,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM IGTV Toplu Takipçi Taramalı Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dmigtv-toplu-message-followers.html',context)



def threadRunDMReelTopluMessage(us,auth_proxy,ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,textUser,users_categories):
    pass




def threadDMReelTopluMessageFollowers(quantity,target_user,link,message,order,users_categories):
    dmmessagelog = {}
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')
    users_list = get_followers_data(target_user,total_quantity)
    print("users_list : ",users_list)
    userSayac = 0
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMReelTopluMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,link,message,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break



def sendDMReelTopluMessageFollowersView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            quantity = int(request.POST.get('quantity', None))

            link = request.POST.get('link', None)
            link = link.replace('https://','')
            link = link.replace('http://','')
            split_link = link.split(':')

            target_username = split_link[0]
            link = split_link[1]
            message = split_link[2]

            users_categories = request.POST.getlist('user_category')

            sv = get_object_or_404(Services, category__category_name="DM Reel Video Toplu Kullanıcı Takipçi Taramalı Mesaj")

            user_order = Orders.objects.create(user=request.user,target=target_username,service=sv,charge=float(sv.rate),status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
                    print('kontroller sağlanıyor...',user_order.cancelled)
                    if user_order.cancelled:
                                                
                        user_order.status = "Partial"
                        user_order.remains = quantity
                        user_order.save()
                        whileStatus = False
                        break

                    if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                        if user_order.cancelled:
                                            
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break
                        orderLast = Orders.objects.filter(status='Pending').last()
                            
                        if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                        
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                            else:
                                user_order.status = 'In Progress'
                                user_order.save()
                                t1 = threading.Thread(target=threadDMReelTopluMessageFollowers,args=(quantity,target_username,link,message,user_order,users_categories))
                                t1.start()
                                whileStatus = False


                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True
        context = {
            'title':'DM Reel Video Toplu Takipçi Taramalı Mesaj Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/dmreel-toplu-message-followers.html',context)



def threadImageLinkDMFollowers(quantity,target_user,media_link,message1,link,message2,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    users_list = get_followers_data(target_user,quantity)
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)
    userSayac = 0

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMImageLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break




def sendPostImageLinkDmFollowersView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            format_data = request.POST['link']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')
            try:
                quantity = int(request.POST['quantity'])
                target_user = format_msg[0]
                media_link = format_msg[1]
                message1 = format_msg[2]
                link = format_msg[3]
                message2 = format_msg[4]
                print(target_user,media_link,message1,link,message2)

                sv = get_object_or_404(Services, category__category_name="PostImage+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=media_link,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False
                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadImageLinkDMFollowers,args=(quantity,target_user,media_link,message1,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False


                        time.sleep(5)
                    

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True


            except:
                formatError = True


            
        context = {
            'title':'Post Resim Ve Link Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,

        }

        return render(request,'custom_admin/instagram_tools/postimagelinkdm-followers.html',context)



def threadVideoLinkDMFollowers(quantity,target_user,media_link,message1,link,message2,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    users_list = get_followers_data(target_user,quantity)
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)
    userSayac = 0

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMVideoLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break





def sendPostVideoLinkDmFollowersView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            format_data = request.POST['link']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')
            try:
                quantity = int(request.POST['quantity'])
                target_user = format_msg[0]
                media_link = format_msg[1]
                message1 = format_msg[2]
                link = format_msg[3]
                message2 = format_msg[4]
                print(target_user,media_link,message1,link,message2)

                sv = get_object_or_404(Services, category__category_name="PostVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=media_link,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False
                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadVideoLinkDMFollowers,args=(quantity,target_user,media_link,message1,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False


                        time.sleep(5)
                    

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True


            except:
                formatError = True


            
        context = {
            'title':'Post Video Ve Link Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,

        }

        return render(request,'custom_admin/instagram_tools/postvideolinkdm-followers.html',context)




def threadIGTVLinkDMFollowers(quantity,target_user,media_link,message1,link,message2,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    users_list = get_followers_data(target_user,quantity)
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)
    userSayac = 0

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMIgTvLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break




def sendPostIGTVLinkDmFollowersView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            format_data = request.POST['link']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')
            try:
                quantity = int(request.POST['quantity'])
                target_user = format_msg[0]
                media_link = format_msg[1]
                message1 = format_msg[2]
                link = format_msg[3]
                message2 = format_msg[4]
                print(target_user,media_link,message1,link,message2)

                sv = get_object_or_404(Services, category__category_name="Igtv+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=media_link,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False
                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadIGTVLinkDMFollowers,args=(quantity,target_user,media_link,message1,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False


                        time.sleep(5)
                    

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True


            except Exception as e:
                formatError = True
                print(e)


            
        context = {
            'title':'IGTV+Mesaj Ve Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,

        }

        return render(request,'custom_admin/instagram_tools/postigtvlinkdm-followers.html',context)


def threadReelLinkDMFollowers(quantity,target_user,media_link,message1,link,message2,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        
    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    users_list = get_followers_data(target_user,quantity)
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)
    userSayac = 0

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunDMReelLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,media_link,message1,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break




def sendPostReelLinkDmFollowersView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()

        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')
            format_data = request.POST['link']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')
            try:
                quantity = int(request.POST['quantity'])
                target_user = format_msg[0]
                media_link = format_msg[1]
                message1 = format_msg[2]
                link = format_msg[3]
                message2 = format_msg[4]
                print(target_user,media_link,message1,link,message2)

                sv = get_object_or_404(Services, category__category_name="ReelVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=media_link,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False
                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadReelLinkDMFollowers,args=(quantity,target_user,media_link,message1,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False


                        time.sleep(5)
                    

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True


            except Exception as e:
                formatError = True
                print(e)


            
        context = {
            'title':'ReelVideo Mesaj Ve Link Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,

        }

        return render(request,'custom_admin/instagram_tools/reellinkdm-followers.html',context)



def sendProfilMessageDmFollowersView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')

            quantity = int(request.POST['quantity'])
            format_data = request.POST['link']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')

            try:
                target_user = format_msg[0]
                user_profile = format_msg[1]
                message = format_msg[2]

                print(user_profile,message)

                sv = get_object_or_404(Services, category__category_name="Profil Sayfası + Mesaj Kullanıcı Takipçi Taramalı DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=user_profile,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False

                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadProfilMessageDMFollowers,args=(quantity,target_user,user_profile,message,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False

                        time.sleep(5)

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True

            except Exception as e:
                print(e)
                formatError = True


            
        context = {
            'title':'Profil + Mesaj Kullanıcı Takipçi Taramalı DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/profilpaylasmadm-followers.html',context)



def threadProfilMessageLinkDMFollowers(quantity,target_user,user_profile,message,link,message2,order,users_categories):
    dmmessagelog = {}   
    if users_categories:

        userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True).order_by('?')
        
        cleaned_up_list = []

        for somemodel in userCookies:
            if somemodel not in cleaned_up_list:
                cleaned_up_list.append(somemodel)

        userCookies = cleaned_up_list
    
    else:
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        

    print('userCookies : ',len(userCookies))

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    users_list = get_followers_data(target_user,quantity)
    if len(users_list) > quantity:
        users_list = users_list[0:quantity]

    total_quantity = len(users_list)
    if total_quantity > len(userCookies):
        total_quantity = len(userCookies)

    userSayac = 0

    print('total_quantity : ',total_quantity)

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    for x in range(0, total_quantity):
                        
        username = users_list[x]

        process_ip_port_proxy = None
        process_auth_proxy = None

        if process_ip_port_proxy_list:

            process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
        if process_auth_proxy_list:

            process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

        if userSayac >= len(userCookies):
            userSayac = 0

        us = userCookies[userSayac]
        userSayac += 1

        thread =  threading.Thread(target=threadRunProfileMessageLinkDM,args=(us,process_auth_proxy,process_ip_port_proxy,x,username,user_profile,message,link,message2,order,quantity,total_quantity,errorFile,us.user.username,users_categories))
        dmmessagelog[x] = thread
        dmmessagelog[x].start()

        threads.append(thread)

        cancellStatus = orderCancelControl(order.id)
        if len(threads) >= last_seo.proxy_limit and cancellStatus == False:
            for t in threads:
                t:threading.Thread
                t.join() 
                threads.clear()

        elif cancellStatus:
            order.status = "Partial"
            order.remains = int(quantity) - order.successful_value
            order.cancelled = True
            order.save()

            get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(order.service.service)).last()
            
            if get_this_service_log:
                get_this_service_log.successful_value += int(order.successful_value)
                get_this_service_log.save()
            else:
                ServicesSuccessfulLog.objects.create(service_id=order.service.service,service_name=order.service.name,successful_value=int(order.successful_value))


            break



def sendProfilMessageDmLinkFollowersView(request):
    
    
    if request.user.is_authenticated and request.user.is_superuser:
        formatError = False
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if 'btnSend' in request.POST:
            users_categories = request.POST.getlist('user_category')

            quantity = int(request.POST['quantity'])
            format_data = request.POST['link']
            format_data = format_data.replace('https://','')
            format_data = format_data.replace('http://','')
            format_msg = format_data.split(':')

            try:

                target_user = format_msg[0]
                user_profile = format_msg[1]
                message = format_msg[2]
                link = format_msg[3]
                message2 = format_msg[4]


                sv = get_object_or_404(Services, category__category_name="Profil Sayfası + Mesaj + Link Kullanıcı Takipçi Taramalı DM")

                user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=user_profile,status="Pending",user_order=True)

                def orderControl(user_order):
                    whileStatus = True
                    last_seo = SeoSettings.objects.all().last()
                    while whileStatus:

                        user_order = get_object_or_404(Orders,id=user_order.id)
                        print('kontroller sağlanıyor...',user_order.cancelled)
                        if user_order.cancelled:
                                                    
                            user_order.status = "Partial"
                            user_order.remains = quantity
                            user_order.save()
                            whileStatus = False
                            break

                        if Orders.objects.filter(status='In Progress').count() == 0 or last_seo.process_queue_disabled:

                            if user_order.cancelled:
                                                
                                user_order.status = "Partial"
                                user_order.remains = quantity
                                user_order.save()
                                whileStatus = False
                                break
                            orderLast = Orders.objects.filter(status='Pending').last()
                                
                            if user_order.id == orderLast.id or last_seo.process_queue_disabled:

                                if user_order.cancelled:
                                            
                                    user_order.status = "Partial"
                                    user_order.remains = quantity
                                    user_order.save()
                                    whileStatus = False

                                else:
                                    user_order.status = 'In Progress'
                                    user_order.save()
                                    t1 = threading.Thread(target=threadProfilMessageLinkDMFollowers,args=(quantity,target_user,user_profile,message,link,message2,user_order,users_categories))
                                    t1.start()
                                    whileStatus = False

                        time.sleep(5)

                t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
                t_o.start()
                print('order oluşturuldu.',user_order.status)
                starting = True

            except:
                formatError = True


            
        context = {
            'title':'Profil + Mesaj + Link Kullanıcı Takipçi Taramalı DM',
            'formatError':formatError,
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/profilpaylasmadmlink-followers.html',context)

def threadStopControl(errorFile,user_order,quantity,sleeptime,media_link):
    turning_control_value = -1
    while True:
        print('stop control çalışıyor...')
        if user_order.successful_value == quantity or turning_control_value == user_order.successful_value:
            try:

                readfile =  open(os.path.realpath(errorFile.name),'r')

                errorFile.close()
                errorCount = 0
                for x in readfile.readlines():
                    if x:
                        errorCount += 1
                        icuser = InstagramCookies.objects.filter(user__username=x.replace('\n','')).last()
                        if icuser.error_count <= 3:
                            print('hata kaydı yapıldı , ',icuser.user.username)
                            icuser.error_count +=1
                            icuser.save()
                        
                try:
                    remove_path = os.path.realpath(readfile.name)
                    readfile.close()
                    os.remove(remove_path)
                except:
                    pass

                if media_link:

                    sayac_value = getVideoSayac(media_link)
                    get_log = VideoSayacLog.objects.filter(order=user_order).last()
                    print('getting sayac value : ',sayac_value)
                    successfull_value = sayac_value - get_log.sayac_value
                    print('successfull_value : ',successfull_value)
                    addValue = 0
                    if successfull_value >= user_order.successful_value:
                        addValue = quantity
                    else:
                        addValue = successfull_value

                    get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
                    
                    if get_this_service_log:
                        get_this_service_log.successful_value += int(addValue)
                        get_this_service_log.save()
                    else:
                        ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(addValue))                    
                
                #default
                else:

                    get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
                    
                    if get_this_service_log:
                        get_this_service_log.successful_value += int(user_order.successful_value)
                        get_this_service_log.save()
                    else:
                        ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(user_order.successful_value))
                
            
            except:
                print('stop kontrol kırıldı döngü sona erdi')
                break
            print('stop kontrol sona erdi')
            break
        turning_control_value = user_order.successful_value
        time.sleep(sleeptime)

def multiRunProfileVisit(us,auth_proxy,ip_port_proxy,x,user_order,quantity,total_quantity,follow_user,errorFile,textUser):
    pass

def threadProfileVisit(quantity,user_order,follow_user,users_categories):
    followislemlog = {}
    userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True)
    cleaned_up_list = []

    for somemodel in userCookies:
        if somemodel not in cleaned_up_list:
            cleaned_up_list.append(somemodel)

    userCookies = cleaned_up_list

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if len(userCookies) < total_quantity:
        total_quantity = len(userCookies)

    video_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,video_proxy=True)
    video_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,video_proxy=True)
    threads = []

    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    userSayac = 0    

    if len(userCookies) == 0:

        user_order.status = "Partial"
        user_order.remains = int(quantity) - user_order.successful_value
        user_order.cancelled = True
        user_order.save()
    else:

        for x in range(0, total_quantity):

            video_ip_port_proxy = None
            video_auth_proxy = None

            if video_ip_port_proxy_list:
                video_ip_port_proxy = video_ip_port_proxy_list[random.randrange(len(video_ip_port_proxy_list))]
                
            if video_auth_proxy_list:
                video_auth_proxy = video_auth_proxy_list[random.randrange(len(video_auth_proxy_list))]


            if userSayac >= len(userCookies):
                userSayac = 0

            us = userCookies[userSayac]
            userSayac += 1
            thread =  threading.Thread(target=multiRunProfileVisit,args=(us,video_auth_proxy,video_ip_port_proxy,x,user_order,quantity,total_quantity,follow_user,errorFile,us.user.username))
            followislemlog[x] = thread
            followislemlog[x].start()

            threads.append(thread)
            
            cancellStatus = orderCancelControl(user_order.id)
            if len(threads) >= last_seo.proxy_limit_video and cancellStatus == False:
                for t in threads:
                    t:threading.Thread
                    t.join() 
                    threads.clear()

            elif cancellStatus:
                user_order.status = "Partial"
                user_order.remains = int(quantity) - user_order.successful_value
                user_order.cancelled = True
                user_order.save()

                get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
                
                if get_this_service_log:
                    get_this_service_log.successful_value += int(user_order.successful_value)
                    get_this_service_log.save()
                else:
                    ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(user_order.successful_value))


                break




def sendProfileVisitView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if "btnStart" in request.POST:
            
            insta_user= request.POST['username']

            users_categories = request.POST.getlist('user_category')
            # Takip edilecek kişi nin kullanıcı adını alıyoruz.
            insta_user = insta_user.replace('https://www.instagram.com/','')
            insta_user = insta_user.replace('www.instagram.com/','')
            insta_user = insta_user.replace('/','')

            quantity = int(request.POST['quantity'])
            sv = get_object_or_404(Services, category__category_name="Profil Ziyaret")

            user_order = Orders.objects.create(user=request.user,target=insta_user,service=sv,charge=float(sv.rate),status="Completed",user_order=True)
            print('order oluşturuldu.',user_order.status)

            t1 = threading.Thread(target=threadProfileVisit,args=(quantity,user_order,insta_user,users_categories))
            t1.start()  
                
            starting = True
        context = {
            'title':'Profil Ziyareti Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/profile-visit.html',context)
    else:
        raise Http404('not found')





def multiRunVideoView(us,auth_proxy,ip_port_proxy,x,user_order,quantity,total_quantity,media_link,errorFile,textUser,target_sayac):
    pass

from custom_admin.models import VideoSayacLog

def getVideoSayac(media_link):
    pass





def threadVideoView(quantity,user_order,media_link,users_categories):
    followislemlog = {}
    userCookies = InstagramCookies.objects.filter(user__otherinfo__category__id__in=users_categories,active=True)
    cleaned_up_list = []

    for somemodel in userCookies:
        if somemodel not in cleaned_up_list:
            cleaned_up_list.append(somemodel)

    userCookies = cleaned_up_list

    last_seo = SeoSettings.objects.all().last()                  

    total_quantity = quantity
    if len(userCookies) < total_quantity:
        total_quantity = len(userCookies)

    video_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,video_proxy=True)
    video_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,video_proxy=True)
    threads = []

    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    userSayac = 0    

    if len(userCookies) == 0:

        user_order.status = "Partial"
        user_order.remains = int(quantity) - user_order.successful_value
        user_order.cancelled = True
        user_order.save()
    else:
        sayac_value = getVideoSayac(media_link)
        user_order.start_count = sayac_value
        user_order.save()
        VideoSayacLog.objects.create(order=user_order,sayac_value=sayac_value)
        for x in range(0, total_quantity):

            video_ip_port_proxy = None
            video_auth_proxy = None

            if video_ip_port_proxy_list:
                video_ip_port_proxy = video_ip_port_proxy_list[random.randrange(len(video_ip_port_proxy_list))]
                
            if video_auth_proxy_list:
                video_auth_proxy = video_auth_proxy_list[random.randrange(len(video_auth_proxy_list))]


            if userSayac >= len(userCookies):
                userSayac = 0

            us = userCookies[userSayac]
            userSayac += 1
            thread =  threading.Thread(target=multiRunVideoView,args=(us,video_auth_proxy,video_ip_port_proxy,x,user_order,quantity,total_quantity,media_link,errorFile,us.user.username,sayac_value))
            followislemlog[x] = thread
            followislemlog[x].start()

            threads.append(thread)
            
            cancellStatus = orderCancelControl(user_order.id)
            if len(threads) >= last_seo.proxy_limit_video and cancellStatus == False:
                for t in threads:
                    t:threading.Thread
                    t.join() 
                    threads.clear()

            elif cancellStatus:
                user_order.status = "Partial"
                user_order.remains = int(quantity) - user_order.successful_value
                user_order.cancelled = True
                user_order.save()
                
                get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id=str(user_order.service.service)).last()
                
                if get_this_service_log:
                    get_this_service_log.successful_value += int(user_order.successful_value)
                    get_this_service_log.save()
                else:
                    ServicesSuccessfulLog.objects.create(service_id=user_order.service.service,service_name=user_order.service.name,successful_value=int(user_order.successful_value))
                break




def sendVideoView(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        starting = False
        get_user_categories = UsersCategories.objects.all()
        if "btnStart" in request.POST:
            
            users_categories = request.POST.getlist('user_category')

            media_link= request.POST['link']
            quantity = int(request.POST['quantity'])
            sv = get_object_or_404(Services, category__category_name="Video İzleme")

            user_order = Orders.objects.create(user=request.user,target=media_link,service=sv,charge=float(sv.rate),status="Completed",user_order=True)
            print('order oluşturuldu.',user_order.status)

            t1 = threading.Thread(target=threadVideoView,args=(quantity,user_order,media_link,users_categories))
            t1.start()  
                
            starting = True
        context = {
            'title':'Video İzleme Gönder',
            'starting':starting,
            'get_user_categories':get_user_categories,
        }

        return render(request,'custom_admin/instagram_tools/video-view.html',context)
    else:
        raise Http404('not found')   
    
    
    
""" 
def notLoginUsersView(request):     pass
def sendVideoView(request):     pass
def successfulValueView(request):     pass
def userPackpagesView(request):     pass
def usersDataView(request):     pass
def servicesview(request):     pass
def apiSettingsView(request):     pass
def importUsersView(request):     pass
def exportUsersView(request):     pass
def editServicesView(request):    pass
def editUserPackpagesView(request):     pass
def seoSettingsView(request):     pass        
def homeManagerView(request):     pass
def addProxyView(request):     pass
def clearAccountsView(request):     pass
def sendFollowView(request):     pass
def sendPostCommentView(request):     pass
def sendPostLikeView(request):     pass
def sendDMMessageView(request):     pass
def sendCommentLiveView(request):     pass
def sendLikeLiveView(request):     pass
def sendWatchLiveView(request):     pass
def savePhotoView(request):     pass
def webApiContactView(request):     pass
def webApiContactManage(request):     pass
def sendDMTopluMessageView(request):    pass
def getUserFollowDataView(request):     pass
def sendDMResimTopluMessageView(request):     pass
def sendDMVideoTopluMessageView(request):     pass
def sendAutoPostLikeView(request):     pass 
def sendDMIgTvTopluMessageView(request):     pass
def sendDMReelTopluMessageView(request):     pass
def articleView(request): pass
def mentionControlView(request): pass
def usersScannerView(request): pass
def updateTxtCookieView(request): pass 
def sendAutoFollowView(request): pass 
def sendIgtvLinkDmView(request): pass 
def affirmationsView(request): pass 
def sendReelLinkDmView(request): pass 
def sendPostVideoLinkDmView(request): pass 
def sendPostImageLinkDmView(request): pass 
def userCategoryView(request): pass 
def editUserCategoryView(request): pass 
def usersActivePasifView(request): pass 
def usersCategoriesUserList(request): pass 
def errorUsersView(request): pass 
def notLoginOldUsersView(request): pass 
def smtpSettingsView(request): pass 
def sendProfilMessageDmView(request): pass 
def sendProfilMessageDmLinkView(request): pass 
def sendDMTopluMessageFollowersView(request): pass 
def sendDMResimTopluMessageFollowersView(request): pass 
def sendDMVideoTopluMessageFollowersView(request): pass 
def sendDMIgtvTopluMessageFollowersView(request): pass 
def sendDMReelTopluMessageFollowersView(request): pass 
def sendPostImageLinkDmFollowersView(request): pass 
def sendPostVideoLinkDmFollowersView(request): pass 
def sendPostIGTVLinkDmFollowersView(request): pass 
def sendPostReelLinkDmFollowersView(request): pass 
def sendProfilMessageDmFollowersView(request): pass 
def sendProfilMessageDmLinkFollowersView(request): pass 
def successfulValueEditView(request): pass 
def successfulValueEditServiceView(request): pass 
def sendProfileVisitView(request): pass """