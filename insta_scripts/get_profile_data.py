import hashlib
import datetime
import time
import urllib
import uuid
import random
import requests
import urllib.parse
from datetime import datetime
import base64
import json

import base64
import time
from random import randint
import hmac
import hashlib

from custom_admin.models import Proxy

import urllib.parse


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent




class GetUserData:

    def __init__(self,user='',username='',password=''):

        self.username = username
        self.password = password
        self.BloksVersionId = 'e097ac2261d546784637b3df264aa3275cb6281d706d91484f43c207d6661931'
        self.deviceid = ''
        self.androidid = ''
        self.USER_AGENT = ''
        self.adid = ''
        self.claim = ''
        self.mid = ''
        self.rur = ''
        self.userid = ''
        self.instaUserId = ''
        self.authorization = ''
        self.guid = ''
        self.mykey = ''
        self.kullaniciuseridbul = user
        self.pigeonid = ''
        self.phoneid = ''
        self.API_URL = 'https://i.instagram.com/api/v1/'
        self.API_URL2 = 'https://b.i.instagram.com/api/v1/'
        self.API_URL3 = 'https://z-p42.i.instagram.com/api/v1/'
        self.PASL = ''
        self.itemList = []
        self.error_users = []
        self.success_users = []
        self.cookie_user_id = 0

        self.ip_port_proxy  = None
        self.auth_proxy = None
        self.root_proxy = None
        self.error_message = ''
        
    def set_proxy_ip_port(self,proxy):
        
      hostnamegel = proxy.split(":")[0]
      portgel = proxy.split(":")[1]

      proxy = hostnamegel + ":" + portgel


      proxyson = {'https': 'http://' + proxy}

      return proxyson


    def set_proxy_auth(self,proxy):
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


    def timestamp1(self, type):
        timeson114 = str(datetime.now().timestamp())  # str(int(datetime.now().timestamp()))
        
        if (type):
          return timeson114


    def timestamp2(self, type):
      timeson115 = str(int(datetime.now().timestamp()))
      if (type):
        return timeson115


    def timestamp3(self, type):
        timeson114 = datetime.now().timestamp()  # str(int(datetime.now().timestamp()))

        if (type):
            return timeson114




    def generateSignature(self, data, skip_quote=False):
        if not skip_quote:
            try:
                parsedData = urllib.parse.quote(data)
            except AttributeError:
                parsedData = urllib.quote(data)
        else:
            parsedData = data
        keysig = "signed_body=SIGNATURE.{}".format(parsedData)
        # print(keysig)
        return keysig

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        self.androidsade1 = m.hexdigest()[:16]
        self.androidsade = self.androidsade1
        return 'android-' + self.androidsade

    def generateUUID(self, type):
        generated_uuid = str(uuid.uuid4())

        if (type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    #user_agent = "Instagram 187.0.0.32.120 Android (28/9; 360dpi; 720x1422; HUAWEI; MRD-LX1; HWMRD-M1; mt6761; tr_TR; 289692181)"


    def user_agent_compile(self,agent):

        agent = agent.split(" ")

        outDict = {
            'device_type': str(agent[7]).replace(";", ""),
            'brand': str(agent[6]).replace(";", ""),
            'manufacturer': str(agent[6]).replace(";", ""),
            'os_type': str(agent[2]),
            'os_ver': str(agent[3]).replace(";", "").split("/")[-1],
        }

        return outDict

    def gen_user_breadcrumb(self,size):

        key = 'iN4$aGr0m'
        dt = int(time.time() * 1000)

        # typing time elapsed
        time_elapsed = randint(500, 1500) + size * randint(500, 1500)

        text_change_event_count = max(1, size / randint(3, 5))

        data = '{size!s} {elapsed!s} {count!s} {dt!s}'.format(**{
            'size': size, 'elapsed': time_elapsed, 'count': text_change_event_count, 'dt': dt
        })
        return {'a1': base64.b64encode(
            hmac.new(key.encode('ascii'), data.encode('ascii'), digestmod=hashlib.sha256).digest()),
                'a2': base64.b64encode(data.encode('ascii'))}

    def getdataStart(self,cookie_user_id,auth_proxy,ip_port_proxy,db_pigeonid,db_claim,db_deviceid,db_phoneid,db_androidid,db_USER_AGENT,db_checksum,db_authorization,db_mid,db_userid,db_rur,db_waterfallid,db_adid,db_guid,db_mykey):
        self.mediadbul = ""
        self.comments = ""

        self.db_pigeonid = db_pigeonid
        self.db_androidid = db_androidid
        self.db_claim = db_claim
        self.db_deviceid = db_deviceid
        self.db_mid = db_mid
        self.db_rur = db_rur
        self.db_USER_AGENT = db_USER_AGENT
        self.db_userid = db_userid
        self.db_phoneid = db_phoneid
        self.db_authorization = db_authorization
        self.db_checksum = db_checksum
        self.db_waterfallid = db_waterfallid
        self.db_guid = db_guid
        self.db_adid = db_adid
        self.db_mykey = db_mykey

        self.cookie_user_id = cookie_user_id.user.id

        if ip_port_proxy:
            self.root_proxy = self.set_proxy_ip_port(ip_port_proxy.proxy)

        elif auth_proxy:
            self.root_proxy = self.set_proxy_auth(auth_proxy.proxy)


        self.userid = self.db_userid
        self.deviceid = self.db_deviceid
        self.pigeonid = self.db_pigeonid
        self.adid = self.db_adid
        self.guid = self.db_guid
        self.phoneid = self.db_phoneid
        self.waterfall_id = self.db_waterfallid
        self.androidid = self.db_androidid
        self.checksum = self.db_checksum
        self.claim = self.db_claim
        self.session_id = self.generateUUID(True)
        self.authorization = self.db_authorization
        self.mid = self.db_mid
        self.USER_AGENT = self.db_USER_AGENT

        self.shbid = None
        self.shbts = None


        self.process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
        self.process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
        self.get_ip_port_proxy = ip_port_proxy
        self.get_auth_proxy = auth_proxy

        veriler = self.user_agent_compile(self.db_USER_AGENT)
        # print(veriler)

        self.deviceapp = veriler['device_type']
        #print(self.deviceapp)

        self.brandapp = veriler['brand']
        #print(self.brandapp)

        self.manufacturerapp = veriler['manufacturer']
        #print(self.manufacturerapp)

        self.os_typeapp = veriler['os_type']
        #print(self.os_typeapp)

        self.os_verapp = veriler['os_ver']
        #print(self.os_verapp)

        ##

        ### işlem başlangıç  ####

        if True:
            print("adim 1'e geldi...")
            self.useridbul()
            ## profil bilgileri getirme  ##
            print("f1")
            self.instaUserId= self.infouseridbul()
            print("f2")
            out = self.info_bilgi_1()
            self.lastMedia = out['last_media']

            print("itemsssssssssssssssssss",len(out['items']))
            if len(out['items']) < 12:
                  last_media_control = False                  
            
            for x in out['items']:
           
                  self.itemList.append(x)

            last_media_control = True
            while last_media_control:

              print("f3")
              out = self.info_bilgi_2()
              self.lastMedia = out['last_media']
              print(out)
              for x in out['items']:
                    self.itemList.append(x)

              if len(self.itemList) >= 15:
                last_media_control = False

            print("f4")

            return self.itemList


        #except Exception as e:
        #    self.error_users.append(self.cookie_user_id)
        #    return {'message':'Hata Tespit Edildi'}


    def changeProxy(self):
        if self.get_ip_port_proxy:
            if self.process_ip_port_proxy_list:
                process_ip_port_proxy = self.process_ip_port_proxy_list[random.randrange(len(self.process_ip_port_proxy_list))]

                self.root_proxy = self.set_proxy_ip_port(process_ip_port_proxy.proxy)

        elif self.get_auth_proxy:
            if self.process_auth_proxy_list:
        
                process_auth_proxy = self.process_auth_proxy_list[random.randrange(len(self.process_auth_proxy_list))]
                self.root_proxy = self.set_proxy_auth(process_auth_proxy.proxy)

    ## KULLANICI BİLGİLERİNİ GETİRME  ##

    def useridbul(self):

        if True:

            link1 = "users/" + self.kullaniciuseridbul + "/usernameinfo/?from_module=deep_link_util"

            self.SendRequestloginsonrasitoplu2get1a(link1)



        #except:
        #    self.changeProxy()
        #    self.useridbul()
        #    pass

        print("çıktı: ", self.json1)

        self.hesapidbul = str(int(self.json1['user']['pk']))
        # print(self.hesapidbul)

        return True



    def infouseridbul(self):


        try:

            link1 = "users/" + self.kullaniciuseridbul  + "/usernameinfo/?from_module=deep_link_util"


            self.SendRequestloginsonrasitoplu2get1a(link1)
        except:
            self.changeProxy()
            self.infouseridbul()
            pass
        print("çıktı0: ",self.json1)

        self.hesapidbul = str(int(self.json1['user']['pk']))

        return self.hesapidbul

    def info_bilgi_1(self):

        try:

            link2 = "feed/user/" + self.hesapidbul + "/?exclude_comment=true&only_fetch_first_carousel_media=false"

            self.SendRequestloginsonrasitoplu2get1a(link2)
        except:
            self.info_bilgi_1()
            pass
        print("çıktı1: ",len(self.json1['items']))

        self.medyaid = str(int(self.json1['items'][0]['pk']))
        print("aa: ", self.medyaid)

        #self.medyaurl = self.json1['items'][0]['image_versions2']['candidates'][0]['url']
        #print("bb: ", self.medyaurl)

        return {'last_media':self.medyaid,'items':self.json1['items']}

    def info_bilgi_2(self):

        try:

                            ### kullanıcı user id ##                          ## kullanıcı son post medya id ##   ### kullanıcı user id ##
            link2 = "feed/user/" + str(self.instaUserId) + "?exclude_comment=true&max_id=" + str(self.lastMedia) + "_" + str(self.instaUserId) + "&only_fetch_first_carousel_media=false"
            self.SendRequestloginsonrasitoplu2get1a(link2)
        except:
            self.info_bilgi_2()
        pass
        print("çıktı2: ",self.json1)

        self.medyaid = str(int(self.json1['items'][0]['pk']))
        print("aa: ", self.medyaid)

        #self.medyaurl = self.json1['items'][0]['carousel_media'][0]['image_versions2']['candidates'][0]['url']
        #print("bb: ", self.medyaurl)


        return {'last_media':self.medyaid,'items':self.json1['items']}




    ######### istek yapıları #########


    def SendRequestloginsonrasitoplu2get1a(self, endpoint):

        headers = {
            'X-IG-App-Locale': 'tr_TR',
            'X-IG-Device-Locale': 'tr_TR',
            'X-IG-Mapped-Locale': 'tr_TR',
            'X-Pigeon-Session-Id': self.pigeonid,
            'X-Pigeon-Rawclienttime': self.timestamp1(True),
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-Bloks-Version-Id': self.BloksVersionId,
            'X-IG-WWW-Claim': self.claim,
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            "x-ig-timezone-offset": "10800",
            "x-ig-connection-type": "MOBILE(HSPA)",
            "x-ig-capabilities": "3brTvx0\u003d",
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'X-MID': self.mid,
            'IG-U-SHBID': self.shbid,
            'IG-U-SHBTS': self.shbts,
            'IG-U-DS-USER-ID': self.userid,
            'IG-U-RUR': self.rur,
            'IG-INTENDED-USER-ID': self.userid,
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
        }
        response2 = requests.get('https://i.instagram.com/api/v1/' + endpoint, headers=headers, verify=True,
                                 proxies=self.root_proxy, timeout=15)  # proxies=proxy
        print("Status1a: ", response2.status_code)
        self.sonjson1a = response2.json()

        self.json1 = response2.json()

        self.json1 = response2.json()

        try:

            message = self.json1['message']
            self.error_message = message
        except:
            pass

        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            # print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            # print('shbts: ', self.shbts)
        except:
            self.shbid = None
            # print('shbid: ', self.shbid)

            self.shbts = None
            # print('shbts: ', self.shbts)

            pass



        self.rur = response2.headers['ig-set-ig-u-rur']

        return response2.status_code

    def SendRequestloginsonrasitoplu2post1a(self, endpoint, post=None):

        headers = {
            'X-IG-App-Locale': 'tr_TR',
            'X-IG-Device-Locale': 'tr_TR',
            'X-IG-Mapped-Locale': 'tr_TR',
            'X-Pigeon-Session-Id': self.pigeonid,
            'X-Pigeon-Rawclienttime': self.timestamp1(True),
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-IG-App-Startup-Country': 'TR',
            'X-Bloks-Version-Id': self.BloksVersionId,
            'X-IG-WWW-Claim': self.claim,
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            "x-ig-timezone-offset": "10800",
            "x-ig-connection-type": "MOBILE(HSPA)",
            "x-ig-capabilities": "3brTvx0\u003d",
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'IG-U-SHBID': self.shbid,
            'IG-U-SHBTS': self.shbts,
            'X-MID': self.mid,
            'IG-U-DS-USER-ID': self.userid,
            'IG-U-RUR': self.rur,
            'IG-INTENDED-USER-ID': self.userid,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
            'Content-Length': str(int(len(post)))
        }
        response2 = requests.post('https://i.instagram.com/api/v1/' + endpoint, headers=headers, data=post,
                                  verify=True, proxies=self.root_proxy, timeout=15)  # proxies=proxy
        print("Status1b: ", response2.status_code)

        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            # print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            # print('shbts: ', self.shbts)
        except:
            self.shbid = None
            # print('shbid: ', self.shbid)

            self.shbts = None
            # print('shbts: ', self.shbts)

            pass

        self.sonjson1 = response2.json()

        self.json1 = response2.json()

        try:

            message = self.json1['message']
            self.error_message = message

        except:
            pass

        print("Status1a: ", response2.content)
        self.rur = response2.headers['ig-set-ig-u-rur']

        return True


    def SendRequestloginsonrasitoplu2post2a(self, endpoint, post=None):

        headers = {
            'X-IG-App-Locale': 'tr_TR',
            'X-IG-Device-Locale': 'tr_TR',
            'X-IG-Mapped-Locale': 'tr_TR',
            'X-Pigeon-Session-Id': self.pigeonid,
            'X-Pigeon-Rawclienttime': self.timestamp1(True),
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-IG-App-Startup-Country': 'TR',
            'X-Bloks-Version-Id': self.BloksVersionId,
            'X-IG-WWW-Claim': self.claim,
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            "x-ig-timezone-offset": "10800",
            "x-ig-connection-type": "MOBILE(HSPA)",
            "x-ig-capabilities": "3brTvx0\u003d",
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'IG-U-SHBID': self.shbid,
            'IG-U-SHBTS': self.shbts,
            'X-MID': self.mid,
            'IG-U-DS-USER-ID': self.userid,
            'IG-U-RUR': self.rur,
            'IG-INTENDED-USER-ID': self.userid,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
            'Content-Length': str(int(len(post)))
        }
        response2 = requests.post('https://i.instagram.com/api/v1/' + endpoint, headers=headers, data=post,
                                  verify=True, proxies=self.root_proxy, timeout=15)  # proxies=proxy
        print("Status1c: ", response2.status_code)



        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            # print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            # print('shbts: ', self.shbts)
        except:
            self.shbid = None
            # print('shbid: ', self.shbid)

            self.shbts = None
            # print('shbts: ', self.shbts)

            pass

        self.sonjson1 = response2.json()

        self.json1 = response2.json()

        try:

            message = self.json1['message']
            self.error_message = message
        except:
            pass

        print("Status1a: ", response2.content)
        self.rur = response2.headers['ig-set-ig-u-rur']

        return True



