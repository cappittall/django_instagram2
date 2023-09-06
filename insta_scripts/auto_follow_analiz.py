import hashlib
import datetime
import urllib
import uuid
import random
import requests
import urllib.parse
from datetime import datetime
from custom_admin.models import Proxy

import urllib.parse


from core.get_path import outpath
BASE_DIR = outpath()






class AutoFollowAnaliz():

    def __init__(self,username='',password='',getusername=''):
        self.getusername = getusername
        self.username = username
        self.password = password
        self.db_BloksVersionId = 'e097ac2261d546784637b3df264aa3275cb6281d706d91484f43c207d6661931'
        self.deviceid = ''
        self.androidid = ''
        self.USER_AGENT = ''
        self.adid = ''
        self.guid = ''
        self.pigeonid = ''
        self.phoneid = ''
        self.API_URL = 'https://i.instagram.com/api/v1/'
        self.API_URL2 = 'https://b.i.instagram.com/api/v1/'
        self.API_URL3 = 'https://z-p42.i.instagram.com/api/v1/'
        self.PASL = ''
        self.root_proxy = None
        self.error_message = ''

    def timestamp1(self, type):
        timeson114 = str(datetime.now().timestamp())  # str(int(datetime.now().timestamp()))
        
        if (type):
          return timeson114


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




    def autoFollowAnalizStart(self,cookie_user_id,auth_proxy,ip_port_proxy,db_pigeonid,db_claim,db_deviceid,db_phoneid,db_androidid,db_USER_AGENT,db_checksum,db_authorization,db_mid,db_userid,db_rur,db_waterfallid,db_adid,db_guid,db_mykey):

        if ip_port_proxy:
            
            self.root_proxy = self.set_proxy_ip_port(ip_port_proxy.proxy)
        elif auth_proxy:

            self.root_proxy = self.set_proxy_auth(auth_proxy.proxy)

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


