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



class PostVideoLinkDM():

    def __init__(self,media_link='',message1='',link='',message2=''):

        self.mediadbul = 'https://' +  media_link

        self.dmmesaj = message1

        self.dmlinkgoder = link

        self.dmlinkmesajgonder = message2


        self.kullaniciuseridbul = ''

        
        self.username = ''
        self.password = ''
        self.BloksVersionId = 'e097ac2261d546784637b3df264aa3275cb6281d706d91484f43c207d6661931'
        self.deviceid = ''
        self.userid = ''
        self.claim = ''
        self.authorization = ''
        self.cookie_user_id = 0

        self.checksum = ''
        self.androidid = ''
        self.USER_AGENT = ''
        self.adid = ''
        self.guid = ''
        self.mykey = ''
        self.likeCount = 0
        self.pigeonid = ''
        self.phoneid = ''
        self.API_URL = 'https://i.instagram.com/api/v1/'
        self.API_URL2 = 'https://b.i.instagram.com/api/v1/'
        self.API_URL3 = 'https://z-p42.i.instagram.com/api/v1/'
        self.PASL = ''

        self.ip_port_proxy  = None
        self.auth_proxy = None
        self.root_proxy = None

        self.like_start_count = 0
        self.like_finish_count = 0
        self.error_users = []
        self.success_users = []
        self.cookie_user_id = 0
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




    def startProccess(self,target_user,auth_proxy,ip_port_proxy,db_pigeonid,db_claim,db_deviceid,db_phoneid,db_androidid,db_USER_AGENT,db_checksum,db_authorization,db_mid,db_userid,db_rur,db_waterfallid,db_adid,db_guid):


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


        self.kullaniciuseridbul = target_user

        self.cookie_user_id = 0


        self.appver = '212.0.0.38.119'


        self.process_ip_port_proxy_list = Proxy.objects.filter(ip_port_proxy=True,process_proxy=True)
        self.process_auth_proxy_list = Proxy.objects.filter(auth_proxy=True,process_proxy=True)
        self.get_ip_port_proxy = ip_port_proxy
        self.get_auth_proxy = auth_proxy

        self.aa = 0

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
        statusDM = False
        try:
            #print("mediadbul ",self.mediadbul)
            #print("dmlinkmesajgonder ",self.dmlinkmesajgonder)
            #print("dmlinkmesajgonder ",self.dmmesaj)
            #print("dmlinkgoder", self.dmlinkgoder)

            ### başlangıç ########

            print("c1")
            self.launcher1c()
            #print("c2")
            #self.feedtimeline()
            #print("c3")
            #self.reelstray()
            #print("c4")

            ### reel video DM gönderme ##

            print("b1")
            self.useridbul()

            print("b2")
            self.medyaidbul()

            print("b3")
            self.DM_video_gonder()

            print("b8")
            self.DM2()

            print("b9")

            self.DMlink()

            print("b10")

            statusDM = True
            self.success_users.append(self.cookie_user_id)


        except Exception as e:
            self.error_users.append(self.cookie_user_id)
            print(e)

        return {'status':statusDM,'message':self.error_message}

    def changeProxy(self):
        if self.get_ip_port_proxy:
            if self.process_ip_port_proxy_list:
                process_ip_port_proxy = self.process_ip_port_proxy_list[random.randrange(len(self.process_ip_port_proxy_list))]

                self.root_proxy = self.set_proxy_ip_port(process_ip_port_proxy.proxy)

        elif self.get_auth_proxy:
            if self.process_auth_proxy_list:
        
                process_auth_proxy = self.process_auth_proxy_list[random.randrange(len(self.process_auth_proxy_list))]
                self.root_proxy = self.set_proxy_auth(process_auth_proxy.proxy) 

    # like işlemleri  #

    def zaman(self):

        zamana = self.timestamp3(True)

        zamanxxx = zamana * 1.0002
        #print("aaaa",zamanxxx)
        zamanyyy = str(int(zamana))
        #print("bbb", zamanyyy[1:])

        self.zamanata1 = "1." + zamanyyy[1:] + "1" + "E12"
        #print("ccc",self.zamanata1)


        zaman1 = zamana * 1.0002
        zaman1a = zaman1 * 1.0002
        zaman2 = zaman1a * 1.0002
        zaman2a = zaman2 * 1.0002
        zaman3 = zaman2a * 1.0002
        zaman3a = zaman3 * 1.0002
        zaman4 = zaman3a * 1.0002
        zaman4a = zaman4 * 1.0002
        zaman5 = zaman4a * 1.0002
        zaman5a = zaman5 * 1.0002
        zaman6 = zaman5a * 1.0002
        zaman6a = zaman6 * 1.0002
        zaman7 = zaman6a * 1.0002
        zaman7a = zaman7 * 1.0002
        zaman8 = zaman7a * 1.0002
        zaman8a = zaman8 * 1.0002
        zaman9 = zaman8a * 1.0002
        zaman9a = zaman9 * 1.0002
        zaman10 = zaman9a * 1.0002
        zaman10a = zaman10 * 1.0002
        zaman11 = zaman10a * 1.0002
        zaman11a = zaman11 * 1.0002
        zaman12a = zaman11a * 1.0002
        zaman12 = zaman12a * 1.0002
        zaman13 = zaman12 * 1.0002
        zaman13a = zaman13 * 1.0002
        zaman14 = zaman13a * 1.0002
        zaman14a = zaman14 * 1.0002
        zaman15 = zaman14a * 1.0002
        zaman15a = zaman15 * 1.0002
        zaman16 = zaman15a * 1.0002
        zaman16a = zaman16 * 1.0002
        zaman17 = zaman16a * 1.0002
        zaman17a = zaman17 * 1.0002
        zaman18 = zaman17a * 1.0002
        zaman18a = zaman18 * 1.0002
        zaman19 = zaman18a * 1.0002
        zaman19a = zaman19 * 1.0002
        zaman20 = zaman19a * 1.0002
        zaman20a = zaman20 * 1.0002
        zaman21 = zaman20a * 1.0002
        zaman21a = zaman21 * 1.0002
        zaman22 = zaman21a * 1.0002
        zaman22a = zaman22 * 1.0002
        zaman23 = zaman22a * 1.0002
        zaman23a = zaman23 * 1.0002
        zaman24 = zaman23a * 1.0002
        zaman24a = zaman24 * 1.0002
        zaman25 = zaman24a * 1.0002
        zaman25a = zaman25 * 1.0002
        zaman26 = zaman25a * 1.0002
        zaman26a = zaman26 * 1.0002
        zaman27 = zaman26a * 1.0002
        zaman27a = zaman27 * 1.0002
        zaman28 = zaman27a * 1.0002
        zaman28a = zaman28 * 1.0002
        zaman29 = zaman28a * 1.0002
        zaman29a = zaman29 * 1.0002
        zaman30 = zaman29a * 1.0002
        zaman30a = zaman30 * 1.0002
        zaman31 = zaman30a * 1.0002
        zaman31a = zaman31 * 1.0002
        zaman32 = zaman31a * 1.0002
        zaman32a = zaman32 * 1.0002
        zaman33 = zaman32a * 1.0002
        zaman33a = zaman33 * 1.0002
        zaman34 = zaman33a * 1.0002
        zaman34a = zaman34 * 1.0002
        zaman35 = zaman34a * 1.0002
        zaman35a = zaman35 * 1.0002
        zaman36 = zaman35a * 1.0002
        zaman36a = zaman36 * 1.0002
        zaman37 = zaman36a * 1.0002
        zaman37a = zaman37 * 1.0002
        zaman38 = zaman37a * 1.0002
        zaman38a = zaman38 * 1.0002
        zaman39 = zaman38a * 1.0002
        zaman39a = zaman39 * 1.0002
        zaman40 = zaman39a * 1.0002
        zaman40a = zaman40 * 1.0002
        zaman41 = zaman40a * 1.0002
        zaman41a = zaman41 * 1.0002
        zaman42 = zaman41a * 1.0002
        zaman42a = zaman42 * 1.0002
        zaman43 = zaman42a * 1.0002
        zaman43a = zaman43 * 1.0002
        zaman44 = zaman43a * 1.0002
        zaman44a = zaman44 * 1.0002
        zaman45 = zaman44a * 1.0002
        zaman45a = zaman45 * 1.0002
        zaman46 = zaman45a * 1.0002
        zaman46a = zaman46 * 1.0002
        zaman47 = zaman46a * 1.0002
        zaman47a = zaman47 * 1.0002
        zaman48 = zaman47a * 1.0002
        zaman48a = zaman48 * 1.0002
        zaman49 = zaman48a * 1.0002
        zaman49a = zaman49 * 1.0002
        zaman50 = zaman49a * 1.0002
        zaman50a = zaman50 * 1.0002
        zaman51 = zaman50a * 1.0002
        zaman51a = zaman51 * 1.0002
        zaman52 = zaman51a * 1.0002
        zaman52a = zaman52 * 1.0002
        zaman53 = zaman52a * 1.0002
        zaman53a = zaman53 * 1.0002

        zaman54 = zaman53a * 1.0002
        zaman54a = zaman54 * 1.0002
        zaman55 = zaman54a * 1.0002
        zaman55a = zaman55 * 1.0002
        zaman56 = zaman55a * 1.0002
        zaman56a = zaman56 * 1.0002
        zaman57 = zaman56a * 1.0002
        zaman57a = zaman57 * 1.0002
        zaman58 = zaman57a * 1.0002
        zaman58a = zaman58 * 1.0002
        zaman59 = zaman58a * 1.0002
        zaman59a = zaman59 * 1.0002
        zaman60 = zaman59a * 1.0002
        zaman60a = zaman60 * 1.0002
        zaman61 = zaman60a * 1.0002
        zaman61a = zaman61 * 1.0002
        zaman62 = zaman61a * 1.0002
        zaman62a = zaman62 * 1.0002
        zaman63 = zaman62a * 1.0002
        zaman63a = zaman63 * 1.0002
        zaman64 = zaman63a * 1.0002
        zaman64a = zaman64 * 1.0002
        zaman65 = zaman64a * 1.0002
        zaman65a = zaman65 * 1.0002
        zaman66 = zaman65a * 1.0002
        zaman66a = zaman66 * 1.0002
        zaman67 = zaman66a * 1.0002
        zaman67a = zaman67 * 1.0002
        zaman68 = zaman67a * 1.0002
        zaman68a = zaman68 * 1.0002
        zaman69 = zaman68a * 1.0002
        zaman69a = zaman69 * 1.0002
        zaman70 = zaman69a * 1.0002
        zaman70a = zaman70 * 1.0002
        zaman71 = zaman70a * 1.0002
        zaman71a = zaman71 * 1.0002
        zaman72 = zaman71a * 1.0002
        zaman72a = zaman72 * 1.0002
        zaman73 = zaman72a * 1.0002
        zaman73a = zaman73 * 1.0002
        zaman74 = zaman73a * 1.0002
        zaman74a = zaman74 * 1.0002
        zaman75 = zaman74a * 1.0002
        zaman75a = zaman75 * 1.0002
        zaman76 = zaman75a * 1.0002
        zaman76a = zaman76 * 1.0002
        zaman77 = zaman76a * 1.0002
        zaman77a = zaman77 * 1.0002
        zaman78 = zaman77a * 1.0002
        zaman78a = zaman78 * 1.0002
        zaman79 = zaman78a * 1.0002
        zaman79a = zaman79 * 1.0002
        zaman80 = zaman79a * 1.0002
        zaman80a = zaman80 * 1.0002
        zaman81 = zaman80a * 1.0002

        zaman81a = zaman81 * 1.0002
        zaman82 = zaman81a * 1.0002
        zaman82a = zaman82 * 1.0002
        zaman83 = zaman82a * 1.0002
        zaman83a = zaman83 * 1.0002
        zaman84 = zaman83a * 1.0002
        zaman84a = zaman84 * 1.0002
        zaman85 = zaman84a * 1.0002
        zaman85a = zaman85 * 1.0002
        zaman86 = zaman85a * 1.0002
        zaman86a = zaman86 * 1.0002
        zaman87 = zaman86a * 1.0002
        zaman87a = zaman87 * 1.0002
        zaman88 = zaman87a * 1.0002
        zaman88a = zaman88 * 1.0002
        zaman89 = zaman88a * 1.0002
        zaman89a = zaman89 * 1.0002
        zaman90 = zaman89a * 1.0002
        zaman90a = zaman90 * 1.0002
        zaman91 = zaman90a * 1.0002
        zaman91a = zaman91 * 1.0002
        zaman92 = zaman91a * 1.0002
        zaman92a = zaman92 * 1.0002
        zaman93 = zaman92a * 1.0002
        zaman93a = zaman93 * 1.0002
        zaman94 = zaman93a * 1.0002
        zaman94a = zaman94 * 1.0002
        zaman95 = zaman94a * 1.0002
        zaman95a = zaman95 * 1.0002
        zaman96 = zaman95a * 1.0002
        zaman96a = zaman96 * 1.0002
        zaman97 = zaman96a * 1.0002
        zaman97a = zaman97 * 1.0002
        zaman98 = zaman97a * 1.0002
        zaman98a = zaman98 * 1.0002
        zaman99 = zaman98a * 1.0002
        zaman99a = zaman99 * 1.0002
        zaman100 = zaman99a * 1.0002
        zaman100a = zaman100 * 1.0002
        zaman101 = zaman100a * 1.0002
        zaman101a = zaman101 * 1.0002
        zaman102 = zaman101a * 1.0002
        zaman102a = zaman102 * 1.0002
        zaman103 = zaman102a * 1.0002
        zaman103a = zaman103 * 1.0002
        zaman104 = zaman103a * 1.0002
        zaman104a = zaman104 * 1.0002
        zaman105 = zaman104a * 1.0002
        zaman105a = zaman105 * 1.0002
        zaman106 = zaman105a * 1.0002
        zaman106a = zaman106 * 1.0002
        zaman107 = zaman106a * 1.0002
        zaman107a = zaman107 * 1.0002
        zaman108 = zaman107a * 1.0002
        zaman108a = zaman108 * 1.0002
        zaman109 = zaman108a * 1.0002
        zaman109a = zaman109 * 1.0002
        zaman110 = zaman109a * 1.0002
        zaman110a = zaman110 * 1.0002
        zaman111 = zaman110a * 1.0002



        self.zaman1 = str(int(zaman1))[:10] +"." + str(int(zaman1))[1:4]
        #print("zaman1",zaman1)
        self.zaman1a = str(int(zaman1a))
        self.zaman2 = str(int(zaman1))[:10] +"." + str(int(zaman1))[1:4]
        self.zaman2a = str(int(zaman2a))
        self.zaman3 = str(int(zaman2))[:10] +"." + str(int(zaman2))[1:4]
        self.zaman3a = str(int(zaman3a))
        self.zaman4 = str(int(zaman3))[:10] +"." + str(int(zaman3))[1:4]
        self.zaman4a = str(int(zaman4a))
        self.zaman5 = str(int(zaman4))[:10] +"." + str(int(zaman4))[1:4]
        self.zaman5a = str(int(zaman5a))
        self.zaman6 = str(int(zaman5))[:10] +"." + str(int(zaman5))[1:4]
        self.zaman6a = str(int(zaman6a))
        self.zaman7 = str(int(zaman6))[:10] +"." + str(int(zaman6))[1:4]
        self.zaman7a = str(int(zaman7a))
        self.zaman8 = str(int(zaman7))[:10] +"." + str(int(zaman7))[1:4]
        self.zaman8a = str(int(zaman8a))
        self.zaman9 = str(int(zaman8))[:10] +"." + str(int(zaman8))[1:4]
        self.zaman9a = str(int(zaman9a))
        self.zaman10 = str(int(zaman9))[:10] +"." + str(int(zaman9))[1:4]
        self.zaman10a = str(int(zaman10a))
        self.zaman11 = str(int(zaman10))[:10] +"." + str(int(zaman10))[1:4]
        self.zaman11a = str(int(zaman11a))
        self.zaman12 = str(int(zaman11))[:10] +"." + str(int(zaman11))[1:4]
        self.zaman12a = str(int(zaman12a))
        self.zaman13 = str(int(zaman12))[:10] +"." + str(int(zaman12))[1:4]
        self.zaman13a = str(int(zaman13a))
        self.zaman14 = str(int(zaman13))[:10] +"." + str(int(zaman13))[1:4]
        self.zaman14a = str(int(zaman14a))
        self.zaman15 = str(int(zaman14))[:10] +"." + str(int(zaman14))[1:4]
        self.zaman15a = str(int(zaman15a))
        self.zaman16 = str(int(zaman15))[:10] +"." + str(int(zaman15))[1:4]
        self.zaman16a = str(int(zaman16a))
        self.zaman17 = str(int(zaman16))[:10] +"." + str(int(zaman16))[1:4]
        self.zaman17a = str(int(zaman17a))
        self.zaman18 = str(int(zaman17))[:10] +"." + str(int(zaman17))[1:4]
        self.zaman18a = str(int(zaman18a))
        self.zaman19 = str(int(zaman18))[:10] +"." + str(int(zaman18))[1:4]
        self.zaman19a = str(int(zaman19a))
        self.zaman20 = str(int(zaman19))[:10] +"." + str(int(zaman19))[1:4]
        self.zaman20a = str(int(zaman20a))
        self.zaman21 = str(int(zaman20))[:10] +"." + str(int(zaman20))[1:4]
        self.zaman21a = str(int(zaman21a))
        self.zaman22 = str(int(zaman21))[:10] +"." + str(int(zaman21))[1:4]
        self.zaman22a = str(int(zaman22a))
        self.zaman23 = str(int(zaman22))[:10] +"." + str(int(zaman22))[1:4]
        self.zaman23a = str(int(zaman23a))
        self.zaman24 = str(int(zaman23))[:10] +"." + str(int(zaman23))[1:4]
        self.zaman24a = str(int(zaman24a))
        self.zaman25 = str(int(zaman24))[:10] +"." + str(int(zaman24))[1:4]
        self.zaman25a = str(int(zaman25a))
        self.zaman26 = str(int(zaman25))[:10] +"." + str(int(zaman25))[1:4]
        self.zaman26a = str(int(zaman26a))
        self.zaman27 = str(int(zaman26))[:10] +"." + str(int(zaman26))[1:4]
        self.zaman27a = str(int(zaman27a))
        self.zaman28 = str(int(zaman27))[:10] +"." + str(int(zaman27))[1:4]
        self.zaman28a = str(int(zaman28a))
        self.zaman29 = str(int(zaman28))[:10] +"." + str(int(zaman28))[1:4]
        self.zaman29a = str(int(zaman29a))
        self.zaman30 = str(int(zaman29))[:10] +"." + str(int(zaman29))[1:4]
        self.zaman30a = str(int(zaman30a))
        self.zaman31 = str(int(zaman30))[:10] +"." + str(int(zaman30))[1:4]
        self.zaman31a = str(int(zaman31a))
        self.zaman32 = str(int(zaman32))[:10] +"." + str(int(zaman32))[1:4]
        self.zaman32a = str(int(zaman32a))
        self.zaman33 = str(int(zaman33))[:10] +"." + str(int(zaman33))[1:4]
        self.zaman33a = str(int(zaman33a))
        self.zaman34 = str(int(zaman34))[:10] +"." + str(int(zaman34))[1:4]
        self.zaman34a = str(int(zaman34a))
        self.zaman35 = str(int(zaman35))[:10] +"." + str(int(zaman35))[1:4]
        self.zaman35a = str(int(zaman35a))
        self.zaman36 = str(int(zaman36))[:10] +"." + str(int(zaman36))[1:4]
        self.zaman36a = str(int(zaman36a))
        self.zaman37 = str(int(zaman37))[:10] +"." + str(int(zaman37))[1:4]
        self.zaman37a = str(int(zaman37a))
        self.zaman38 = str(int(zaman38))[:10] +"." + str(int(zaman38))[1:4]
        self.zaman38a = str(int(zaman38a))
        self.zaman39 = str(int(zaman39))[:10] +"." + str(int(zaman39))[1:4]
        self.zaman39a = str(int(zaman39a))
        self.zaman40 = str(int(zaman40))[:10] +"." + str(int(zaman40))[1:4]
        self.zaman40a = str(int(zaman40a))
        self.zaman41 = str(int(zaman41))[:10] +"." + str(int(zaman41))[1:4]
        self.zaman41a = str(int(zaman41a))
        self.zaman42 = str(int(zaman42))[:10] +"." + str(int(zaman42))[1:4]
        self.zaman42a = str(int(zaman42a))
        self.zaman43 = str(int(zaman43))[:10] +"." + str(int(zaman43))[1:4]
        self.zaman43a = str(int(zaman43a))
        self.zaman44 = str(int(zaman44))[:10] +"." + str(int(zaman44))[1:4]
        self.zaman44a = str(int(zaman44a))
        self.zaman45 = str(int(zaman45))[:10] +"." + str(int(zaman45))[1:4]
        self.zaman45a = str(int(zaman45a))
        self.zaman46 = str(int(zaman46))[:10] +"." + str(int(zaman46))[1:4]
        self.zaman46a = str(int(zaman46a))
        self.zaman47 = str(int(zaman47))[:10] +"." + str(int(zaman47))[1:4]
        self.zaman47a = str(int(zaman47a))
        self.zaman48 = str(int(zaman48))[:10] +"." + str(int(zaman48))[1:4]
        self.zaman48a = str(int(zaman48a))
        self.zaman49 = str(int(zaman49))[:10] +"." + str(int(zaman49))[1:4]
        self.zaman49a = str(int(zaman49a))
        self.zaman50 = str(int(zaman50))[:10] +"." + str(int(zaman50))[1:4]
        self.zaman50a = str(int(zaman50a))
        self.zaman51 = str(int(zaman51))[:10] +"." + str(int(zaman51))[1:4]
        self.zaman51a = str(int(zaman51a))
        self.zaman52 = str(int(zaman52))[:10] +"." + str(int(zaman52))[1:4]
        self.zaman52a = str(int(zaman52a))
        self.zaman53 = str(int(zaman53))[:10] +"." + str(int(zaman53))[1:4]
        self.zaman53a = str(int(zaman53a))




        self.zaman54 = str(int(zaman54))[:10] +"." + str(int(zaman54))[1:4]
        self.zaman54a = str(int(zaman54a))
        self.zaman55 = str(int(zaman55))[:10] +"." + str(int(zaman55))[1:4]
        self.zaman55a = str(int(zaman55a))
        self.zaman56 = str(int(zaman56))[:10] +"." + str(int(zaman56))[1:4]
        self.zaman56a = str(int(zaman56a))
        self.zaman57 = str(int(zaman57))[:10] +"." + str(int(zaman57))[1:4]
        self.zaman57a = str(int(zaman57a))
        self.zaman58 = str(int(zaman58))[:10] +"." + str(int(zaman58))[1:4]
        self.zaman58a = str(int(zaman58a))
        self.zaman59 = str(int(zaman59))[:10] +"." + str(int(zaman59))[1:4]
        self.zaman59a = str(int(zaman59a))
        self.zaman60 = str(int(zaman60))[:10] +"." + str(int(zaman60))[1:4]
        self.zaman60a = str(int(zaman60a))
        self.zaman61 = str(int(zaman61))[:10] +"." + str(int(zaman61))[1:4]
        self.zaman61a = str(int(zaman61a))
        self.zaman62 = str(int(zaman62))[:10] +"." + str(int(zaman62))[1:4]
        self.zaman62a = str(int(zaman62a))
        self.zaman63 = str(int(zaman63))[:10] +"." + str(int(zaman63))[1:4]
        self.zaman63a = str(int(zaman63a))
        self.zaman64 = str(int(zaman64))[:10] +"." + str(int(zaman64))[1:4]
        self.zaman64a = str(int(zaman64a))
        self.zaman65 = str(int(zaman65))[:10] +"." + str(int(zaman65))[1:4]
        self.zaman65a = str(int(zaman65a))
        self.zaman66 = str(int(zaman66))[:10] +"." + str(int(zaman66))[1:4]
        self.zaman66a = str(int(zaman66a))
        self.zaman67 = str(int(zaman67))[:10] +"." + str(int(zaman67))[1:4]
        self.zaman67a = str(int(zaman67a))
        self.zaman68 = str(int(zaman68))[:10] +"." + str(int(zaman68))[1:4]
        self.zaman68a = str(int(zaman68a))


        self.zaman69 = str(int(zaman69))[:10] +"." + str(int(zaman69))[1:4]
        self.zaman69a = str(int(zaman69a))
        self.zaman70 = str(int(zaman70))[:10] +"." + str(int(zaman70))[1:4]
        self.zaman70a = str(int(zaman70a))
        self.zaman71 = str(int(zaman71))[:10] +"." + str(int(zaman71))[1:4]
        self.zaman71a = str(int(zaman71a))
        self.zaman72 = str(int(zaman72))[:10] +"." + str(int(zaman72))[1:4]
        self.zaman72a = str(int(zaman72a))
        self.zaman73 = str(int(zaman73))[:10] +"." + str(int(zaman73))[1:4]
        self.zaman73a = str(int(zaman73a))
        self.zaman74 = str(int(zaman74))[:10] +"." + str(int(zaman74))[1:4]
        self.zaman74a = str(int(zaman74a))




        self.zaman75 = str(int(zaman75))[:10] +"." + str(int(zaman75))[1:4]
        self.zaman75a = str(int(zaman75a))
        self.zaman76 = str(int(zaman76))[:10] +"." + str(int(zaman76))[1:4]
        self.zaman76a = str(int(zaman76a))
        self.zaman77 = str(int(zaman77))[:10] +"." + str(int(zaman77))[1:4]
        self.zaman77a = str(int(zaman77a))
        self.zaman78 = str(int(zaman78))[:10] +"." + str(int(zaman78))[1:4]
        self.zaman78a = str(int(zaman78a))
        self.zaman79 = str(int(zaman79))[:10] +"." + str(int(zaman79))[1:4]
        self.zaman79a = str(int(zaman79a))
        self.zaman80 = str(int(zaman80))[:10] +"." + str(int(zaman80))[1:4]
        self.zaman80a = str(int(zaman80a))
        self.zaman81 = str(int(zaman81))[:10] +"." + str(int(zaman81))[1:4]

        self.zaman81a = str(int(zaman81a))
        self.zaman82 = str(int(zaman82))[:10] +"." + str(int(zaman82))[1:4]



        return True


    def feedtimeline(self):

        try:

            data = 'feed_view_info=%5B%5D&reason=cold_start_fetch&timezone_offset=10800&device_id=' + self.db_deviceid + '&request_id=' + self.generateUUID(
                True) + '&is_pull_to_refresh=0&_uuid=' + self.db_guid + '&session_id=' + self.generateUUID(
                True) + '&bloks_versioning_id=' + self.BloksVersionId

            status = self.SendRequestfeedtime(data)
        except Exception as e:
            print('hata!!', e)
            self.changeProxy()
            self.feedtimeline()
            pass

        return status

    def reelstray(self):

        try:

            data = 'supported_capabilities_new=%5B%7B%22name%22%3A%22SUPPORTED_SDK_VERSIONS%22%2C%22value%22%3A%22108.0%2C109.0%2C110.0%2C111.0%2C112.0%2C113.0%2C114.0%2C115.0%2C116.0%2C117.0%2C118.0%2C119.0%2C120.0%2C121.0%2C122.0%2C123.0%2C124.0%2C125.0%2C126.0%22%7D%2C%7B%22name%22%3A%22FACE_TRACKER_VERSION%22%2C%22value%22%3A%2214%22%7D%2C%7B%22name%22%3A%22segmentation%22%2C%22value%22%3A%22segmentation_enabled%22%7D%2C%7B%22name%22%3A%22COMPRESSION%22%2C%22value%22%3A%22ETC2_COMPRESSION%22%7D%2C%7B%22name%22%3A%22world_tracker%22%2C%22value%22%3A%22world_tracker_enabled%22%7D%2C%7B%22name%22%3A%22gyroscope%22%2C%22value%22%3A%22gyroscope_enabled%22%7D%5D&reason=cold_start&timezone_offset=10800&tray_session_id=' + self.generateUUID(
                True) + '&request_id=' + self.generateUUID(True) + '&_uuid=' + self.db_guid + '&page_size=50'

            status = self.SendRequestreeltray(data)
        except Exception as e:
            print('hata !', e)
            self.changeProxy()
            self.reelstray()
            pass

        return status

    def launcher1c(self):

        try:

            alfason = {
                "id": self.userid,
                "_uid": self.userid,
                "_uuid": self.guid,
                "server_config_retrieval": "1"
            }
            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestsync1(signature18)
        except Exception as e:
            print("hhh: ", e)
            self.changeProxy()
            self.launcher1c()
            pass

        return status




    def useridbul(self):

        try:

            link1 = "users/" + self.kullaniciuseridbul + "/usernameinfo/?from_module=deep_link_util"

            self.SendRequestloginsonrasitoplu2get1a(link1)

            print("çıktı: ", self.json1)


        except:
            if self.aa < 3:
                self.aa += 1
                self.useridbul()
                print('sorgu tekrar ediliyor')
            else:
                print("canommmm1")
                raise Exception("iptalllll")

            # pass

        self.hesapidbul = str(int(self.json1['user']['pk']))
        # print(self.hesapidbul)

        return True

    def medyaidbul(self):

        try:
            link1 = self.mediadbul + "?utm_medium=copy_link"

            ddd80 = urllib.parse.quote(link1)
            # print("aaaaa", ddd80)

            link2 = "oembed/?url=" + ddd80

            self.SendRequestloginsonrasitoplu2get1a(link2)

        # print("çıktı: ",self.json1)

        except:
            self.medyaidbul()
            pass

        hobbala = str(self.json1['media_id'])
        atakan = hobbala.split("_")
        self.media_id = atakan[0]
        print("media_id: ", self.media_id)
        return True



    def DM_video_gonder(self):

        try:

            url = 'direct_v2/threads/broadcast/media_share/?media_type=video'

            self.timeson12 = str(int(datetime.now().timestamp()))

            atmaca1 = '[[' + self.hesapidbul + ']]'
            ddd81 = urllib.parse.quote(atmaca1)

            videopostid = self.media_id

            data = 'recipient_users=' + ddd81 + '&action=send_item&is_shh_mode=0&send_attribution=feed_contextual_chain&client_context=' + self.timeson12 + '&media_id=' + videopostid + '&device_id=' + self.androidid + '&mutation_token=' + self.timeson12 + '&_uuid=' + self.guid + '&offline_threading_id=' + self.timeson12

            self.SendRequestloginsonrasitoplu2post1a(url, data)


        except:
            self.DM_video_gonder()
            pass

        self.thred = str(int(self.json1['payload']['thread_id']))
        print("thread son: ", self.thred)

        self.items = str(int(self.json1['payload']['item_id']))
        print("items son: ", self.items)

        return True


    def DM2(self):

        try:

            mesaj = self.dmmesaj
            ddd81 = urllib.parse.quote(mesaj)
            #print("aaaaa", ddd81)


            self.timeson1 = str(int(self.timestamp3(True)) * 1.0004)

            DM2 = "direct_v2/threads/broadcast/text/"

            al = '[[' + self.hesapidbul + ']]'

            ddd80 = urllib.parse.quote(al)
            print("aaaaa", ddd80)

            data = 'recipient_users=' + ddd80 + '&action=send_item&is_shh_mode=0&send_attribution=clips_viewer_explore_popular_major_unit&client_context=' + self.timeson1 + '&text=' + ddd81 + '&device_id=' + self.androidid + '&mutation_token=' + self.timeson1 + '&_uuid=' + self.guid + '&offline_threading_id=' + self.timeson1

            # signature18 = "signed_body=SIGNATURE.{}".format(json.dumps(data216))

            self.SendRequestloginsonrasitoplu2post1a(DM2, data)

            print("çıktı: ", self.json1)

        except Exception as e:
            print(e)
            self.changeProxy()
            self.DM2()
            pass


        return True





    def DMlink(self):

        try:

            self.timeson1 = str(int(datetime.now().timestamp()))

            self.hesapidDM = str(self.hesapidbul)

            DM3 = "direct_v2/threads/broadcast/link/"

            atmaca1 = '[[' + self.hesapidDM + ']]'
            ddd81 = urllib.parse.quote(atmaca1)

            atmaca2 = '[[' + self.hesapidDM + ']]'
            ddd82 = urllib.parse.quote(atmaca2)

            linkatmaca2 = self.dmlinkgoder
            ddd85 = urllib.parse.quote(linkatmaca2)

            linkatmaca1 = 'https://' + linkatmaca2 + '/' + '\n'
            ddd83 = urllib.parse.quote(linkatmaca1)

            linkatmaca3 = '["' + 'https:\/\/' + linkatmaca2 + '"]'
            ddd85 = urllib.parse.quote(linkatmaca3)

            linkmessage = self.dmlinkmesajgonder
            ddd84 = urllib.parse.quote(linkmessage)

            data2 = 'recipient_users=' + ddd81 + '&link_text=' + ddd83 + ddd84 + '&link_urls=' + ddd85 + '&action=send_item&is_shh_mode=0&send_attribution=inbox_search&client_context=' + self.timeson1 + '&device_id=' + self.androidid + '&mutation_token=' + self.timeson1 + '&_uuid=' + self.guid + '&offline_threading_id=' + self.timeson1

            self.SendRequestloginsonrasitoplu2post1a(DM3, data2)

            print("çıktı: ", self.json1)


        except:
            self.DMlink()
            pass

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
        print("Status1: ", response2.status_code)
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
        print("Status1: ", response2.status_code)

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
        print("Status1: ", response2.status_code)



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


    ###############################
    def SendRequestreeltray(self, post=None):

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
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
            'Content-Length': str(int(len(post)))
        }
        response2 = requests.post('https://i.instagram.com/api/v1/feed/reels_tray/', headers=headers, data=post,
                                  verify=True, proxies=self.root_proxy, timeout=30)  # proxies=proxy
        print("reeltray Status: ", response2.status_code)
        # print("timeline Status5: ", response2.json())
        # print("Status5: ", response2.headers)

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
        return {'status_code': response2.status_code, 'status5': response2.json()}

    def SendRequestfeedtime(self, post=None):

        headers = {
            'X-Ads-Opt-Out': '0',
            'X-Google-AD-ID': self.adid,
            'X-DEVICE-ID': self.deviceid,
            'X-FB': '1',
            'X-CM-Bandwidth-KBPS': '-1.000',
            'X-CM-Latency': '60.000',
            'battery_level': str(random.randint(1, 100)),
            'is_charging': '1',
            'is_dark_mode': '0',
            'phone_id': self.phoneid,
            'will_sound_on': '0',
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
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
            'Content-Length': str(int(len(post)))
        }
        response2 = requests.post('https://i.instagram.com/api/v1/feed/timeline/', headers=headers, data=post,
                                  verify=True, proxies=self.root_proxy, timeout=30)  # proxies=proxy
        print("feedtime Status: ", response2.status_code)
        # print("timeline Status5: ", response2.json())
        # print("Status5: ", response2.headers)

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
        return {'status_code': response2.status_code, 'status5': response2.json()}

    def SendRequestsync1(self, post=None):

        headers = {
            'X-IG-App-Locale': 'tr_TR',
            'X-IG-Device-Locale': 'tr_TR',
            'X-IG-Mapped-Locale': 'tr_TR',
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
        response2 = requests.post('https://i.instagram.com/api/v1/qe/sync/', headers=headers, data=post, verify=True,
                                  proxies=self.root_proxy, timeout=30)

        print("Status6: ", response2.status_code)

        self.json1 = response2.json()

        try:

            message = self.json1['message']
            self.error_message = message
        except:
            pass


        self.rur = response2.headers['ig-set-ig-u-rur']
        # print("rur: ", self.rur)

        # print(response2.content)

        return True





