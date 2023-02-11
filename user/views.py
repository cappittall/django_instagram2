
from user.models import InstagramCookies, OtherInfo
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required

import random
import time


from services.models import Orders,Services
import threading
import binascii,os
from custom_admin.models import Proxy,SeoSettings
from pathlib import Path
import requests
BASE_DIR = Path(__file__).resolve().parent.parent


import base64

def set_proxy_ip_port(proxy):

    hostnamegel = proxy.split(":")[0]
    portgel = proxy.split(":")[1]

    proxy = hostnamegel + ":" + portgel

    proxyson = {'https': 'http://' + proxy}

    return proxyson

def set_proxy_auth(proxy):
    hostnamegel = proxy.split(":")[0]
    portgel = proxy.split(":")[1]
    userhostname = proxy.split(":")[2]
    passhostname = proxy.split(":")[3]

    proxydd1 = userhostname + ":" + passhostname
    port1a = hostnamegel + ":" + portgel
    hostname = proxydd1
    port = port1a
    proxy = hostname + "@" + port

    return {'https': 'http://' + proxy}

def base64image(url):
    
    linkom = url
    atakan = requests.get(linkom,verify=True, timeout=20)
    ata = base64.b64encode(atakan.content)

    sonmedya = "data:image/jpeg;base64,{}".format(str(ata.decode()))
    return sonmedya


def orderCancelControl(id):
    
    order_ = Orders.objects.filter(id=id).last()
    if order_:

        return order_.cancelled

    else:
        return False

@login_required(login_url='/login/')
def userView(request,username):
    pass

def multiRunFollow(us,auth_proxy,ip_port_proxy,x,user_order,quantity,total_quantity,follow_user,errorFile,textUser):
    pass

def threadFollow(quantity,user_order,follow_user):
    followislemlog = {}
    userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
    last_seo = SeoSettings.objects.all().last()

    total_quantity = quantity
    if len(userCookies) < total_quantity:
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
            user_order.remains = quantity - user_order.successful_value
            user_order.cancelled = True
            user_order.save()
            break
        


def threadRunComment(us,auth_proxy,ip_port_proxy,x,comm,quantity,comment_media,comment_media_id,total_quantity,comment_list,user_order,errorFile,textUser):
            
    pass


def threadComment(quantity,comment_list,comment_media,comment_media_id,user_order):
                    
    userCookies = InstagramCookies.objects.filter(active=True).order_by('?')

    total_quantity = quantity

    postcomlog = {}
    last_seo = SeoSettings.objects.all().last()

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    userSayac = 0    
    threads = []

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
        thread = threading.Thread(target=threadRunComment,args=(us,process_auth_proxy,process_ip_port_proxy,x,comm,quantity,comment_media,comment_media_id,total_quantity,comment_list,user_order,errorFile,us.user.username))
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
            user_order.remains = quantity - user_order.successful_value
            user_order.cancelled = True
            user_order.save()
            break


def threadRunLike(us,auth_proxy,ip_port_proxy,x,order,like_media,like_media_id,quantity,total_quantity,errorFile,textUser):

    pass

def threadLike(quantity,user_order,user_media,user_media_id):
    pass

@login_required(login_url='/login/')
def otherProfileView(request):
    pass


@login_required(login_url='/login/')
def sendFollowView(request):
    pass




@login_required(login_url='/login/')
def sendPostLikeView(request):
    pass





@login_required(login_url='/login/')
def sendPostCommentView(request):

    if request.user.is_authenticated:
        starting = False

        if 'btnSend' in request.POST  and request.user.otherinfo.balance > 0:
            comment_media = request.POST.get('media_link', None)
            comment_media = 'https://www.instagram.com/' + comment_media.split('.com/')[1]
            comments = request.POST.get('comments', None)
            comment_media_id = None 
            comment_list = comments.splitlines()

            quantity = len(comment_list)
            if request.user.is_superuser == False:


                if request.user.is_superuser == False:

                    oi = get_object_or_404(OtherInfo,user=request.user)
                    if quantity > oi.balance:
                            quantity = oi.balance

                    oi.balance -= quantity
                    oi.save()
            sv = get_object_or_404(Services, category__category_name="Yorum")
            
            user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=comment_media,status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
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
                                t1 = threading.Thread(target=threadComment,args=(quantity,comment_list,comment_media,comment_media_id,user_order))
                                t1.start()
                                whileStatus = False


                    
                    time.sleep(5)


            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True

        context = {
            'title':'Send Post Comment',
            'starting':starting,
        }

        return render(request,'user/tools/send-postcomment.html',context)


