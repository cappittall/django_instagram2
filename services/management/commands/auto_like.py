from time import time
from custom_admin.views import threadLike, threadRunLike
from user.models import OtherInfo
from django.core.management.base import BaseCommand
import requests
from services.models import HostKeys
from django.conf import settings as conf_settings

import threading
from insta_scripts.auto_like import Like
from insta_scripts.get_profile_data import GetUserData
from user.models import InstagramCookies
from custom_admin.models import SeoSettings,Proxy,AutoLikeUser,AutoLikeUserLog,AutoLikeQueue
import random
import time
from datetime import datetime, timezone
from django.utils.timezone import localtime
from services.models import ServicesSuccessfulLog
class Command(BaseCommand):



    def threadRunLike(self,auth_proxy,ip_port_proxy,like_media,media_id,queueControl,total_quantity):
        
        l = Like(user_media=like_media,media_id=media_id)
        successControl = True
        exceptValue = 0
        while successControl and exceptValue < 10:
            us = random.choice(InstagramCookies.objects.filter(active=True).order_by('?'))
            try:

                if ( int(time.time()) - us.last_process_time ) < 10:
                    print('user 10 saniye uykuya alindi arından isleme devam edecek...')
                    time.sleep(10)

                us.last_process_time = int(time.time()) + 3
                us.save()

                statusLike = l.likeStart(cookie_user_id=us,auth_proxy=auth_proxy,ip_port_proxy=ip_port_proxy,db_androidid=us.androidid, db_authorization=us.authorization, db_claim=us.claim, db_deviceid=us.deviceid,
                        db_mid=us.mid, db_phoneid=us.phoneid, db_pigeonid=us.pigeonid, db_rur=us.rur, db_USER_AGENT=us.user_agent,
                        db_userid=us.userid, db_checksum=us.checksum,db_waterfallid=us.waterfallid,db_adid=us.adid,db_guid=us.guid,db_mykey=us.key)


                if statusLike['status'] == False:
                
                    try:

                        message = statusLike['message']

                        if message == 'feedback_required':
                            print('feedback_required geldi... pasif olmali',us.user,us.id)
                            us.feedback = True
                            us.active = False

                        elif message == 'challenge_required':
                            print('challenge_required geldi... pasif olmali',us.user,us.id)

                            us.challenge = True
                            us.active = False

                        elif message == 'checkpoint_required':
                            print('checkpoint_required geldi... pasif olmali',us.user,us.id)

                            us.checkpoint = True
                            us.active = False

                        elif message == 'login_required':
                            print('login_required geldi... pasif olmali',us.user,us.id)
                            us.login_required = True
                            us.active = False
                    except:
                        pass
                    us.error_count +=1
                    us.save()

                else:
                    queueControl.successful_value +=1
                    successControl = False
                    us.error_count = 0
                    us.save()
                    queueControl.save()
            except:
                exceptValue += 1
                time.sleep(10)

                print('db hatası')

            if queueControl.successful_value == total_quantity:
                queueControl.success = True
                queueControl.save()



    def threadLike(self,quantity,user_media,user_media_id,queueControl):
        userlikelog = {}
        userCookies = InstagramCookies.objects.filter(active=True).order_by('?')
        last_seo = SeoSettings.objects.all().last()                  

        total_quantity = quantity
        if len(userCookies) < quantity:
            total_quantity = len(userCookies)    

        process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,auto_process_proxy=True)
        process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,auto_process_proxy=True)
        threads = []
        for x in range(0, total_quantity):
            process_ip_port_proxy = None
            process_auth_proxy = None

            if process_ip_port_proxy_list:

                process_ip_port_proxy = process_ip_port_proxy_list[random.randrange(len(process_ip_port_proxy_list))]
            if process_auth_proxy_list:

                process_auth_proxy = process_auth_proxy_list[random.randrange(len(process_auth_proxy_list))]

            thread =  threading.Thread(target=self.threadRunLike,args=(process_auth_proxy,process_ip_port_proxy,user_media,user_media_id,queueControl,total_quantity))
            userlikelog[x] = thread
            userlikelog[x].start()

            threads.append(thread)

            if len(threads) >= last_seo.proxy_limit:
                for t in threads:
                    t:threading.Thread
                    t.join() 
                    threads.clear()


    def handle(self, *args, **kwargs):
        queueControl = AutoLikeQueue.objects.filter(success=False).last()
        if queueControl:
            print('işlemler devam etmekte bu task askıya alındı...')
        else:

            auto_like = AutoLikeUser.objects.all()

            for auto_user in auto_like:
                control_date = datetime.now(timezone.utc) - auto_user.date
                print(control_date)
                if int(control_date.days) <= auto_user.timeout:
                    print('başladı')
                    startObject = GetUserData(user=auto_user.username)
                    auto_user_log  = AutoLikeUserLog.objects.filter(auto_like_user=auto_user)
                    oii = random.choice(InstagramCookies.objects.all())
                    login_after_ip_port_proxy = None
                    login_after_auth_proxy = None

                    login_after_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_after_proxy=True)
                    login_after_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_after_proxy=True)

                    if login_after_ip_port_proxy_list:

                        login_after_ip_port_proxy = login_after_ip_port_proxy_list[random.randrange(len(login_after_ip_port_proxy_list))]
                    if login_after_auth_proxy_list:

                        login_after_auth_proxy = login_after_auth_proxy_list[random.randrange(len(login_after_auth_proxy_list))]
                    print('data cagirma basladi')
                    items = startObject.getdataStart(cookie_user_id=oii,ip_port_proxy=login_after_ip_port_proxy,auth_proxy=login_after_auth_proxy,db_androidid=oii.androidid,db_authorization=oii.authorization,db_claim=oii.claim,db_deviceid=oii.deviceid,
                                        db_mid=oii.mid,db_phoneid=oii.phoneid,db_pigeonid=oii.pigeonid,db_rur=oii.rur,db_USER_AGENT=oii.user_agent,
                                        db_userid=oii.userid,db_checksum=oii.checksum,db_waterfallid=oii.waterfallid,db_adid=oii.adid,db_guid=oii.guid,db_mykey=oii.key)
                    print('items : ',items)
                    media_id_list = []
                    for item in items[0:12]:
                        try:
                            
                            p_id = item['pk']
                            print("media id:",p_id)
                            okControl = True

                            for x in media_id_list:
                                if x == p_id:
                                    okControl = False
                                    break
                            
                            if okControl:
                                media_id_list.append(str(p_id))
                         
                            if len(media_id_list) == 12:
                                break
                        except Exception as e:
                            print(e)
                    
                    use_media = []
                    for x in media_id_list:
                        
                        if auto_user_log.filter(media_id=str(x)):
                            pass
                        else:
                            AutoLikeUserLog.objects.create(media_id=x,auto_like_user=auto_user)
                            use_media.append(x)
                    
                    for m in use_media:
                        
                        ql = AutoLikeQueue.objects.create(auto_like_user=auto_user,media_id=m)

                        turnWhile = True
                        while turnWhile:
                            queueControl = AutoLikeQueue.objects.filter(success=False).last()
                            if queueControl.id == ql.id:

                                user_media = None
                                media_id = m
                                t = threading.Thread(target=self.threadLike,args=(auto_user.quantity,user_media,media_id,queueControl))
                                t.start()
                                print('burada 1.')
                                get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id="Oto Beğeni").last()
                                
                                if get_this_service_log:
                                    get_this_service_log.successful_value += int(auto_user.quantity)
                                    get_this_service_log.save()
                                else:
                                    ServicesSuccessfulLog.objects.create(service_id="Oto Beğeni",service_name="Oto Beğeni",successful_value=int(auto_user.quantity))

                                turnWhile = False
                                break
                            print('burada...')
                            time.sleep(15)
                
                else:
                    print('bir emirin süresi doldu.')
                    auto_user.delete()