import hashlib
import datetime
import time
import urllib
import uuid
import requests
import json
import urllib.parse
from datetime import datetime
import base64
import json
import random
import base64
import time
from random import randint
import hmac
import hashlib

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

from custom_admin.models import Proxy

class LiveComment:

    def __init__(self,username='',password='',live_user=''):

        self.username = username
        self.password = password
        self.kullaniciuseridbul = live_user
        self.BloksVersionId = 'e097ac2261d546784637b3df264aa3275cb6281d706d91484f43c207d6661931'
        self.deviceid = ''
        self.userid = ''
        self.claim = ''
        self.authorization = ''
        self.checksum = ''
        self.androidid = ''
        self.USER_AGENT = ''
        self.adid = ''
        self.guid = ''
        self.mykey = ''
        self.pigeonid = ''
        self.phoneid = ''
        self.API_URL = 'https://i.instagram.com/api/v1/'
        self.API_URL2 = 'https://b.i.instagram.com/api/v1/'
        self.API_URL3 = 'https://z-p42.i.instagram.com/api/v1/'
        self.PASL = ''
        self.live_comment_count = 0
        self.error_users = []
        self.success_users = []
        self.cookie_user_id = 0
        self.ip_port_proxy  = None
        self.auth_proxy = None
        self.root_proxy = None
        self.error_message = ''

    def timestamp1(self, type):
        timeson114 = str(datetime.now().timestamp())  # str(int(datetime.now().timestamp()))
        
        if (type):
          return timeson114


    def timestamp2(self, type):
      timeson115 = str(int(datetime.now().timestamp()))
      if (type):
        return timeson115


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

    def liveCommentStart(self,comment,cookie_user_id,ip_port_proxy,auth_proxy,db_pigeonid,db_claim,db_deviceid,db_phoneid,db_androidid,db_USER_AGENT,db_checksum,db_authorization,db_mid,db_userid,db_rur,db_waterfallid,db_adid,db_guid,db_mykey):
        self.livecomments = comment

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
        self.ip_port_proxy = None
        self.auth_proxy = None


        self.appver = '212.0.0.38.119'


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
        liveCommentStatus = False
        try:
            ## canlı yayın like ##
            print("f0")
            self.useridbul()
            print("f1")
            self.liveid1()
            print("f2")
            status_comment = self.livecomments1()
            if str(status_comment) == "200":
                  self.live_comment_count +=1
                  liveCommentStatus = True
            print("f3")
            self.success_users.append(self.cookie_user_id)

        except Exception as e:
            self.error_users.append(self.cookie_user_id)
            print(e)
            return False

        return {'status':liveCommentStatus,'message':self.error_message}
    ##### canlı yayın işlemleri  ########

    def changeProxy(self):
        if self.get_ip_port_proxy:
            if self.process_ip_port_proxy_list:
                process_ip_port_proxy = self.process_ip_port_proxy_list[random.randrange(len(self.process_ip_port_proxy_list))]

                self.root_proxy = self.set_proxy_ip_port(process_ip_port_proxy.proxy)

        elif self.get_auth_proxy:
            if self.process_auth_proxy_list:
        
                process_auth_proxy = self.process_auth_proxy_list[random.randrange(len(self.process_auth_proxy_list))]
                self.root_proxy = self.set_proxy_auth(process_auth_proxy.proxy)

    ##### canlı yayın yorum ###

    def useridbul(self):

        try:

            link1 = "users/" + self.kullaniciuseridbul + "/usernameinfo/?from_module=deep_link_util"

            self.SendRequestloginsonrasitoplu2get(link1)

        except:
            self.useridbul()
            pass


        # print("çıktı: ",self.json1)

        self.hesapidbul = str(int(self.json1['user']['pk']))
        # print(self.hesapidbul)

        return True

    def liveid1(self):

        try:

            link = 'feed/user/' + self.hesapidbul + '/story/?supported_capabilities_new=%5B%7B%22name%22%3A%22SUPPORTED_SDK_VERSIONS%22%2C%22value%22%3A%2273.0%2C74.0%2C75.0%2C76.0%2C77.0%2C78.0%2C79.0%2C80.0%2C81.0%2C82.0%2C83.0%2C84.0%2C85.0%2C86.0%2C87.0%2C88.0%2C89.0%2C90.0%2C91.0%2C92.0%2C93.0%2C94.0%2C95.0%2C96.0%2C97.0%2C98.0%2C99.0%2C100.0%2C101.0%2C102.0%2C103.0%2C104.0%2C105.0%2C106.0%22%7D%2C%7B%22name%22%3A%22FACE_TRACKER_VERSION%22%2C%22value%22%3A%2214%22%7D%2C%7B%22name%22%3A%22COMPRESSION%22%2C%22value%22%3A%22ETC2_COMPRESSION%22%7D%2C%7B%22name%22%3A%22world_tracker%22%2C%22value%22%3A%22world_tracker_enabled%22%7D%2C%7B%22name%22%3A%22gyroscope%22%2C%22value%22%3A%22gyroscope_enabled%22%7D%5D'

            self.SendRequestloginsonrasitoplu2get(link)


        except:
            self.liveid1()
            pass

        # print("çıktı: ", self.json1)

        self.liveid = str(self.json1["broadcast"]["id"])
        print("liveid: ", self.liveid)

        return True

    def livecomments1(self):

        try:

            sss = self.gen_user_breadcrumb(len(self.livecomments))

            b1 = sss['a1'].decode('UTF-8')
            # print(b1)

            c1 = sss['a2'].decode('UTF-8')
            # print(c1)

            aa = b1 + "\n" + c1 + "\n"

            alfason = {
                "user_breadcrumb": aa,
                "live_or_vod": "1",
                "idempotence_token": self.generateUUID(True),
                "_uid": self.db_userid,
                "_uuid": self.db_guid,
                "force_create": "false",
                "comment_text": self.livecomments,
                "offset_to_video_start": "200"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            link = "live/" + self.liveid + "/comment/"

            status_code = self.SendRequestloginsonrasitoplu2post(link, signature18)


        except:
            self.changeProxy()
            self.livecomments1()
            pass


        # print("çıktı: ", self.json1)

        return status_code


    ######### istek yapıları #########

    def SendRequestloginsonrasitoplu2get(self, endpoint):

        headers = {
                'X-IG-App-Locale': 'tr_TR',
                'X-IG-Device-Locale': 'tr_TR',
                'X-IG-Mapped-Locale': 'tr_TR',
                'X-Pigeon-Session-Id': self.db_pigeonid,
                'X-Pigeon-Rawclienttime': self.timestamp1(True),
                'X-IG-Bandwidth-Speed-KBPS': '-1.000',
                'X-IG-Bandwidth-TotalBytes-B': '0',
                'X-IG-Bandwidth-TotalTime-MS': '0',
                'X-Bloks-Version-Id': self.BloksVersionId,
                'X-IG-WWW-Claim': self.db_claim,
                'X-Bloks-Is-Layout-RTL': 'false',
                'X-Bloks-Is-Panorama-Enabled': 'true',
                'X-IG-Device-ID': self.db_deviceid,
                'X-IG-Family-Device-ID': self.db_phoneid,
                'X-IG-Android-ID': self.db_androidid,
                'X-IG-Timezone-Offset': '3600',
                'X-IG-Connection-Type': 'MOBILE(LTE)',
                'X-IG-Capabilities':'3brTvx0=',
                'X-IG-App-ID': '567067343352427',
                'User-Agent': self.db_USER_AGENT,
                'Accept-Language': 'tr-TR, en-US',
                'Authorization': self.db_authorization,
                'X-MID': self.db_mid,
                'IG-U-DS-USER-ID': self.db_userid,
                'IG-U-RUR': self.db_rur,
                'IG-INTENDED-USER-ID': self.db_userid,
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'Connection': 'keep-alive',
                }
        response2 = requests.get('https://i.instagram.com/api/v1/' + endpoint,headers = headers,proxies=self.root_proxy,verify=True, timeout=15)
        print("Status1: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']
        self.json1 = response2.json()

        self.json1 = response2.json()

        try:

            message = self.json1['message']
            self.error_message = message
        except:
            pass

        #print("rur: ", self.rur)
        #print("Status1: ", response2.content)


        return True

    def SendRequestloginsonrasitoplu2post(self, endpoint, post=None):

        headers = {
            'X-IG-App-Locale': 'tr_TR',
            'X-IG-Device-Locale': 'tr_TR',
            'X-IG-Mapped-Locale': 'tr_TR',
            'X-Pigeon-Session-Id': self.db_pigeonid,
            'X-Pigeon-Rawclienttime': self.timestamp1(True),
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-IG-App-Startup-Country': 'TR',
            'X-Bloks-Version-Id': self.BloksVersionId,
            'X-IG-WWW-Claim': self.db_claim,
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.db_deviceid,
            'X-IG-Family-Device-ID': self.db_phoneid,
            'X-IG-Android-ID': self.db_androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.db_USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.db_authorization,
            'X-MID': self.db_mid,
            'IG-U-DS-USER-ID': self.db_userid,
            'IG-U-RUR': self.db_rur,
            'IG-INTENDED-USER-ID': self.db_userid,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
        }
        #headers['Content-Length'] = '779'
        response2 = requests.post('https://i.instagram.com/api/v1/' + endpoint, headers = headers,data=post,proxies=self.root_proxy,verify=True, timeout=15)
        print("Status1: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']
        self.json1 = response2.json()

        try:

            message = self.json1['message']
            self.error_message = message    
        except:
            pass


        return response2.status_code


    ################
