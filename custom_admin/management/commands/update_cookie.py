import threading
from django.core.management.base import BaseCommand
from pathlib import Path
from core.get_path import outpath
from insta_scripts.serilog import Scanner
from custom_admin.models import Proxy,SeoSettings
BASE_DIR = Path(__file__).resolve().parent.parent
import random
import time


class Command(BaseCommand):
    def threadScanner(self,login_after_ip_port_proxy_list,login_after_auth_proxy_list,userid,authorization,claim,phoneid,waterfallid,guid,adid,deviceid,androidid,user_agent,pigeonid,mid,checksum,rur):
        
        login_after_ip_port_proxy = None
        login_after_auth_proxy = None

        if login_after_ip_port_proxy_list:

            login_after_ip_port_proxy = login_after_ip_port_proxy_list[random.randrange(len(login_after_ip_port_proxy_list))]
        if login_after_auth_proxy_list:

            login_after_auth_proxy = login_after_auth_proxy_list[random.randrange(len(login_after_auth_proxy_list))]  

        s = Scanner()
        s.startUserScanner(ip_port_proxy=login_after_ip_port_proxy,auth_proxy=login_after_auth_proxy,db_userid=userid,db_adid=adid,db_androidid=androidid,db_authorization=authorization,db_claim=claim,db_phoneid=phoneid,
        db_waterfallid=waterfallid,db_checksum=checksum,db_deviceid=deviceid,db_guid=guid,db_USER_AGENT=user_agent,db_pigeonid=pigeonid,db_mid=mid,db_rur=rur)

    
    def handle(self, *args, **kwargs):
        cookie_data = open(outpath() / 'user_cookies/cookies.txt','r',encoding='utf-8')

        login_after_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,login_after_proxy=True)
        login_after_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,login_after_proxy=True)
        sayac = 0
        data_split = cookie_data.read().splitlines()
        thDict = {}
        threads = []
        last_seo = SeoSettings.objects.all().last()                  

        for x in data_split:
            
            data_sp = x.split("::")

            userid = data_sp[0]
            authorization = data_sp[1]
            claim = data_sp[2]
            phoneid = data_sp[3]
            waterfallid = data_sp[4]
            guid = data_sp[5]
            adid = data_sp[6]
            deviceid = data_sp[7]
            androidid = data_sp[8]
            user_agent = data_sp[9]
            pigeonid = data_sp[10]
            mid = data_sp[11]
            checksum = data_sp[12]
            rur = data_sp[13]

            thDict[sayac] = threading.Thread(target=self.threadScanner,args=(login_after_ip_port_proxy_list,login_after_auth_proxy_list,
                userid,authorization,claim,phoneid,waterfallid,guid,adid,deviceid,androidid,user_agent,pigeonid,mid,checksum,rur))
            threads.append(thDict[sayac])
            thDict[sayac].start()

            if len(threads) >= last_seo.proxy_limit:
                for t in threads:
                    t:threading.Thread
                    t.join()
                    threads.clear()