def threadRunSavePost(us,auth_proxy,ip_port_proxy,x,quantity,total_quantity,order,user_media,errorFile,textUser):
    pass


def threadSavePost(quantity,user_order,photo_media):
    pass

@login_required(login_url='/login/')
def savePhotoView(request):

    if request.user.is_authenticated:
        starting = False

        if 'btnSend' in request.POST  and request.user.otherinfo.balance > 0:
            photo_media = request.POST.get('media_link', None)
            quantity = request.POST.get('quantity', None)

            if request.user.is_superuser == False:


                if request.user.is_superuser == False:
                    oi = get_object_or_404(OtherInfo,user=request.user)
                    if quantity > oi.balance:
                            quantity = oi.balance

                    oi.balance -= quantity
                    oi.save()
            sv = get_object_or_404(Services, category__category_name="Fotoğraf Kaydetme")

            user_order = Orders.objects.create(user=request.user,service=sv,charge=float(sv.rate),target=photo_media,status="Pending",user_order=True)

            def orderControl(user_order):
                whileStatus = True
                last_seo = SeoSettings.objects.all().last()
                while whileStatus:

                    user_order = get_object_or_404(Orders,id=user_order.id)
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
                                t1 = threading.Thread(target=threadSavePost,args=(quantity,user_order,photo_media))
                                t1.start()
                                whileStatus = False

                    time.sleep(5)
                

            t_o = threading.Thread(target=orderControl,args=(user_order,),daemon=True)
            t_o.start()
            print('order oluşturuldu.',user_order.status)
            starting = True



        context = {
            'title':'Photo Saving',
            'starting':starting,
        }

        return render(request,'user/tools/savephotos.html',context)


                
def threadRunLiveWatch(us,auth_proxy,ip_port_proxy,x,order,live_user,quantity,total_quantity,errorFile,textUser):
     pass

def threadLiveWatch(quantity,order,username):
    livewatchlog = {}
                    
    userCookies = InstagramCookies.objects.filter(active=True).order_by('?')

    total_quantity = quantity
    if len(userCookies) < quantity:
        total_quantity = len(userCookies)

    login_after_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_after_proxy=True)
    login_after_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_after_proxy=True)
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

    if total_quantity < 1 :
        order.status = "Partial"
        order.remains = int(quantity) - order.successful_value
        order.cancelled = True
        order.save()

    userSayac = 0
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
        livewatchlog[x] = threading.Thread(target=threadRunLiveWatch,args=(us,login_after_auth_proxy,login_after_ip_port_proxy,x,order,username,quantity,total_quantity,errorFile,us.user.username))
        livewatchlog[x].start()



@login_required(login_url='/login/')
def sendWatchLiveView(request):
    pass

def threadRunLiveLike(us,auth_proxy,ip_port_proxy,x,order,live_user,quantity,total_quantity,errorFile,textUser):
    pass
def threadLiveLike(quantity,user_order,username):
    pass

@login_required(login_url='/login/')
def sendLikeLiveView(request):
    pass
def threadRunLiveComment(us,login_after_auth_proxy,login_after_ip_port_proxy,x,comm,order,live_user,quantity,total_quantity,errorFile,textUser):
    pass

def threadLiveComment(quantity,comment_list,order,live_user):
    pass
@login_required(login_url='/login/')
def sendCommentLiveView(request):
    pass
def threadRunDMMessage(us,auth_proxy,ip_port_proxy,x,order,quantity,total_quantity,dm_user,comm,errorFile,textUser):
    pass

def threadDMMessage(quantity,comment_list,dm_user,order):
    dmmessagelog = {}   
    userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
    last_seo = SeoSettings.objects.all().last()

    total_quantity = quantity

    process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
    process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
    threads = []
    errorFile = open((BASE_DIR / 'static/userlogs/error_users_{}.txt'.format(binascii.hexlify(os.urandom(20)).decode())),'a')

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
        thread =  threading.Thread(target=threadRunDMMessage,args=(us,process_auth_proxy,process_ip_port_proxy,x,order,quantity,total_quantity,dm_user,comm,errorFile,us.user.username))
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
            order.remains = quantity - order.successful_value
            order.cancelled = True
            order.save()
            break

@login_required(login_url='/login/')
def sendDMMessageView(request):
    pass