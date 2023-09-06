import hashlib
import datetime
import urllib
import uuid
import random
import requests
import json
import urllib.parse
from datetime import datetime
import json

import urllib.parse

from custom_admin.models import Proxy


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent




class SavePost:

    def __init__(self,user_media=None,media_id=None):

        self.username = ''
        self.password = ''
        self.userMedia = user_media
        self.media_id = media_id
        self.BloksVersionId = 'e097ac2261d546784637b3df264aa3275cb6281d706d91484f43c207d6661931'
        self.deviceid = ''
        self.userid = ''
        self.claim = ''
        self.authorization = ''
        self.mykey = ''
        self.checksum = ''
        self.androidid = ''
        self.USER_AGENT = ''
        self.adid = ''
        self.guid = ''
        self.likeCount = 0
        self.pigeonid = ''
        self.phoneid = ''
        self.API_URL = 'https://i.instagram.com/api/v1/'
        self.API_URL2 = 'https://b.i.instagram.com/api/v1/'
        self.API_URL3 = 'https://z-p42.i.instagram.com/api/v1/'
        self.PASL = ''

        self.save_post_count = 0
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

    # print(user_agent_compile(user_agent))




    def savePostStart(self,cookie_user_id,auth_proxy,ip_port_proxy,db_pigeonid,db_claim,db_deviceid,db_phoneid,db_androidid,db_USER_AGENT,db_checksum,db_authorization,db_mid,db_userid,db_rur,db_waterfallid,db_adid,db_guid,db_mykey):

        if self.userMedia:
              
            if self.userMedia.find('https://') != -1 or self.userMedia.find('http://') != -1:
                self.mediadbul = self.userMedia
                print('http bulundu')
            else:
                print('http bulunamadı eklendi...')
                self.mediadbul = 'https://' + self.userMedia
                print('http bulunamadı eklendi...')

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
        self.rur = self.db_rur
        self.shbid = None
        self.shbts = None

        self.process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
        self.process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
        self.get_ip_port_proxy = ip_port_proxy
        self.get_auth_proxy = auth_proxy

        veriler = self.user_agent_compile(self.USER_AGENT)
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

        savePhotoStatus = False
        try:

            ### fotoğraf kaydetme  ####
            print("j1")
            self.kaydetbul()
            print("j2")
            status_code = self.kaydet1()
            if status_code == 'ok':
                self.save_post_count +=1
                savePhotoStatus = True
            print("j3")
            self.success_users.append(self.cookie_user_id)

        except Exception as e:
            self.error_users.append(self.cookie_user_id)
            print(e)

        return {'status':savePhotoStatus,'message':self.error_message}

    def changeProxy(self):
        if self.get_ip_port_proxy:
            if self.process_ip_port_proxy_list:
                process_ip_port_proxy = self.process_ip_port_proxy_list[random.randrange(len(self.process_ip_port_proxy_list))]

                self.root_proxy = self.set_proxy_ip_port(process_ip_port_proxy.proxy)

        elif self.get_auth_proxy:
            if self.process_auth_proxy_list:
        
                process_auth_proxy = self.process_auth_proxy_list[random.randrange(len(self.process_auth_proxy_list))]
                self.root_proxy = self.set_proxy_auth(process_auth_proxy.proxy)

    def kaydetbul(self):

        try:
    

            link1 = self.mediadbul + "?utm_medium=copy_link"

            ddd80 = urllib.parse.quote(link1)
            #print("aaaaa", ddd80)

            link2 = "oembed/?url=" + ddd80


            self.SendRequestloginsonrasitoplu2get1a(link2)

        except:
            self.changeProxy()
            self.kaydetbul()
            pass

        #print("çıktı: ",self.json1)

        self.media_id = str(self.json1['media_id'])
        print("media_id: ", self.media_id)


        return True



    def kaydet1(self):

        try:
    
            alfason = {
                      "module_name": "feed_contextual_profile",
                      "radio_type": "wifi-none",
                      "_uid": self.db_userid,
                      "_uuid": self.db_guid
                    }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            #print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}&d=0".format(ddd80)
            #print(signature18)

            link = "media/" + self.media_id + "/save/"

            self.SendRequestloginsonrasitoplu2post1a(link,signature18)
        except:
            self.kaydet1()
            pass

        print("çıktı: ", self.json1)

        return self.json1['status']



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




