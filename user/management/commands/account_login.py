from django.contrib.auth.models import User
from user.models import InstagramCookies,OtherInfo
from django.core.management.base import BaseCommand
from insta_scripts.insta_login import Login
from custom_admin.models import Proxy
import random
import threading
from django.shortcuts import get_object_or_404
from services.models import CountryCodes

class Command(BaseCommand):
    def threadRun(self,insta_login,other_info_i):
        
        insta_login.loginLaterThread()
        other_info_i.checksum = insta_login.checksum
        other_info_i.rur = insta_login.rur
        other_info_i.key = insta_login.mykey
        other_info_i.save()

    def try4login(self,user_oi):
        success_count = 0
        for x in range(0,1):
            print(x)
            login_error = False

            try:

                login_after_ip_port_proxy = None
                login_after_auth_proxy = None
                login_ip_port_proxy = None
                login_auth_proxy = None


                login_after_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_after_proxy=True)
                login_after_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_after_proxy=True)
                login_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_proxy=True)
                login_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_proxy=True)

                if login_after_ip_port_proxy_list:

                    login_after_ip_port_proxy = login_after_ip_port_proxy_list[random.randrange(len(login_after_ip_port_proxy_list))]

                if login_after_auth_proxy_list:

                    login_after_auth_proxy = login_after_auth_proxy_list[random.randrange(len(login_after_auth_proxy_list))]
                    
                if login_ip_port_proxy_list:

                    login_ip_port_proxy = login_ip_port_proxy_list[random.randrange(len(login_ip_port_proxy_list))]
                if login_auth_proxy_list:

                    login_auth_proxy = login_auth_proxy_list[random.randrange(len(login_auth_proxy_list))]

                insta_login = Login(username=user_oi.user.username,password=user_oi.default_password)
                output = insta_login.loginStart(login_after_auth_proxy=login_after_auth_proxy,login_after_ip_port_proxy=login_after_ip_port_proxy,login_ip_port_proxy=login_ip_port_proxy,login_auth_proxy=login_auth_proxy)

            except:
                login_error = True
                print('hata oluştu.')

            
            if login_error == False:

                try:
                    if output['login_error'] == False and output['status_code'] == 200:
                        success_count +=1

                        user = get_object_or_404(User,username=user_oi.user.username)
                        
                        other_info_i = get_object_or_404(InstagramCookies,user=user)
                        other_info = get_object_or_404(OtherInfo,user=user)
                        other_info_i.userid = output['userid']
                        other_info_i.authorization = output['authorization']
                        other_info_i.claim = output['claim']
                        other_info_i.phoneid = output['phoneid']
                        other_info_i.waterfallid = output['waterfallid']
                        other_info_i.guid = output['guid']
                        other_info_i.adid = output['adid']                        
                        other_info_i.deviceid = output['deviceid']
                        other_info_i.androidid = output['androidid']
                        other_info_i.user_agent = output['user_agent']
                        other_info_i.checksum = output['checksum']
                        other_info_i.pigeonid = output['pigeonid']
                        other_info_i.rur = output['rur']
                        other_info_i.mid = output['mid']
                    

                        pic_url = "https://togetherearn.com/fr/v/" + str(output['status5']['logged_in_user']['profile_pic_url'].split('/v')[1])

                        other_info.picture_url = pic_url
                        other_info_i.error_count = 0 
                        other_info.save()
                        other_info_i.save()

                        if output['user_data']['ulke_kodu']:
                            countryControl = CountryCodes.objects.filter(name=output['user_data']['ulke_kodu'])
                            if len(countryControl) == 0:
                                CountryCodes.objects.create(name=output['user_data']['ulke_kodu']) 

                        other_info.gender = output['user_data']['cinsiyet']
                        other_info.phone = output['user_data']['phone_number']
                        other_info.country_code = output['user_data']['ulke_kodu']
                        user.email = output['user_data']['email']
                        other_info.save()
                        user.save()


                        t1 = threading.Thread(target=self.threadRun,args=(insta_login,user_oi))
                        t1.start()
                        break
                
                except:
                    print('giriş başarısız : ',user_oi.user.username)
        if success_count >= 0:

            user_oi.error_count = 0
            user_oi.active = True
            user_oi.save()

        else:
            
            user_oi.active = False
            user_oi.save()
            print("hesap deaktif edildi : ",user_oi.user.username)              


    def handle(self, *args, **kwargs):

        error_users = InstagramCookies.objects.filter(active=True,error_count=4)
        for user_oi in error_users:
            print("kontrol sağlanıyor... : ",user_oi.user.username)

            t = threading.Thread(target=self.try4login,args=(user_oi,),daemon=False)
            t.start()