#######################
        self.BloksVersionId = self.db_BloksVersionId
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
        ##

        ### işlem başlangıç  ####
        data = None
        try:

            ### oto analiz 1 ########

            print("d0")
            self.useridbul()
            print("d1")
            data = self.ototakipanaliz()
            print("d2")

        except:
            return data
        
        return data

    def changeProxy(self):
        if self.get_ip_port_proxy:
            if self.process_ip_port_proxy_list:
                process_ip_port_proxy = self.process_ip_port_proxy_list[random.randrange(len(self.process_ip_port_proxy_list))]

                self.root_proxy = self.set_proxy_ip_port(process_ip_port_proxy.proxy)

        elif self.get_auth_proxy:
            if self.process_auth_proxy_list:
        
                process_auth_proxy = self.process_auth_proxy_list[random.randrange(len(self.process_auth_proxy_list))]
                self.root_proxy = self.set_proxy_auth(process_auth_proxy.proxy)

    def zaman(self):

        zamana = self.timestamp3(True)

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
        print(zaman1)
        print(zaman2)
        print(zaman53a)

        self.zaman1 = zaman1
        self.zaman1a = str(int(zaman1a))
        self.zaman2 = zaman2
        self.zaman2a = str(int(zaman2a))
        self.zaman3 = zaman3
        self.zaman3a = str(int(zaman3a))
        self.zaman4 = zaman4
        self.zaman4a = str(int(zaman4a))
        self.zaman5 = zaman5
        self.zaman5a = str(int(zaman5a))
        self.zaman6 = zaman6
        self.zaman6a = str(int(zaman6a))
        self.zaman7 = zaman7
        self.zaman7a = str(int(zaman7a))
        self.zaman8 = zaman8
        self.zaman8a = str(int(zaman8a))
        self.zaman9 = zaman9
        self.zaman9a = str(int(zaman9a))
        self.zaman10 = zaman10
        self.zaman10a = str(int(zaman10a))
        self.zaman11 = zaman11
        self.zaman11a = str(int(zaman11a))
        self.zaman12 = zaman12
        self.zaman12a = str(int(zaman12a))
        self.zaman13 = zaman13
        self.zaman13a = str(int(zaman13a))
        self.zaman14 = zaman14
        self.zaman14a = str(int(zaman14a))
        self.zaman15 = zaman15
        self.zaman15a = str(int(zaman15a))
        self.zaman16 = zaman16
        self.zaman16a = str(int(zaman16a))
        self.zaman17 = zaman17
        self.zaman17a = str(int(zaman17a))
        self.zaman18 = zaman18
        self.zaman18a = str(int(zaman18a))
        self.zaman19 = zaman19
        self.zaman19a = str(int(zaman19a))
        self.zaman20 = zaman20
        self.zaman20a = str(int(zaman20a))
        self.zaman21 = zaman21
        self.zaman21a = str(int(zaman21a))
        self.zaman22 = zaman22
        self.zaman22a = str(int(zaman22a))
        self.zaman23 = zaman23
        self.zaman23a = str(int(zaman23a))
        self.zaman24 = zaman24
        self.zaman24a = str(int(zaman24a))
        self.zaman25 = zaman25
        self.zaman25a = str(int(zaman25a))
        self.zaman26 = zaman26
        self.zaman26a = str(int(zaman26a))
        self.zaman27 = zaman27
        self.zaman27a = str(int(zaman27a))
        self.zaman28 = zaman28
        self.zaman28a = str(int(zaman28a))
        self.zaman29 = zaman29
        self.zaman29a = str(int(zaman29a))
        self.zaman30 = zaman30
        self.zaman30a = str(int(zaman30a))
        self.zaman31 = zaman31
        self.zaman31a = str(int(zaman31a))
        self.zaman32 = zaman32
        self.zaman32a = str(int(zaman32a))
        self.zaman33 = zaman33
        self.zaman33a = str(int(zaman33a))
        self.zaman34 = zaman34
        self.zaman34a = str(int(zaman34a))
        self.zaman35 = zaman35
        self.zaman35a = str(int(zaman35a))
        self.zaman36 = zaman36
        self.zaman36a = str(int(zaman36a))
        self.zaman37 = zaman37
        self.zaman37a = str(int(zaman37a))
        self.zaman38 = zaman38
        self.zaman38a = str(int(zaman38a))
        self.zaman39 = zaman39
        self.zaman39a = str(int(zaman39a))
        self.zaman40 = zaman40
        self.zaman40a = str(int(zaman40a))
        self.zaman41 = zaman41
        self.zaman41a = str(int(zaman41a))
        self.zaman42 = zaman42
        self.zaman42a = str(int(zaman42a))
        self.zaman43 = zaman43
        self.zaman43a = str(int(zaman43a))
        self.zaman44 = zaman44
        self.zaman44a = str(int(zaman44a))
        self.zaman45 = zaman45
        self.zaman45a = str(int(zaman45a))
        self.zaman46 = zaman46
        self.zaman46a = str(int(zaman46a))
        self.zaman47 = zaman47
        self.zaman47a = str(int(zaman47a))
        self.zaman48 = zaman48
        self.zaman48a = str(int(zaman48a))
        self.zaman49 = zaman49
        self.zaman49a = str(int(zaman49a))
        self.zaman50 = zaman50
        self.zaman50a = str(int(zaman50a))
        self.zaman51 = zaman51
        self.zaman51a = str(int(zaman51a))
        self.zaman52 = zaman52
        self.zaman52a = str(int(zaman52a))
        self.zaman53 = zaman53
        self.zaman53a = str(int(zaman53a))

        return True


    # like işlemleri  #

    def useridbul(self):

        if True:
    


            link1 = "users/" + self.getusername + "/usernameinfo/?from_module=deep_link_util"

            print('self.getusername : ',self.getusername)
            self.SendRequestloginsonrasitoplu2get1a(link1)

        #except:
        #    self.useridbul()
        #    pass


        print("çıktı: ",self.json1)

        self.hesapid = str(int(self.json1['user']['pk']))
        #print(self.hesapidbul)

        return True

    def ototakipanaliz(self):

        try:

            link2 = 'friendships/' + self.hesapid + '/following/?includes_hashtags=true&search_surface=follow_list_page&query=&enable_groups=true&rank_token=' + self.generateUUID(True)
            print("hesap id : ",self.hesapid)
            self.SendRequestloginsonrasitoplu2get1a(link2)

            #print("çıktı: ",self.json1)
        except:
            self.changeProxy()
            self.ototakipanaliz()
            pass


        caskim = self.json1

        usersData = []
        for x in caskim['users']:
            usersData.append({'pk': x['pk'], 'username': x['username']})

        print(usersData)
        return usersData


    ######### istek yapıları #########

    def SendRequestloginsonrasitoplu2get1a(self, endpoint):
        print('adim 1')
        headers = {
            'X-IG-App-Locale': 'tr_TR',
            'X-IG-Device-Locale': 'tr_TR',
            'X-IG-Mapped-Locale': 'tr_TR',
            'X-Pigeon-Session-Id': 'UFS-' + self.pigeonid,
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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTv10=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'X-MID': self.mid,
            #'IG-U-SHBID': self.shbid,
            #'IG-U-SHBTS': self.shbts,
            'IG-U-DS-USER-ID': self.userid,
            'IG-U-RUR': self.rur,
            'IG-INTENDED-USER-ID': self.userid,
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'b.i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            }
        print('adim 2 ')    
        response2 = requests.get('https://b.i.instagram.com/api/v1/' + endpoint, headers=headers,verify=True, proxies=self.root_proxy, timeout=15)  # proxies=proxy
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
