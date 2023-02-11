from time import time

from django.core.management.base import BaseCommand


import threading
from insta_scripts.auto_follow_analiz import AutoFollowAnaliz
from insta_scripts.follow import Follow
from user.models import InstagramCookies
from custom_admin.models import SeoSettings,Proxy,AutoFollowUser,AutoFollowUserLog,AutoFollowQueue
import random
import time
from core.get_path import outpath
import binascii,os
from services.models import ServicesSuccessfulLog

BASE_DIR = outpath()

class Command(BaseCommand):



    def multiRunFollow(self,us,auth_proxy,ip_port_proxy,x,quantity,total_quantity,follow_user,errorFile,textUser,queueControl):
        

        f = Follow(follow_user=follow_user)
        try:

            if ( int(time.time()) - us.last_process_time ) < 10:
                print('user 10 saniye uykuya alindi arından isleme devam edecek...')
                time.sleep(10)

            us.last_process_time = int(time.time()) + 3
            us.save()

            followStatus = f.followStart(cookie_user_id=us,auth_proxy=auth_proxy,ip_port_proxy=ip_port_proxy,db_androidid=us.androidid, db_authorization=us.authorization, db_claim=us.claim, db_deviceid=us.deviceid,
                                    db_mid=us.mid, db_phoneid=us.phoneid, db_pigeonid=us.pigeonid, db_rur=us.rur, db_USER_AGENT=us.user_agent,
                                    db_userid=us.userid, db_checksum=us.checksum,db_waterfallid=us.waterfallid,db_adid=us.adid,db_guid=us.guid,db_mykey=us.key)
                            
            if followStatus['status'] == False:
            
                try:

                    message = followStatus['message']
                    print('message')
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
                except Exception as e:
                    print('hata : ',e)
                us.error_count +=1
                us.save()
                errorFile.write(textUser+'\n')


            if x == 0:
                print("follow_count_after : ",f.follow_count_after)
        except:
            print('db hatası')
        
        if x + 1 == total_quantity:
            queueControl.success = True
            queueControl.save()



        if total_quantity == x + 1:

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


    def threadFollow(self,quantity,follow_user,queueControl):
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
            thread =  threading.Thread(target=self.multiRunFollow,args=(us,process_auth_proxy,process_ip_port_proxy,x,quantity,total_quantity,follow_user,errorFile,us.user.username,queueControl))
            followislemlog[x] = thread
            followislemlog[x].start()

            threads.append(thread)
            
            if len(threads) >= last_seo.proxy_limit:
                for t in threads:
                    t:threading.Thread
                    t.join() 
                    threads.clear()


    def handle(self, *args, **kwargs):
        queueControl = AutoFollowQueue.objects.filter(success=False).last()
        if queueControl:
            print('işlemler devam etmekte bu task askıya alındı...')
        else:

            auto_follow = AutoFollowUser.objects.all()

            for auto_user in auto_follow:
                
                listControl = True
                controlValue = 0
                while listControl and controlValue < 50:
                    controlValue += 1
                    print(auto_user.username)
                    startObject = AutoFollowAnaliz(getusername=auto_user.username)
                    auto_user_log  = AutoFollowUserLog.objects.filter(auto_follow_user=auto_user)
                    oii = random.choice(InstagramCookies.objects.all())
                    login_after_ip_port_proxy = None
                    login_after_auth_proxy = None

                    login_after_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_after_proxy=True)
                    login_after_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_after_proxy=True)

                    if login_after_ip_port_proxy_list:

                        login_after_ip_port_proxy = login_after_ip_port_proxy_list[random.randrange(len(login_after_ip_port_proxy_list))]
                    
                    if login_after_auth_proxy_list:

                        login_after_auth_proxy = login_after_auth_proxy_list[random.randrange(len(login_after_auth_proxy_list))]

                    users_list = startObject.autoFollowAnalizStart(cookie_user_id=oii,ip_port_proxy=login_after_ip_port_proxy,auth_proxy=login_after_auth_proxy,db_androidid=oii.androidid,db_authorization=oii.authorization,db_claim=oii.claim,db_deviceid=oii.deviceid,
                                        db_mid=oii.mid,db_phoneid=oii.phoneid,db_pigeonid=oii.pigeonid,db_rur=oii.rur,db_USER_AGENT=oii.user_agent,
                                        db_userid=oii.userid,db_checksum=oii.checksum,db_waterfallid=oii.waterfallid,db_adid=oii.adid,db_guid=oii.guid,db_mykey=oii.key)
                    print(users_list)
                    if users_list:

                        listControl = False

                        use_ = []
                        for x in users_list:
                            
                            if auto_user_log.filter(user_id=str(x['pk'])):
                                pass
                            else:
                                AutoFollowUserLog.objects.create(user_id=x['pk'],username=x['username'],auto_follow_user=auto_user)
                                use_.append(x)
                        print("use kontrol : ",use_)
                        
                        for m in use_:
                            
                            ql = AutoFollowQueue.objects.create(auto_follow_user=auto_user,target_user=m['username'])

                            turnWhile = True
                            while turnWhile:
                                queueControl = AutoFollowQueue.objects.filter(success=False).last()
                                if queueControl.id == ql.id:

                                    t = threading.Thread(target=self.threadFollow,args=(auto_user.quantity,m['username'],queueControl))
                                    t.start()

                                    get_this_service_log = ServicesSuccessfulLog.objects.filter(service_id="Oto Takipçi").last()
                                    
                                    if get_this_service_log:
                                        get_this_service_log.successful_value += int(auto_user.quantity)
                                        get_this_service_log.save()
                                    else:
                                        ServicesSuccessfulLog.objects.create(service_id="Oto Takipçi",service_name="Oto Takipçi",successful_value=int(auto_user.quantity))


                                    turnWhile = False
                                    break
                                
                                time.sleep(15)
                                print('sıra bekleniyor...')
                    else:
                        pass
                
                else:
                    print('bir denetleme tamamlandı')