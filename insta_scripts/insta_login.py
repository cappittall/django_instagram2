import hashlib
import datetime
import urllib
import uuid
import random
import requests
import json
import urllib.parse
from datetime import datetime
import base64
import json
import tempfile

from pathlib import Path

from instagram_private_api import Client, ClientCookieExpiredError, ClientLoginRequiredError
from dateutil.relativedelta import relativedelta
from fbns_mqtt.fbns_mqtt import FBNSMQTTClient, FBNSAuth
import asyncio

BASE_DIR = Path(__file__).resolve().parent.parent


class Login:

    def __init__(self, username='', password=''):

        self.username = username
        self.password = password
        self.userid = ''
        self.BloksVersionId = 'e097ac2261d546784637b3df264aa3275cb6281d706d91484f43c207d6661931'
        self.deviceid = ''
        self.androidid = ''
        self.mykey = ''
        self.checksum = ''
        self.authorization = ''
        self.USER_AGENT = ''
        self.waterfall_id = ''
        self.claim = ''
        self.adid = ''
        self.mid = ''
        self.guid = ''
        self.rur = ''
        self.pigeonid = ''
        self.phoneid = ''
        self.API_URL = 'https://i.instagram.com/api/v1/'
        self.API_URL2 = 'https://b.i.instagram.com/api/v1/'
        self.API_URL3 = 'https://z-p42.i.instagram.com/api/v1/'
        self.PASL = ''
        self.user_data = ''
        self.login_after_proxy = None
        self.login_proxy = None
        self.registerkey = ''
        self.ck_data = ''


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

    def user_agent_compile(self, agent):

        agent = agent.split(" ")

        outDict = {
            'device_type': str(agent[7]).replace(";", ""),
            'brand': str(agent[6]).replace(";", ""),
            'manufacturer': str(agent[6]).replace(";", ""),
            'os_type': str(agent[2]),
            'os_ver': str(agent[3]).replace(";", "").split("/")[-1],
        }

        return outDict

    def set_proxy_ip_port(self, proxy):

        hostnamegel = proxy.split(":")[0]
        portgel = proxy.split(":")[1]

        proxy = hostnamegel + ":" + portgel

        proxyson = {'https': 'http://' + proxy}

        return proxyson

    def set_proxy_auth(self, proxy):
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

    def reCreate(self):
        self.deviceid1 = self.generateUUID(True)
        self.deviceid = self.deviceid1
        self.pigeonid1 = self.generateUUID(True)
        self.pigeonid = self.pigeonid1
        self.adid1 = self.generateUUID(True)
        self.adid = self.adid1
        self.guid = self.deviceid
        self.phoneid1 = self.generateUUID(True)
        self.phoneid = self.phoneid1
        self.session_id = self.generateUUID(True)
        self.waterfall_id1 = self.generateUUID(True)
        self.waterfall_id = self.waterfall_id1

        self.appver = '187.0.0.32.120'
        AGENTSON = open((BASE_DIR / 'insta_scripts/androidagenttrson.txt'), "r", encoding="utf-8").read().splitlines()
        AGENT = random.choice(AGENTSON)
        self.USER_AGENT = 'Instagram 187.0.0.32.120 ' + AGENT + ' 289692181)'
        m = hashlib.md5()
        m.update(self.username.encode('utf-8') + self.password.encode('utf-8'))
        self.androidid = self.generateDeviceId(m.hexdigest())


        veriler = self.user_agent_compile(self.USER_AGENT)
        # print(veriler)

        self.deviceapp = veriler['device_type']
        # print(self.deviceapp)

        self.brandapp = veriler['brand']
        # print(self.brandapp)

        self.manufacturerapp = veriler['manufacturer']
        # print(self.manufacturerapp)

        self.os_typeapp = veriler['os_type']
        # print(self.os_typeapp)

        self.os_verapp = veriler['os_ver']
        # print(self.os_verapp)

    def loginLaterThread(self):
        login_error = False
   

        while_turn = True
        countof429 = 0
        while while_turn and login_error == False:

            try:
                if countof429 >= 10:
                    while_turn = False
                    break
                else:
                    countof429 += 1

                status_code = self.register1()
                if str(status_code) == '429':

                    while_turn = True


                elif str(status_code) == '400' or str(status_code) == '403':
                    while_turn = False
                    login_error = True
                    break

                else:
                    while_turn = False
            except Exception as e:
                print('a8 hata',e)

                login_error = True
                while_turn = False

        print("a8")

        while_turn = True
        countof429 = 0
        while while_turn and login_error == False:

            try:
                if countof429 >= 10:
                    while_turn = False
                    break
                else:
                    countof429 += 1

                status_code = self.ig_steps()
                if str(status_code) == '429':

                    while_turn = True


                elif str(status_code) == '400' or str(status_code) == '403':
                    while_turn = False
                    login_error = True
                    break

                else:
                    while_turn = False
            except Exception as e:
                print('a10 hata',e)

                login_error = True
                while_turn = False

        print("a9")

        while_turn = True
        countof429 = 0
        while while_turn and login_error == False:

            try:
                if countof429 >= 10:
                    while_turn = False
                    break
                else:
                    countof429 += 1

                status_code = self.feedtimeline()
                if str(status_code) == '429':

                    while_turn = True


                elif str(status_code) == '400' or str(status_code) == '403':
                    while_turn = False
                    login_error = True
                    break

                else:
                    while_turn = False
            except Exception as e:
                print('a9 hata',e)
                login_error = True
                while_turn = False

        print("a10")

        while_turn = True
        countof429 = 0
        while while_turn and login_error == False:

            try:
                if countof429 >= 10:
                    while_turn = False
                    break
                else:
                    countof429 += 1

                status_code = self.reelstray()
                if str(status_code) == '429':

                    while_turn = True


                elif str(status_code) == '400' or str(status_code) == '403':
                    while_turn = False
                    login_error = True
                    break

                else:
                    while_turn = False
            except Exception as e:
                print('a10 hata',e)

                login_error = True
                while_turn = False

        print("a11")
        while_turn = True
        countof429 = 0
        while while_turn and login_error == False:

            try:
                if countof429 >= 10:
                    while_turn = False
                    break
                else:
                    countof429 += 1

                status_code = self.badge()
                if str(status_code) == '429':

                    while_turn = True


                elif str(status_code) == '400' or str(status_code) == '403':
                    while_turn = False
                    login_error = True
                    break

                else:
                    while_turn = False
            except Exception as e:
                print('a11 hata',e)

                login_error = True
                while_turn = False

        print("a12")
        while_turn = True
        countof429 = 0
        while while_turn and login_error == False:

            try:
                if countof429 >= 10:
                    while_turn = False
                    break
                else:
                    countof429 += 1

                status_code = self.banyan()
                if str(status_code) == '429':

                    while_turn = True


                elif str(status_code) == '400' or str(status_code) == '403':
                    while_turn = False
                    login_error = True
                    break

                else:
                    while_turn = False
            except Exception as e:
                print('a12 hata',e)
                login_error = True
                while_turn = False


        print("a13")
        while_turn = True
        countof429 = 0
        while while_turn and login_error == False:

            try:
                if countof429 >= 10:
                    while_turn = False
                    break
                else:
                    countof429 += 1

                status_code = self.aktivateson()
                if str(status_code) == '429':

                    while_turn = True


                elif str(status_code) == '400' or str(status_code) == '403':
                    while_turn = False
                    login_error = True
                    break

                else:
                    while_turn = False
            except Exception as e:
                login_error = True
                while_turn = False
        print("a14")
        while_turn = True
        countof429 = 0
        while while_turn and login_error == False:

            try:
                if countof429 >= 10:
                    while_turn = False
                    break
                else:
                    countof429 += 1

                status_code = self.loglarbaslangic4()
                if str(status_code) == '429':

                    while_turn = True


                elif str(status_code) == '400' or str(status_code) == '403':
                    while_turn = False
                    login_error = True
                    break

                else:
                    while_turn = False
            except Exception as e:
                login_error = True
                while_turn = False

        print("a SON")
        return True


    async def instagram_listener_worker(self):

        client = FBNSMQTTClient()
        print("7777777777", client)

        def on_fbns_auth(auth):
            print("a22222222222", auth)
            self.ck_data = auth
            self.ck = auth['ck']
            print(self.ck)
            self.cs = auth['cs']
            print(self.cs)
            self.sr = auth['sr']
            print(self.sr)
            self.di = auth['di']
            print(self.di)
            self.ds = auth['ds']
            print(self.ds)
            print('>>>>>>>> ')


        client.on_fbns_auth = on_fbns_auth
        print("11111", on_fbns_auth)

        await client.connect('mqtt-mini.facebook.com', 443, ssl=True, keepalive=5)


    def loginStart(self, login_after_ip_port_proxy, login_after_auth_proxy, login_ip_port_proxy, login_auth_proxy):

        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.instagram_listener_worker()) 
        loop.close()

        if login_after_ip_port_proxy and login_after_auth_proxy:
            self.login_after_proxy = self.set_proxy_ip_port(login_after_ip_port_proxy.proxy)
        elif login_after_ip_port_proxy:
            self.login_after_proxy = self.set_proxy_ip_port(login_after_ip_port_proxy.proxy)
        elif login_after_auth_proxy:
            self.login_after_proxy = self.set_proxy_auth(login_after_auth_proxy.proxy)
        else:
            self.login_after_proxy = None                

        if login_ip_port_proxy and login_auth_proxy:
            self.login_proxy = self.set_proxy_ip_port(login_ip_port_proxy.proxy)
        elif login_ip_port_proxy:
            self.login_proxy = self.set_proxy_ip_port(login_ip_port_proxy.proxy)
        elif login_auth_proxy:
            self.login_proxy = self.set_proxy_auth(login_auth_proxy.proxy)
        else:
            self.login_proxy = None   

        ### işlem başlangıç  ####
        login_error = False
        error_message = ''
        self.user_data = None

        print('işlemler başladı....')
        try:

            self.reCreate()
            print("a2")
            while_turn = True
            countof429 = 0
            while while_turn and login_error == False:

                try:
                    if countof429 >= 10:
                        while_turn = False
                        login_error = True
                        break
                    else:
                        countof429 += 1

                    status_code = self.SendRequestcookieal1()
                    if str(status_code) == '429':

                        while_turn = True
                        self.reCreate()


                    elif str(status_code) == '400' or str(status_code) == '403':
                        while_turn = False
                        login_error = True
                        break

                    else:
                        while_turn = False
                except Exception as e:
                    login_error = True
                    while_turn = False

      
            print("a3")

            while_turn = True
            countof429 = 0
            last_status_data = None
            while while_turn and login_error == False:

                try:
                    if countof429 >= 10:
                        while_turn = False
                        login_error = True
                        break
                    else:
                        countof429 += 1

                    status_data = self.mobillogin()
                    last_status_data = status_data
                    print(status_data)
                    if str(status_data['status_code']) == '429':

                        while_turn = True

                    elif str(status_data['status_code']) == '400' or str(status_data['status_code']) == '403':
                        while_turn = False
                        login_error = True
                        break

                    else:
                        while_turn = False
                except Exception as e:
                    login_error = True
                    while_turn = False




            print("a4")
            while_turn = True
            countof429 = 0
            while while_turn and login_error == False:

                try:
                    if countof429 >= 10:
                        while_turn = False
                        login_error = True
                        break
                    else:
                        countof429 += 1

                    status_code = self.yenitoken1()
                    if str(status_code) == '429':

                        while_turn = True
                        self.reCreate()


                    elif str(status_code) == '400' or str(status_code) == '403':
                        while_turn = False
                        login_error = True
                        break

                    else:
                        while_turn = False
                except Exception as e:
                    login_error = True
                    while_turn = False


            print("a5")
            while_turn = True
            countof429 = 0
            while while_turn and login_error == False:

                try:
                    if countof429 >= 10:
                        while_turn = False
                        login_error = True
                        break
                    else:
                        countof429 += 1

                    status_code = self.launcher1c()
                    if str(status_code) == '429':

                        while_turn = True
                        self.reCreate()


                    elif str(status_code) == '400' or str(status_code) == '403':
                        while_turn = False
                        login_error = True
                        break

                    else:
                        while_turn = False
                except Exception as e:
                    login_error = True
                    while_turn = False



            print("a6")
            while_turn = True
            countof429 = 0
            while while_turn and login_error == False:

                try:
                    if countof429 >= 10:
                        while_turn = False
                        login_error = True
                        break
                    else:
                        countof429 += 1

                    status_code = self.account_family()
                    if str(status_code) == '429':

                        while_turn = True
                        self.reCreate()


                    elif str(status_code) == '400' or str(status_code) == '403':
                        while_turn = False
                        login_error = True
                        break

                    else:
                        while_turn = False
                except Exception as e:
                    login_error = True
                    while_turn = False

            print("a7")
            while_turn = True
            countof429 = 0
            while while_turn and login_error == False:

                try:
                    if countof429 >= 10:
                        while_turn = False
                        login_error = True
                        break
                    else:
                        countof429 += 1
                    self.user_data = self.infowho1()

                    if str(status_code) == '429':
                        while_turn = True

                    elif str(status_code) == '400' or str(status_code) == '403':
                        while_turn = False
                        login_error = True
                        break

                    else:
                        while_turn = False
                except Exception as e:
                    login_error = True
                    while_turn = False
            print("a14")

            status_data = last_status_data
            return {'user_data': self.user_data, 'status_code': status_data['status_code'],
                    'status5': status_data['status5'], 'login_error': login_error, 'userid': self.userid,
                    'authorization': self.authorization, 'claim': self.claim, 'pigeonid': self.pigeonid,
                    'phoneid': self.phoneid, 'waterfallid': self.waterfall_id, 'deviceid': self.deviceid,
                    'androidid': self.androidid, 'rur': self.rur,
                    'user_agent': self.USER_AGENT, 'mid': self.mid, 'checksum': self.checksum, 'adid': self.adid,
                    'guid': self.guid, 'user_agent_compile': self.user_agent_compile(self.USER_AGENT)}

        except Exception as e:
            print(e)
            
            return {'user_data':self.user_data,'status_code':status_data['status_code'],'status5':status_data['status5'],'login_error':login_error,'userid':self.userid,'authorization':self.authorization,'claim':self.claim,'pigeonid':self.pigeonid,
                'phoneid':self.phoneid,'waterfallid':self.waterfall_id,'deviceid':self.deviceid,'guid':self.guid,'adid':self.adid,'androidid':self.androidid,'rur':self.rur,
                'user_agent':self.USER_AGENT,'mid':self.mid,'checksum':self.checksum,'user_agent_compile':self.user_agent_compile(self.USER_AGENT)}




    ### yeniler ##




    def reelstray(self):

        try:

            data = 'supported_capabilities_new=%5B%7B%22name%22%3A%22SUPPORTED_SDK_VERSIONS%22%2C%22value%22%3A%22108.0%2C109.0%2C110.0%2C111.0%2C112.0%2C113.0%2C114.0%2C115.0%2C116.0%2C117.0%2C118.0%2C119.0%2C120.0%2C121.0%2C122.0%2C123.0%2C124.0%2C125.0%2C126.0%22%7D%2C%7B%22name%22%3A%22FACE_TRACKER_VERSION%22%2C%22value%22%3A%2214%22%7D%2C%7B%22name%22%3A%22segmentation%22%2C%22value%22%3A%22segmentation_enabled%22%7D%2C%7B%22name%22%3A%22COMPRESSION%22%2C%22value%22%3A%22ETC2_COMPRESSION%22%7D%2C%7B%22name%22%3A%22world_tracker%22%2C%22value%22%3A%22world_tracker_enabled%22%7D%2C%7B%22name%22%3A%22gyroscope%22%2C%22value%22%3A%22gyroscope_enabled%22%7D%5D&reason=cold_start&timezone_offset=3600&tray_session_id=' + self.generateUUID(
                True) + '&request_id=' + self.generateUUID(True) + '&_uuid=' + self.guid + '&page_size=50'

            status = self.SendRequestreeltray(data)
        except Exception as e:
            self.reelstray()
            pass

        return status




    def SendRequestreeltray(self, post=None):

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
        response2 = requests.post('https://i.instagram.com/api/v1/feed/reels_tray/', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("reeltray Status: ", response2.status_code)
        #print("timeline Status5: ", response2.json())
        # print("Status5: ", response2.headers)
        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            #print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            #print('shbts: ', self.shbts)
        except Exception as e:
            self.shbid = None
            #print('shbid: ', self.shbid)

            self.shbts = None
            #print('shbts: ', self.shbts)

            pass
        return {'status_code': response2.status_code, 'status5': response2.json()}




    def feedtimeline(self):
    
        try:
            data = 'feed_view_info=%5B%5D&reason=cold_start_fetch&timezone_offset=3600&device_id=' + self.deviceid + '&request_id=' + self.generateUUID(
                True) + '&is_pull_to_refresh=0&_uuid=' + self.guid + '&session_id=' + self.generateUUID(
                True) + '&bloks_versioning_id=' + self.BloksVersionId

            status = self.SendRequestfeedtime(data)
        except Exception as e:
            self.feedtimeline()
            pass

        return status


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
        response2 = requests.post('https://i.instagram.com/api/v1/feed/timeline/', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("feedtime Status: ", response2.status_code)
        #print("timeline Status5: ", response2.json())
        # print("Status5: ", response2.headers)
        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            #print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            #print('shbts: ', self.shbts)
        except Exception as e:
            self.shbid = None
            #print('shbid: ', self.shbid)

            self.shbts = None
            #print('shbts: ', self.shbts)

            pass
        return {'status_code': response2.status_code, 'status5': response2.json()}





    def feeduser1(self):

        try:

            urlm = 'feed/user/' + self.userid + '/?exclude_comment=true&only_fetch_first_carousel_media=false'

            status = self.SendRequestloginsonrasitoplu2get(urlm)
        except Exception as e:
            self.feeduser1()
            pass

        return status

    def highlights1(self):

        try:

            urlm = 'highlights/' + self.userid + '/highlights_tray/?supported_capabilities_new=%5B%7B%22name%22%3A%22SUPPORTED_SDK_VERSIONS%22%2C%22value%22%3A%2290.0%2C91.0%2C92.0%2C93.0%2C94.0%2C95.0%2C96.0%2C97.0%2C98.0%2C99.0%2C100.0%2C101.0%2C102.0%2C103.0%2C104.0%2C105.0%2C106.0%2C107.0%2C108.0%2C109.0%2C110.0%2C111.0%2C112.0%2C113.0%22%7D%2C%7B%22name%22%3A%22FACE_TRACKER_VERSION%22%2C%22value%22%3A%2214%22%7D%2C%7B%22name%22%3A%22COMPRESSION%22%2C%22value%22%3A%22PVR_COMPRESSION%22%7D%2C%7B%22name%22%3A%22COMPRESSION%22%2C%22value%22%3A%22ETC2_COMPRESSION%22%7D%2C%7B%22name%22%3A%22world_tracker%22%2C%22value%22%3A%22world_tracker_enabled%22%7D%5D&' + 'phone_id=' + self.phoneid + '&battery_level=' + str(
                random.randint(10, 99)) + '&is_charging=0&is_dark_mode=0&will_sound_on=0'

            status = self.SendRequestloginsonrasitoplu2get(urlm)
        except Exception as e:
            self.highlights1()
            pass

        return status

    def infom1(self):

        try:

            urlm = 'users/' + self.userid + '/info/'

            status = self.SendRequestloginsonrasitoplu2get(urlm)
        except Exception as e:
            self.infom1()
            pass

        return status

    def sync1a(self):

        try:

            alfason = {
                "id": self.deviceid,
                "server_config_retrieval": "1",
                "experiments": "ig_android_device_detection_info_upload,ig_android_gmail_oauth_in_reg,ig_android_device_info_foreground_reporting,ig_android_device_verification_fb_signup,ig_android_passwordless_account_password_creation_universe,ig_growth_android_profile_pic_prefill_with_fb_pic_2,ig_account_identity_logged_out_signals_global_holdout_universe,ig_android_quickcapture_keep_screen_on,ig_android_device_based_country_verification,ig_android_login_identifier_fuzzy_match,ig_android_reg_modularization_universe,ig_android_security_intent_switchoff,ig_android_device_verification_separate_endpoint,ig_android_suma_landing_page,ig_android_sim_info_upload,ig_android_fb_account_linking_sampling_freq_universe,ig_android_retry_create_account_universe,ig_android_caption_typeahead_fix_on_o_universe"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestsync1a(signature18)
        except Exception as e:
            self.sync1a()
            pass

        return status

    def sync1b(self):

        try:

            alfason = {
                "id": self.deviceid,
                "server_config_retrieval": "1",
                "experiments": "ig_android_device_detection_info_upload,ig_android_gmail_oauth_in_reg,ig_android_device_info_foreground_reporting,ig_android_device_verification_fb_signup,ig_android_passwordless_account_password_creation_universe,ig_growth_android_profile_pic_prefill_with_fb_pic_2,ig_account_identity_logged_out_signals_global_holdout_universe,ig_android_quickcapture_keep_screen_on,ig_android_device_based_country_verification,ig_android_login_identifier_fuzzy_match,ig_android_reg_modularization_universe,ig_android_security_intent_switchoff,ig_android_device_verification_separate_endpoint,ig_android_suma_landing_page,ig_android_sim_info_upload,ig_android_fb_account_linking_sampling_freq_universe,ig_android_retry_create_account_universe,ig_android_caption_typeahead_fix_on_o_universe"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestsync1b(signature18)
        except Exception as e:
            self.sync1b()
            pass

        return status

    def sync1c(self):

        try:

            alfason = {
                "id": self.userid,
                "_uid": self.userid,
                "_uuid": self.guid,
                "server_config_retrieval": "1",
                "experiments": "ig_android_video_raven_streaming_upload_universe,ig_android_vc_explicit_intent_for_notification,ig_stories_ads_delivery_rules,ig_shopping_checkout_improvements_universe,ig_business_new_value_prop_universe,ig_android_suggested_users_background,ig_android_stories_music_search_typeahead,ig_android_direct_mutation_manager_media_3,ig_android_shopping_bag_null_state_v1,ig_camera_android_feed_effect_attribution_universe,ig_android_test_not_signing_address_book_unlink_endpoint,ig_android_stories_share_extension_video_segmentation,ig_android_search_nearby_places_universe,ig_android_vc_migrate_to_bluetooth_v2_universe,ig_ei_option_setting_universe,instagram_ns_qp_prefetch_universe,ig_android_camera_leak,ig_android_separate_empty_feed_su_universe,ig_stories_rainbow_ring,ig_android_zero_rating_carrier_signal,ig_explore_2019_h1_destination_cover,ig_android_explore_recyclerview_universe,ig_android_whats_app_contact_invite_universe,ig_android_direct_add_member_dialog_universe,ig_android_xposting_reel_memory_share_universe,ig_android_viewpoint_stories_public_testing,ig_android_photo_creation_large_width,ig_android_save_all,ig_android_video_upload_hevc_encoding_universe,instagram_shopping_hero_carousel_visual_variant_consolidation,ig_android_vc_face_effects_universe,ig_android_fbpage_on_profile_side_tray,ig_android_igtv_refresh_tv_guide_interval,ig_android_recyclerview_binder_group_enabled_universe,ig_android_video_exoplayer_2,ig_rn_branded_content_settings_approval_on_select_save,ig_android_account_insights_shopping_content_universe,ig_branded_content_tagging_approval_request_flow_brand_side_v2,ig_android_render_thread_memory_leak_holdout,ig_threads_clear_notifications_on_has_seen,ig_android_xposting_dual_destination_shortcut_fix,ig_android_show_create_content_pages_universe,ig_android_disk_usage_logging_universe,ig_android_stories_blacklist,ig_payments_billing_address,ig_android_fs_new_gallery_hashtag_prompts,ig_android_video_product_specific_abr,ig_android_sidecar_segmented_streaming_universe,ig_android_xposting_feed_to_stories_reshares_universe,ig_android_stories_layout_universe,ig_emoji_render_counter_logging_universe,ig_android_vc_cpu_overuse_universe,ig_android_invite_list_button_redesign_universe,ig_android_react_native_email_sms_settings_universe,ig_android_enable_zero_rating,ig_android_direct_leave_from_group_message_requests,ig_android_publisher_stories_migration,aymt_instagram_promote_flow_abandonment_ig_universe,ig_android_whitehat_options_universe,ig_android_stories_context_sheets_universe,ig_android_stories_vpvd_container_module_fix,instagram_android_profile_follow_cta_context_feed,ig_android_personal_user_xposting_destination_fix,ig_android_stories_boomerang_v2_universe,ig_android_direct_message_follow_button,ig_android_video_raven_passthrough,ig_android_vc_cowatch_universe,ig_shopping_insights_wc_copy_update_android,ig_stories_ads_media_based_insertion,ig_android_wellbeing_timeinapp_v1_universe,ig_android_feed_ads_ppr_universe,ig_android_igtv_browse_long_press,ig_xposting_mention_reshare_stories,ig_threads_sanity_check_thread_viewkeys,ig_android_vc_shareable_moments_universe,ig_android_igtv_stories_preview,ig_android_shopping_product_metadata_on_product_tiles_universe,ig_android_stories_quick_react_gif_universe,ig_android_video_qp_logger_universe,ig_android_stories_weblink_creation,ig_android_frx_highlight_cover_reporting_qe,ig_android_vc_capture_universe,ig_android_optic_face_detection,ig_android_save_to_collections_flow,ig_android_direct_segmented_video,ig_android_stories_video_prefetch_kb,ig_android_direct_mark_as_read_notif_action,ig_android_product_breakdown_post_insights,ig_inventory_connections,ig_android_canvas_cookie_universe,ig_android_video_streaming_upload_universe,ig_android_smplt_universe,ig_cameracore_android_new_optic_camera2,ig_android_partial_share_sheet,ig_android_fbc_upsell_on_dp_first_load,ig_android_stories_sundial_creation_universe,ig_android_music_story_fb_crosspost_universe,ig_android_payments_growth_promote_payments_in_payments,ig_carousel_bumped_organic_impression_client_universe,ig_android_business_attribute_sync,ig_biz_post_approval_nux_universe,ig_camera_android_bg_processor,ig_android_ig_personal_account_to_fb_page_linkage_backfill,ig_android_ad_stories_scroll_perf_universe,ig_android_persistent_nux,ig_android_tango_cpu_overuse_universe,ig_android_direct_wellbeing_message_reachability_settings,ig_android_edit_location_page_info,ig_android_unfollow_from_main_feed_v2,ig_android_stories_project_eclipse,ig_direct_android_bubble_system,ig_android_li_session_chaining,ig_android_create_mode_memories_see_all,ig_android_feed_post_warning_universe,ig_mprotect_code_universe,ig_android_video_visual_quality_score_based_abr,ig_explore_2018_post_chaining_account_recs_dedupe_universe,ig_android_view_info_universe,ig_android_camera_upsell_dialog,ig_android_business_transaction_in_stories_consumer,ig_android_dead_code_detection,ig_android_stories_video_seeking_audio_bug_fix,ig_android_qp_kill_switch,ig_android_new_follower_removal_universe,ig_android_feed_post_sticker,ig_android_business_cross_post_with_biz_id_infra,ig_android_inline_editing_local_prefill,ig_android_reel_tray_item_impression_logging_viewpoint,ig_android_video_abr_universe,ig_android_vc_cowatch_media_share_universe,ig_challenge_general_v2,ig_android_place_signature_universe,ig_android_direct_inbox_cache_universe,ig_android_business_promote_tooltip,ig_android_wellbeing_support_frx_hashtags_reporting,ig_camera_android_facetracker_v12_universe,igqe_pending_tagged_posts,ig_sim_api_analytics_reporting,ig_android_interest_follows_universe,ig_android_direct_view_more_qe,ig_android_audience_control,ig_android_memory_use_logging_universe,ig_android_igtv_whitelisted_for_web,ig_rti_inapp_notifications_universe,ig_android_share_publish_page_universe,ig_direct_max_participants,ig_commerce_platform_ptx_bloks_universe,ig_android_video_raven_bitrate_ladder_universe,ig_android_recipient_picker,ig_android_graphql_survey_new_proxy_universe,ig_android_music_browser_redesign,ig_android_disable_manual_retries,ig_android_qr_code_nametag,ig_android_purx_native_checkout_universe,ig_android_fs_creation_flow_tweaks,ig_android_apr_lazy_build_request_infra,ig_android_business_transaction_in_stories_creator,ig_cameracore_android_new_optic_camera2_galaxy,ig_android_branded_content_appeal_states,ig_android_claim_location_page,ig_android_location_integrity_universe,ig_video_experimental_encoding_consumption_universe,ig_android_biz_story_to_fb_page_improvement,ig_shopping_checkout_improvements_v2_universe,ig_android_create_mode_tap_to_cycle,ig_android_fb_profile_integration_universe,ig_android_shopping_bag_optimization_universe,ig_android_create_page_on_top_universe,android_ig_cameracore_aspect_ratio_fix,ig_android_skip_button_content_on_connect_fb_universe,ig_android_igtv_explore2x2_viewer,ig_android_network_perf_qpl_ppr,ig_android_insights_post_dismiss_button,ig_xposting_biz_feed_to_story_reshare,ig_android_user_url_deeplink_fbpage_endpoint,ig_android_comment_warning_non_english_universe,ig_android_stories_question_sticker_music_format,ig_promote_interactive_poll_sticker_igid_universe,ig_android_feed_cache_update,ig_pacing_overriding_universe,ig_explore_reel_ring_universe,ig_android_igtv_pip,ig_android_wishlist_reconsideration_universe,ig_android_sso_use_trustedapp_universe,ig_android_stories_music_lyrics,ig_android_camera_formats_ranking_universe,ig_android_stories_music_awareness_universe,ig_explore_2019_h1_video_autoplay_resume,ig_android_video_upload_quality_qe1,ig_android_country_code_fix_universe,ig_android_stories_music_overlay,ig_android_emoji_util_universe_3,ig_android_shopping_pdp_post_purchase_sharing,ig_branded_content_settings_unsaved_changes_dialog,ig_android_realtime_mqtt_logging,ig_android_rainbow_hashtags,ig_android_create_mode_templates,ig_android_direct_block_from_group_message_requests,ig_android_live_subscribe_user_level_universe,ig_android_video_call_finish_universe,ig_android_viewpoint_occlusion,ig_android_logged_in_delta_migration,ig_android_push_reliability_universe,ig_android_self_story_button_non_fbc_accounts,ig_android_explore_discover_people_entry_point_universe,ig_android_live_webrtc_livewith_params,ig_camera_android_effect_metadata_cache_refresh_universe,ig_android_appstate_logger,ig_prefetch_scheduler_backtest,ig_android_ads_data_preferences_universe,ig_payment_checkout_cvv,ig_android_vc_background_call_toast_universe,ig_android_fb_link_ui_polish_universe,ig_android_qr_code_scanner,ig_disable_fsync_universe,mi_viewpoint_viewability_universe,ig_android_live_egl10_compat,ig_android_video_upload_transform_matrix_fix_universe,ig_android_fb_url_universe,ig_android_reel_raven_video_segmented_upload_universe,ig_android_fb_sync_options_universe,ig_android_recommend_accounts_destination_routing_fix,ig_android_enable_automated_instruction_text_ar,ig_traffic_routing_universe,ig_stories_allow_camera_actions_while_recording,ig_shopping_checkout_mvp_experiment,ig_android_video_fit_scale_type_igtv,ig_android_igtv_player_follow_button,ig_android_arengine_remote_scripting_universe,ig_android_page_claim_deeplink_qe,ig_android_logging_metric_universe_v2,ig_android_xposting_newly_fbc_people,ig_android_recognition_tracking_thread_prority_universe,ig_android_contact_point_upload_rate_limit_killswitch,ig_android_optic_photo_cropping_fixes,ig_android_sso_kototoro_app_universe,ig_android_profile_thumbnail_impression,ig_camera_android_share_effect_link_universe,ig_android_igtv_autoplay_on_prepare,ig_android_ads_rendering_logging,ig_shopping_size_selector_redesign,ig_android_image_exif_metadata_ar_effect_id_universe,ig_android_optic_new_architecture,ig_android_external_gallery_import_affordance,ig_search_hashtag_content_advisory_remove_snooze,ig_android_on_notification_cleared_async_universe,ig_payment_checkout_info"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestsync2a(signature18)
        except Exception as e:
            self.sync1c()
            pass

        return status



    def ig_steps(self):
    
        try:

            status = self.SendRequestaccountig_steps()

        except Exception as e:
            self.SendRequestaccountig_steps()
            pass

        return status



    def badge(self):
    
        try:

            data = 'phone_id=' + self.phoneid + '&user_ids=' + self.userid + '&device_id=' + self.deviceid + '&_uuid=' + self.guid

            status = self.SendRequestbadge(data)
        except Exception as e:
            self.badge()
            pass

        return status



    def SendRequestbadge(self, post=None):

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
        response2 = requests.post('https://i.instagram.com/api/v1/notifications/badge/', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("badge Status: ", response2.status_code)
        #print("timeline Status5: ", response2.json())
        # print("Status5: ", response2.headers)
        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            #print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            #print('shbts: ', self.shbts)
        except Exception as e:
            self.shbid = None
            #print('shbid: ', self.shbid)

            self.shbts = None
            #print('shbts: ', self.shbts)

            pass
        return {'status_code': response2.status_code, 'status5': response2.json()}



    def launcher1a(self):

        try:

            alfason = {
                "id": self.deviceid,
                "server_config_retrieval": "1"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestlaunch(signature18)
        except Exception as e:
            self.launcher1a()
            pass

        return status

    def launcher1b(self):

        try:

            alfason = {
                "id": self.deviceid,
                "server_config_retrieval": "1"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestlaunch1b(signature18)
        except Exception as e:
            self.launcher1b()
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
            self.launcher1c()
            pass

        return status

    def contact_point_prefill1a(self):

        try:

            alfason = {
                "phone_id":self.phoneid,
                "usage":"prefill"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            #print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            #print(signature18)

            status = self.SendRequestgetprefill1a(signature18)
        except Exception as e:
            self.contact_point_prefill1a()
            pass

        return status

    def log1(self):

        try:

            alfa = {
                "seq": 1,
                "app_id": "567067343352427",
                "app_ver": self.appver,
                "build_num": "289692181",
                "device_id": self.deviceid,
                "family_device_id": "",
                "session_id": self.session_id,
                "channel": "zero_latency",
                "app_uid": "0",
                "config_version": "v2",
                "config_checksum": "",
                "data": [
                    {
                        "name": "ig_emergency_push_did_set_initial_version",
                        "time": self.timestamp1(True),
                        "sampling_rate": 1,
                        "extra": {
                            "current_version": 46,
                            "pk": "0",
                            "release_channel": "prod",
                            "radio_type": "wifi-none"
                        }
                    }
                ],
                "log_type": "client_event"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfa))
            # print("aaaaa", ddd80)

            alfason = 'access_token=' + '567067343352427' + '|' + 'f249176f09e26ce54212b472dbab8fa8' + '&format=json&compressed=' + '0' + '&sent_time=' + self.timestamp1(
                True) + '&message=' + ddd80

            data = alfason

            status = self.SendRequestlog1(data)
        except Exception as e:
            self.log1()
            pass

        return status

    def pwdsifreleme(self):

        self.timeson114 = str(int(datetime.now().timestamp()))

        data2 = {"id": self.deviceid,
                 "server_config_retrieval": "1",
                 "experiments": "ig_android_device_detection_info_upload,ig_android_gmail_oauth_in_reg,ig_android_device_info_foreground_reporting,ig_android_device_verification_fb_signup,ig_android_passwordless_account_password_creation_universe,ig_growth_android_profile_pic_prefill_with_fb_pic_2,ig_account_identity_logged_out_signals_global_holdout_universe,ig_android_quickcapture_keep_screen_on,ig_android_device_based_country_verification,ig_android_login_identifier_fuzzy_match,ig_android_reg_modularization_universe,ig_android_security_intent_switchoff,ig_android_device_verification_separate_endpoint,ig_android_suma_landing_page,ig_android_sim_info_upload,ig_android_fb_account_linking_sampling_freq_universe,ig_android_retry_create_account_universe,ig_android_caption_typeahead_fix_on_o_universe"
                 }

        self.SendRequest2pwd('qe/sync/', self.generateSignature(json.dumps(data2)))
        data10 = self.HeadersJsona2
        # print(data9a)
        publickeyid = int(data10['ig-set-password-encryption-key-id'])
        # print("keyidson",publickeyid)
        publickey = data10['ig-set-password-encryption-pub-key']

        self.pub_key = publickey
        # print("publickeyson",publickey)

        ############################# ENCPASY ŞİFRE ÜRETME KISMI ####################################

        key_id = publickeyid
        pub_key = publickey
        password = self.password
        time = self.timeson114

        data = {
            'time': time,
            'password': password,
            'pubkey': pub_key,
            'keyid': key_id,
        }
        response = requests.post('http://argeelektrik.com/insta/mobilpwd.php', data=data, verify=True,
                                 proxies=self.login_after_proxy, timeout=15)

        atim = response.text

        self.PASL = atim
        # print(self.PASL)
        return response.status_code

    def launcher(self):

        try:

            alfason = {
                "id": self.deviceid,
                "server_config_retrieval": "1"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestlaunch(signature18)
        except Exception as e:
            self.launcher()
            pass

        return status

    def getprefill(self):

        try:

            alfason = {
                "android_device_id": self.androidid,
                "phone_id": self.phoneid,
                "usages": "[\"account_recovery_omnibox\"]",
                "device_id": self.deviceid
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestgetprefill(signature18)
        except Exception as e:
            self.getprefill()
            pass

        return status

    def attribution(self):

        try:

            alfason = {

                "adid": self.adid

            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestattribution(signature18)
        except Exception as e:
            self.attribution()
            pass


        return status

    def mobillogin(self):

       #self.pwdsifreleme()


        self.timeson114 = str(int(datetime.now().timestamp()))


        try:

            alfason = {
                "jazoest": "22379",
                "country_codes": "[{\"country_code\":\"90\",\"source\":[\"default\"]}]",
                "phone_id": self.phoneid,
                "enc_password": "#PWD_INSTAGRAM:0:" + self.timeson114 + ":" + self.password, #self.PASL
                "username": self.username,
                "adid": self.adid,
                "guid": self.guid,
                "device_id": self.androidid,
                "google_tokens": "[]",
                "login_attempt_count": "0"
            }


            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            status = self.SendRequestlogin(signature18)

        except Exception as e:
            print(e)
            self.mobillogin()
            pass

        return status



    def banyan(self):
    
        try:

            link = 'https://i.instagram.com/api/v1/banyan/banyan/?views=%5B%22call_recipients%22%2C%22reshare_share_sheet%22%2C%22direct_user_search_keypressed%22%2C%22direct_inbox_active_now%22%2C%22story_share_sheet%22%2C%22forwarding_recipient_sheet%22%2C%22direct_user_search_nullstate%22%2C%22threads_people_picker%22%5D'
            status = self.SendRequestbanyan(link)
        except Exception as e:
            self.banyan()
            pass

        return status



    def SendRequestbanyan(self, endpoint=None):

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
        response2 = requests.get(endpoint, headers=headers,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("banyan Status: ", response2.status_code)
        #print("timeline Status5: ", response2.json())
        # print("Status5: ", response2.headers)
        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            #print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            #print('shbts: ', self.shbts)
        except Exception as e:
            self.shbid = None
            #print('shbid: ', self.shbid)

            self.shbts = None
            #print('shbts: ', self.shbts)

            pass
        return {'status_code': response2.status_code, 'status5': response2.json()}



    def yenitoken1(self):
    
        try:

            status = self.SendRequesttoken1()

        except Exception as e:
            print("tttt: ", e)
            self.yenitoken1()
            pass

        return status

    def account_family(self):

        try:

            status = self.SendRequestaccountfamily()

        except Exception as e:
            self.account_family()
            pass

        return status

    def sync1(self):

        try:

            alfason = {
                "id": self.userid,
                "_uid": self.userid,
                "_uuid": self.guid,
                "server_config_retrieval": "1",
                "experiments": "ig_android_video_raven_streaming_upload_universe,ig_android_vc_explicit_intent_for_notification,ig_stories_ads_delivery_rules,ig_shopping_checkout_improvements_universe,ig_business_new_value_prop_universe,ig_android_suggested_users_background,ig_android_stories_music_search_typeahead,ig_android_direct_mutation_manager_media_3,ig_android_shopping_bag_""_state_v1,ig_camera_android_feed_effect_attribution_universe,ig_android_test_not_signing_address_book_unlink_endpoint,ig_android_stories_share_extension_video_segmentation,ig_android_search_nearby_places_universe,ig_android_vc_migrate_to_bluetooth_v2_universe,ig_ei_option_setting_universe,instagram_ns_qp_prefetch_universe,ig_android_camera_leak,ig_android_separate_empty_feed_su_universe,ig_stories_rainbow_ring,ig_android_zero_rating_carrier_signal,ig_explore_2019_h1_destination_cover,ig_android_explore_recyclerview_universe,ig_android_whats_app_contact_invite_universe,ig_android_direct_add_member_dialog_universe,ig_android_xposting_reel_memory_share_universe,ig_android_viewpoint_stories_public_testing,ig_android_photo_creation_large_width,ig_android_save_all,ig_android_video_upload_hevc_encoding_universe,instagram_shopping_hero_carousel_visual_variant_consolidation,ig_android_vc_face_effects_universe,ig_android_fbpage_on_profile_side_tray,ig_android_igtv_refresh_tv_guide_interval,ig_android_recyclerview_binder_group_enabled_universe,ig_android_video_exoplayer_2,ig_rn_branded_content_settings_approval_on_select_save,ig_android_account_insights_shopping_content_universe,ig_branded_content_tagging_approval_request_flow_brand_side_v2,ig_android_render_thread_memory_leak_holdout,ig_threads_clear_notifications_on_has_seen,ig_android_xposting_dual_destination_shortcut_fix,ig_android_show_create_content_pages_universe,ig_android_disk_usage_logging_universe,ig_android_stories_blacklist,ig_payments_billing_address,ig_android_fs_new_gallery_hashtag_prompts,ig_android_video_product_specific_abr,ig_android_sidecar_segmented_streaming_universe,ig_android_xposting_feed_to_stories_reshares_universe,ig_android_stories_layout_universe,ig_emoji_render_counter_logging_universe,ig_android_vc_cpu_overuse_universe,ig_android_invite_list_button_redesign_universe,ig_android_react_native_email_sms_settings_universe,ig_android_enable_zero_rating,ig_android_direct_leave_from_group_message_requests,ig_android_publisher_stories_migration,aymt_instagram_promote_flow_abandonment_ig_universe,ig_android_whitehat_options_universe,ig_android_stories_context_sheets_universe,ig_android_stories_vpvd_container_module_fix,instagram_android_profile_follow_cta_context_feed,ig_android_personal_user_xposting_destination_fix,ig_android_stories_boomerang_v2_universe,ig_android_direct_message_follow_button,ig_android_video_raven_passthrough,ig_android_vc_cowatch_universe,ig_shopping_insights_wc_copy_update_android,ig_stories_ads_media_based_insertion,ig_android_wellbeing_timeinapp_v1_universe,ig_android_feed_ads_ppr_universe,ig_android_igtv_browse_long_press,ig_xposting_mention_reshare_stories,ig_threads_sanity_check_thread_viewkeys,ig_android_vc_shareable_moments_universe,ig_android_igtv_stories_preview,ig_android_shopping_product_metadata_on_product_tiles_universe,ig_android_stories_quick_react_gif_universe,ig_android_video_qp_logger_universe,ig_android_stories_weblink_creation,ig_android_frx_highlight_cover_reporting_qe,ig_android_vc_capture_universe,ig_android_optic_face_detection,ig_android_save_to_collections_flow,ig_android_direct_segmented_video,ig_android_stories_video_prefetch_kb,ig_android_direct_mark_as_read_notif_action,ig_android_product_breakdown_post_insights,ig_inventory_connections,ig_android_canvas_cookie_universe,ig_android_video_streaming_upload_universe,ig_android_smplt_universe,ig_cameracore_android_new_optic_camera2,ig_android_partial_share_sheet,ig_android_fbc_upsell_on_dp_first_load,ig_android_stories_sundial_creation_universe,ig_android_music_story_fb_crosspost_universe,ig_android_payments_growth_promote_payments_in_payments,ig_carousel_bumped_organic_impression_client_universe,ig_android_business_attribute_sync,ig_biz_post_approval_nux_universe,ig_camera_android_bg_processor,ig_android_ig_personal_account_to_fb_page_linkage_backfill,ig_android_ad_stories_scroll_perf_universe,ig_android_persistent_nux,ig_android_tango_cpu_overuse_universe,ig_android_direct_wellbeing_message_reachability_settings,ig_android_edit_location_page_info,ig_android_unfollow_from_main_feed_v2,ig_android_stories_project_eclipse,ig_direct_android_bubble_system,ig_android_li_session_chaining,ig_android_create_mode_memories_see_all,ig_android_feed_post_warning_universe,ig_mprotect_code_universe,ig_android_video_visual_quality_score_based_abr,ig_explore_2018_post_chaining_account_recs_dedupe_universe,ig_android_view_info_universe,ig_android_camera_upsell_dialog,ig_android_business_transaction_in_stories_consumer,ig_android_dead_code_detection,ig_android_stories_video_seeking_audio_bug_fix,ig_android_qp_kill_switch,ig_android_new_follower_removal_universe,ig_android_feed_post_sticker,ig_android_business_cross_post_with_biz_id_infra,ig_android_inline_editing_local_prefill,ig_android_reel_tray_item_impression_logging_viewpoint,ig_android_video_abr_universe,ig_android_vc_cowatch_media_share_universe,ig_challenge_general_v2,ig_android_place_signature_universe,ig_android_direct_inbox_cache_universe,ig_android_business_promote_tooltip,ig_android_wellbeing_support_frx_hashtags_reporting,ig_camera_android_facetracker_v12_universe,igqe_pending_tagged_posts,ig_sim_api_analytics_reporting,ig_android_interest_follows_universe,ig_android_direct_view_more_qe,ig_android_audience_control,ig_android_memory_use_logging_universe,ig_android_igtv_whitelisted_for_web,ig_rti_inapp_notifications_universe,ig_android_share_publish_page_universe,ig_direct_max_participants,ig_commerce_platform_ptx_bloks_universe,ig_android_video_raven_bitrate_ladder_universe,ig_android_recipient_picker,ig_android_graphql_survey_new_proxy_universe,ig_android_music_browser_redesign,ig_android_disable_manual_retries,ig_android_qr_code_nametag,ig_android_purx_native_checkout_universe,ig_android_fs_creation_flow_tweaks,ig_android_apr_lazy_build_request_infra,ig_android_business_transaction_in_stories_creator,ig_cameracore_android_new_optic_camera2_galaxy,ig_android_branded_content_appeal_states,ig_android_claim_location_page,ig_android_location_integrity_universe,ig_video_experimental_encoding_consumption_universe,ig_android_biz_story_to_fb_page_improvement,ig_shopping_checkout_improvements_v2_universe,ig_android_create_mode_tap_to_cycle,ig_android_fb_profile_integration_universe,ig_android_shopping_bag_optimization_universe,ig_android_create_page_on_top_universe,android_ig_cameracore_aspect_ratio_fix,ig_android_skip_button_content_on_connect_fb_universe,ig_android_igtv_explore2x2_viewer,ig_android_network_perf_qpl_ppr,ig_android_insights_post_dismiss_button,ig_xposting_biz_feed_to_story_reshare,ig_android_user_url_deeplink_fbpage_endpoint,ig_android_comment_warning_non_english_universe,ig_android_stories_question_sticker_music_format,ig_promote_interactive_poll_sticker_igid_universe,ig_android_feed_cache_update,ig_pacing_overriding_universe,ig_explore_reel_ring_universe,ig_android_igtv_pip,ig_android_wishlist_reconsideration_universe,ig_android_sso_use_trustedapp_universe,ig_android_stories_music_lyrics,ig_android_camera_formats_ranking_universe,ig_android_stories_music_awareness_universe,ig_explore_2019_h1_video_autoplay_resume,ig_android_video_upload_quality_qe1,ig_android_country_code_fix_universe,ig_android_stories_music_overlay,ig_android_emoji_util_universe_3,ig_android_shopping_pdp_post_purchase_sharing,ig_branded_content_settings_unsaved_changes_dialog,ig_android_realtime_mqtt_logging,ig_android_rainbow_hashtags,ig_android_create_mode_templates,ig_android_direct_block_from_group_message_requests,ig_android_live_subscribe_user_level_universe,ig_android_video_call_finish_universe,ig_android_viewpoint_occlusion,ig_android_logged_in_delta_migration,ig_android_push_reliability_universe,ig_android_self_story_button_non_fbc_accounts,ig_android_explore_discover_people_entry_point_universe,ig_android_live_webrtc_livewith_params,ig_camera_android_effect_metadata_cache_refresh_universe,ig_android_appstate_logger,ig_prefetch_scheduler_backtest,ig_android_ads_data_preferences_universe,ig_payment_checkout_cvv,ig_android_vc_background_call_toast_universe,ig_android_fb_link_ui_polish_universe,ig_android_qr_code_scanner,ig_disable_fsync_universe,mi_viewpoint_viewability_universe,ig_android_live_egl10_compat,ig_android_video_upload_transform_matrix_fix_universe,ig_android_fb_url_universe,ig_android_reel_raven_video_segmented_upload_universe,ig_android_fb_sync_options_universe,ig_android_recommend_accounts_destination_routing_fix,ig_android_enable_automated_instruction_text_ar,ig_traffic_routing_universe,ig_stories_allow_camera_actions_while_recording,ig_shopping_checkout_mvp_experiment,ig_android_video_fit_scale_type_igtv,ig_android_igtv_player_follow_button,ig_android_arengine_remote_scripting_universe,ig_android_page_claim_deeplink_qe,ig_android_logging_metric_universe_v2,ig_android_xposting_newly_fbc_people,ig_android_recognition_tracking_thread_prority_universe,ig_android_contact_point_upload_rate_limit_killswitch,ig_android_optic_photo_cropping_fixes,ig_android_sso_kototoro_app_universe,ig_android_profile_thumbnail_impression,ig_camera_android_share_effect_link_universe,ig_android_igtv_autoplay_on_prepare,ig_android_ads_rendering_logging,ig_shopping_size_selector_redesign,ig_android_image_exif_metadata_ar_effect_id_universe,ig_android_optic_new_architecture,ig_android_external_gallery_import_affordance,ig_search_hashtag_content_advisory_remove_snooze,ig_android_on_notification_cleared_async_universe,ig_payment_checkout_info"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)

            self.SendRequestsync1(signature18)
        except Exception as e:
            self.sync1()
            pass


        return True

    def sync2(self):

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

            self.SendRequestsync2(signature18)
        except Exception as e:
            self.sync2()
            pass

        return True

    def notifications1(self):

        try:

            data = 'phone_id=' + self.phoneid + '&user_ids=' + self.userid + '&device_id=' + self.deviceid + '&_uuid=' + self.guid

            status = self.SendRequestnotifications1(data)
        except Exception as e:
            self.notifications1()
            pass

        return status

    def reeltray1(self):

        try:

            atamm = [{"name": "SUPPORTED_SDK_VERSIONS",
                      "value": "90.0,91.0,92.0,93.0,94.0,95.0,96.0,97.0,98.0,99.0,100.0,101.0,102.0,103.0,104.0,105.0,106.0,107.0,108.0,109.0,110.0,111.0,112.0,113.0"},
                     {"name": "FACE_TRACKER_VERSION", "value": "14"}, {"name": "COMPRESSION", "value": "PVR_COMPRESSION"},
                     {"name": "COMPRESSION", "value": "ETC2_COMPRESSION"},
                     {"name": "world_tracker", "value": "world_tracker_enabled"}]

            alfason = 'supported_capabilities_new=' + json.dumps(
                atamm) + '&reason=cold_start&timezone_offset=3600&tray_session_id=' + self.generateUUID(
                True) + '&request_id=' + self.generateUUID(True) + '&_uuid=' + self.guid

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            status = self.SendRequestloginsonrasitoplu1post('feed/reels_tray/', ddd80)
        except Exception as e:
            self.reeltray1()
            pass

        return status

    def timeline(self):

        try:

            data = 'feed_view_info=%5B%5D&phone_id=' + self.phoneid + '&reason=cold_start_fetch&battery_level=29&timezone_offset=3600&device_id=' + self.deviceid + '&request_id=' + self.generateUUID(
                True) + '&is_pull_to_refresh=0&_uuid=' + self.guid + '&is_charging=0&is_dark_mode=0&will_sound_on=0&session_id=' + self.session_id + '&bloks_versioning_id=' + self.BloksVersionId

            status = self.SendRequesttimeline1(data)
        except Exception as e:
            self.timeline()
            pass

        return status

    def ndx_ig_steps(self):

        try:

            status = self.SendRequestloginsonrasitoplu2get('devices/ndx/api/async_get_ndx_ig_steps/')

        except Exception as e:
            self.ndx_ig_steps()
            pass


        return status

    def banyan1(self):

        try:

            status = self.SendRequestloginsonrasitoplu1get('banyan/banyan/?views=%5B%22story_share_sheet%22%2C%22direct_user_search_nullstate%22%2C%22forwarding_recipient_sheet%22%2C%22threads_people_picker%22%2C%22direct_inbox_active_now%22%2C%22group_stories_share_sheet%22%2C%22call_recipients%22%2C%22reshare_share_sheet%22%2C%22direct_user_search_keypressed%22%5D')

        except Exception as e:
            self.banyan1()
            pass

        return status

    def register1(self):
    
        try:

            self.atak = {
                "ck": self.ck,
                "ai": 567310203415052,
                "di": self.di,
                "pn": "com.instagram.android"
            }
            message = json.dumps(self.atak)
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')

            # print(base64_message)

            self.registerkey = {"k": base64_message, "v": 0, "t": "fbns-b64"}  #

            print("register: ",self.registerkey)

            alfason = 'device_type=android_mqtt&is_main_push_channel=true&device_sub_type=2&device_token=' + json.dumps(self.registerkey) + '&guid=' + self.guid + '&_uuid=' + self.guid + '&users=' + self.userid + '&family_device_id=' + self.phoneid

            status = self.SendRequestloginsonrasitoplu1post(
                'push/register/', alfason)
        except:
            self.register1()
            pass

        return status

    def register2(self):

        try:

            message = json.dumps(self.atak)
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')

            # print(base64_message)

            alfalar = base64_message

            alfason = 'device_type=android_fcm&is_main_push_channel=false&device_sub_type=0&device_token=' + json.dumps(
                alfalar) + '&guid=' + self.guid + '&_uuid=' + self.guid + '&users=' + self.userid + '&family_device_id=' + self.phoneid

            status = self.SendRequestloginsonrasitoplu1post(
                'push/register/', alfason)
        except Exception as e:
            self.register2()
            pass

        return status

    def timezone1(self):

        try:

            status = self.SendRequestloginsonrasitoplu1get('news/inbox/?mark_as_seen=false&timezone_offset=3600')


        except Exception as e:
            self.timezone1()
            pass

        return status

    def fetch_config1(self):

        try:

            status = self.SendRequestconfigget('loom/fetch_config/')


        except Exception as e:
            self.fetch_config1()
            pass

        return status

    def media_blocked1(self):

        try:

            status = self.SendRequestloginsonrasitoplu1get('media/blocked/')
        except Exception as e:
            self.media_blocked1()
            pass

        return status

    def getcools1(self):
        try:

            status = self.SendRequestloginsonrasitoplu2get('qp/get_cooldowns/?signed_body=SIGNATURE.%7B%7D')

        except Exception as e:
            self.getcools1()
            pass

        return status

    def scores1(self):
        try:

            status = self.SendRequestloginsonrasitoplu1get('scores/bootstrap/users/?surfaces=%5B%22autocomplete_user_list%22%2C%22coefficient_besties_list_ranking%22%2C%22coefficient_rank_recipient_user_suggestion%22%2C%22coefficient_ios_section_test_bootstrap_ranking%22%2C%22coefficient_direct_recipients_ranking_variant_2%22%5D')
        except Exception as e:
            self.scores1()
            pass

        return status

    def discover1(self):

        try:

            status = self.SendRequestloginsonrasitoplu2get('discover/topical_explore/?is_prefetch=true&omit_cover_media=true&reels_configuration=default&use_sectional_payload=true&timezone_offset=3600&session_id=' + self.generateUUID(True) + '&include_fixed_destinations=true')
        except Exception as e:
            self.discover1()
            pass

        return status

    def notifications2(self):

        try:

            data = 'phone_id=' + self.phoneid + '&user_ids=' + self.userid + '&device_id=' + self.deviceid + '&_uuid=' + self.guid

            status = self.SendRequestloginsonrasitoplu1post('notifications/badge/', data)
        except Exception as e:
            self.notifications2()
            pass

        return status

    def get_viewable1(self):

        try:

            status = self.SendRequestloginsonrasitoplu2get('status/get_viewable_statuses/?include_authors=true')
        except Exception as e:
            self.get_viewable1()
            pass

        return status

    def loglarbaslangic1(self):

        try:

            alfa = {
                "seq": 2,
                "app_id": "567067343352427",
                "app_ver": self.appver,
                "build_num": "289692181",
                "device_id": self.deviceid,
                "family_device_id": self.phoneid,
                "session_id": self.generateUUID(True),
                "channel": "zero_latency",
                "app_uid": self.userid,
                "claims": [
                    self.claim
                ],
                "config_version": "v2",
                "config_checksum": None,
                "data": [
                    {
                        "name": "instagram_netego_impression",
                        "time": self.timestamp1(True),
                        "module": "feed_timeline",
                        "sampling_rate": 1,
                        "extra": {
                            "id": None,
                            "netego_id": None,
                            "tracking_token": None,
                            "type": "suggested_users",
                            "position": 0,
                            "m_ix": 0,
                            "session_id": self.generateUUID(True),
                            "gap_to_last_ad": "-1",
                            "gap_to_last_netego": "-1",
                            "pk": self.userid,
                            "release_channel": "prod",
                            "radio_type": "wifi-none"
                        }
                    }
                ],
                "log_type": "client_event"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfa))
            # print("aaaaa", ddd80)

            alfason = 'access_token=' + '567067343352427' + '|' + 'f249176f09e26ce54212b472dbab8fa8' + '&format=json&compressed=' + '0' + '&sent_time=' + self.timestamp1(
                True) + '&message=' + ddd80

            data = alfason

            status = self.SendRequestlogtoplu1(data)
        except Exception as e:
            self.loglarbaslangic1()
            pass

        return status

    def process_contact1(self):

        try:

            alfason = {
                "phone_id": self.phoneid,
                "_uid": self.userid,
                "device_id": self.deviceid,
                "_uuid": self.deviceid,
                "google_tokens": "[]"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)
            status = self.SendRequestloginsonrasitoplu1post('accounts/process_contact_point_signals/', signature18)
        except Exception as e:
            self.process_contact1()
            pass

        return status

    def store_client_push_permissions1(self):

        try:

            data = 'enabled=true&device_id=' + self.deviceid + '&_uuid=' + self.guid

            status = self.SendRequestloginsonrasitoplu1post('accounts/process_contact_point_signals/', data)
        except Exception as e:
            self.store_client_push_permissions1()
            pass

        return status

    def visualmessage1(self):

        try:

            status = self.SendRequestloginsonrasitoplu2get(
                'direct_v2/inbox/?visual_message_return_type=unseen&thread_message_limit=10&persistentBadging=true&limit=20&fetch_reason=initial_snapshot')
        except Exception as e:
            self.visualmessage1()
            pass

        return status

    def account_linking1(self):

        try:

            status = self.SendRequestloginsonrasitoplu2get(
                'ig_fb_xposting/account_linking/user_xposting_destination/?signed_body=SIGNATURE.%7B%7D')
        except Exception as e:
            self.account_linking1()
            pass

        return status

    def batch_fetch1(self):

        try:

            atakan1 = str(random.randint(4000, 9999))
            atakan1a = atakan1

            atakan2 = str(random.randint(5000, 9999))
            atakan2a = atakan2

            atakan3 = str(random.randint(5000, 9999))
            atakan3a = atakan3

            atakan4 = str(random.randint(5000, 9999))
            atakan4a = atakan4

            alfason = {
                "surfaces_to_triggers": "{\"" + atakan1a + "\":[\"instagram_navigation_tooltip\",\"instagram_feed_tool_tip\",\"instagram_featured_product_media_tooltip\",\"instagram_feed_promote_cta_tooltip\"],\"" + "4715" + "\":[\"instagram_feed_header\"],\"" + atakan2a + "\":[\"instagram_feed_prompt\",\"instagram_shopping_enable_auto_highlight_interstitial\"]}",
                "surfaces_to_queries": "{\"" + atakan1a + "\":\"Query+QuickPromotionSurfaceQuery:+Viewer{viewer(){eligible_promotions.trigger_context_v2(<trigger_context_v2>).ig_parameters(<ig_parameters>).trigger_name(<trigger_name>).surface_nux_id(<surface>).external_gating_permitted_qps(<external_gating_permitted_qps>).supports_client_filters(true).include_holdouts(true){edges{client_ttl_seconds,log_eligibility_waterfall,is_holdout,priority,time_range{start,end},node{id,promotion_id,logging_data,is_server_force_pass,max_impressions,triggers,contextual_filters{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}}}}}},is_uncancelable,template{name,parameters{name,required,bool_value,string_value,color_value}},creatives{title{text},content{text},footer{text},social_context{text},social_context_images,primary_action{title{text},url,limit,dismiss_promotion},secondary_action{title{text},url,limit,dismiss_promotion},dismiss_action{title{text},url,limit,dismiss_promotion},image.scale(<scale>){uri,width,height}}}}}}}\",\"" + atakan3a + "\":\"Query+QuickPromotionSurfaceQuery:+Viewer{viewer(){eligible_promotions.trigger_context_v2(<trigger_context_v2>).ig_parameters(<ig_parameters>).trigger_name(<trigger_name>).surface_nux_id(<surface>).external_gating_permitted_qps(<external_gating_permitted_qps>).supports_client_filters(true).include_holdouts(true){edges{client_ttl_seconds,log_eligibility_waterfall,is_holdout,priority,time_range{start,end},node{id,promotion_id,logging_data,is_server_force_pass,max_impressions,triggers,contextual_filters{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}}}}}},is_uncancelable,template{name,parameters{name,required,bool_value,string_value,color_value}},creatives{title{text},content{text},footer{text},social_context{text},social_context_images,primary_action{title{text},url,limit,dismiss_promotion},secondary_action{title{text},url,limit,dismiss_promotion},dismiss_action{title{text},url,limit,dismiss_promotion},image.scale(<scale>){uri,width,height},dark_mode_image.scale(<scale>){uri,width,height}}}}}}}\",\"" + atakan4a + "\":\"Query+QuickPromotionSurfaceQuery:+Viewer{viewer(){eligible_promotions.trigger_context_v2(<trigger_context_v2>).ig_parameters(<ig_parameters>).trigger_name(<trigger_name>).surface_nux_id(<surface>).external_gating_permitted_qps(<external_gating_permitted_qps>).supports_client_filters(true).include_holdouts(true){edges{client_ttl_seconds,log_eligibility_waterfall,is_holdout,priority,time_range{start,end},node{id,promotion_id,logging_data,is_server_force_pass,max_impressions,triggers,contextual_filters{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}},clauses{clause_type,filters{filter_type,unknown_action,value{name,required,bool_value,int_value,string_value},extra_datas{name,required,bool_value,int_value,string_value}}}}}},is_uncancelable,template{name,parameters{name,required,bool_value,string_value,color_value}},creatives{title{text},content{text},footer{text},social_context{text},social_context_images,primary_action{title{text},url,limit,dismiss_promotion},secondary_action{title{text},url,limit,dismiss_promotion},dismiss_action{title{text},url,limit,dismiss_promotion},image.scale(<scale>){uri,width,height},dark_mode_image.scale(<scale>){uri,width,height}}}}}}}\"}",
                "vc_policy": "default",
                "_uid": self.userid,
                "_uuid": self.guid,
                "scale": "3",
                "version": "1"
            }

            # data = 'signed_body=SIGNATURE.%7B%22surfaces_to_triggers%22%3A%22%7B%5C%225858%5C%22%3A%5B%5C%22instagram_navigation_tooltip%5C%22%2C%5C%22instagram_feed_tool_tip%5C%22%2C%5C%22instagram_featured_product_media_tooltip%5C%22%2C%5C%22instagram_feed_promote_cta_tooltip%5C%22%5D%2C%5C%224715%5C%22%3A%5B%5C%22instagram_feed_header%5C%22%5D%2C%5C%225734%5C%22%3A%5B%5C%22instagram_feed_prompt%5C%22%2C%5C%22instagram_shopping_enable_auto_highlight_interstitial%5C%22%5D%7D%22%2C%22surfaces_to_queries%22%3A%22%7B%5C%225858%5C%22%3A%5C%22Query+QuickPromotionSurfaceQuery%3A+Viewer%7Bviewer%28%29%7Beligible_promotions.trigger_context_v2%28%3Ctrigger_context_v2%3E%29.ig_parameters%28%3Cig_parameters%3E%29.trigger_name%28%3Ctrigger_name%3E%29.surface_nux_id%28%3Csurface%3E%29.external_gating_permitted_qps%28%3Cexternal_gating_permitted_qps%3E%29.supports_client_filters%28true%29.include_holdouts%28true%29%7Bedges%7Bclient_ttl_seconds%2Clog_eligibility_waterfall%2Cis_holdout%2Cpriority%2Ctime_range%7Bstart%2Cend%7D%2Cnode%7Bid%2Cpromotion_id%2Clogging_data%2Cis_server_force_pass%2Cmax_impressions%2Ctriggers%2Ccontextual_filters%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%7D%7D%7D%7D%2Cis_uncancelable%2Ctemplate%7Bname%2Cparameters%7Bname%2Crequired%2Cbool_value%2Cstring_value%2Ccolor_value%7D%7D%2Ccreatives%7Btitle%7Btext%7D%2Ccontent%7Btext%7D%2Cfooter%7Btext%7D%2Csocial_context%7Btext%7D%2Csocial_context_images%2Cprimary_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Csecondary_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Cdismiss_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Cimage.scale%28%3Cscale%3E%29%7Buri%2Cwidth%2Cheight%7D%7D%7D%7D%7D%7D%7D%5C%22%2C%5C%224715%5C%22%3A%5C%22Query+QuickPromotionSurfaceQuery%3A+Viewer%7Bviewer%28%29%7Beligible_promotions.trigger_context_v2%28%3Ctrigger_context_v2%3E%29.ig_parameters%28%3Cig_parameters%3E%29.trigger_name%28%3Ctrigger_name%3E%29.surface_nux_id%28%3Csurface%3E%29.external_gating_permitted_qps%28%3Cexternal_gating_permitted_qps%3E%29.supports_client_filters%28true%29.include_holdouts%28true%29%7Bedges%7Bclient_ttl_seconds%2Clog_eligibility_waterfall%2Cis_holdout%2Cpriority%2Ctime_range%7Bstart%2Cend%7D%2Cnode%7Bid%2Cpromotion_id%2Clogging_data%2Cis_server_force_pass%2Cmax_impressions%2Ctriggers%2Ccontextual_filters%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%7D%7D%7D%7D%2Cis_uncancelable%2Ctemplate%7Bname%2Cparameters%7Bname%2Crequired%2Cbool_value%2Cstring_value%2Ccolor_value%7D%7D%2Ccreatives%7Btitle%7Btext%7D%2Ccontent%7Btext%7D%2Cfooter%7Btext%7D%2Csocial_context%7Btext%7D%2Csocial_context_images%2Cprimary_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Csecondary_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Cdismiss_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Cimage.scale%28%3Cscale%3E%29%7Buri%2Cwidth%2Cheight%7D%2Cdark_mode_image.scale%28%3Cscale%3E%29%7Buri%2Cwidth%2Cheight%7D%7D%7D%7D%7D%7D%7D%5C%22%2C%5C%225734%5C%22%3A%5C%22Query+QuickPromotionSurfaceQuery%3A+Viewer%7Bviewer%28%29%7Beligible_promotions.trigger_context_v2%28%3Ctrigger_context_v2%3E%29.ig_parameters%28%3Cig_parameters%3E%29.trigger_name%28%3Ctrigger_name%3E%29.surface_nux_id%28%3Csurface%3E%29.external_gating_permitted_qps%28%3Cexternal_gating_permitted_qps%3E%29.supports_client_filters%28true%29.include_holdouts%28true%29%7Bedges%7Bclient_ttl_seconds%2Clog_eligibility_waterfall%2Cis_holdout%2Cpriority%2Ctime_range%7Bstart%2Cend%7D%2Cnode%7Bid%2Cpromotion_id%2Clogging_data%2Cis_server_force_pass%2Cmax_impressions%2Ctriggers%2Ccontextual_filters%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%2Cclauses%7Bclause_type%2Cfilters%7Bfilter_type%2Cunknown_action%2Cvalue%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%2Cextra_datas%7Bname%2Crequired%2Cbool_value%2Cint_value%2Cstring_value%7D%7D%7D%7D%7D%7D%2Cis_uncancelable%2Ctemplate%7Bname%2Cparameters%7Bname%2Crequired%2Cbool_value%2Cstring_value%2Ccolor_value%7D%7D%2Ccreatives%7Btitle%7Btext%7D%2Ccontent%7Btext%7D%2Cfooter%7Btext%7D%2Csocial_context%7Btext%7D%2Csocial_context_images%2Cprimary_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Csecondary_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Cdismiss_action%7Btitle%7Btext%7D%2Curl%2Climit%2Cdismiss_promotion%7D%2Cimage.scale%28%3Cscale%3E%29%7Buri%2Cwidth%2Cheight%7D%2Cdark_mode_image.scale%28%3Cscale%3E%29%7Buri%2Cwidth%2Cheight%7D%7D%7D%7D%7D%7D%7D%5C%22%7D%22%2C%22vc_policy%22%3A%22default%22%2C%22_uid%22%3A%2248594379482%22%2C%22_uuid%22%3A%2268f2e680-a663-4484-ad1f-8f0b49c2f53a%22%2C%22scale%22%3A%223%22%2C%22version%22%3A%221%22%7D'


            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = 'signed_body=SIGNATURE.{}'.format(ddd80)

            atmacalar90 = signature18

            print(atmacalar90)
            self.SendRequestbatchfetch(atmacalar90)
        except Exception as e:
            self.batch_fetch1()
            pass

        return True

    def get_presence1(self):

        try:

            status = self.SendRequestloginsonrasitoplu2get(
                'direct_v2/get_presence/')
        except Exception as e:
            self.get_presence1()
            pass


        return status

    def get_presence2(self):

        try:

            status = self.SendRequestloginsonrasitoplu2get(
                'accounts/get_presence_disabled/?signed_body=SIGNATURE.%7B%7D')
        except Exception as e:
            self.get_presence2()
            pass


        return status

    def aktivateson(self):

        try:

            deger = {
                "_appVersion": self.appver,
                "_logTime": self.timestamp2(True),
                "_eventName": "fb_mobile_activate_app"
            }

            f = tempfile.TemporaryFile()
            f.write(json.dumps([deger]).encode("utf-8"))
            f.seek(0)

            self.payload42 = {'format': 'json',
                              'advertiser_tracking_enabled': '1',
                              'anon_id': 'XZ' + self.waterfall_id,
                              'advertiser_id': self.adid,
                              'event': 'CUSTOM_APP_EVENTS',
                              'application_package_name': 'com.instagram.android',
                              'application_tracking_enabled': '1'}

            self.files1 = [
                ('custom_events_file', ('custom_events_file.json', f, 'application/json'))
            ]
            self.SendRequestactivate1()

            data = 'advertiser_tracking_enabled=1&anon_id=XZ' + self.waterfall_id + '&advertiser_id=' + self.adid + '&event=MOBILE_APP_INSTALL&application_package_name=com.instagram.android&application_tracking_enabled=1'

            status_code = self.SendRequestactivate(data)
            pass
        except Exception as e:
            self.aktivateson()
            pass

        return status_code

    def has_interop_upgraded1(self):

        try:

            self.SendRequestloginsonrasitoplu2get(
                'direct_v2/has_interop_upgraded/')
        except Exception as e:
            self.has_interop_upgraded1()
            pass


        return True

    def direct_v2(self):

        try:

            self.SendRequestloginsonrasitoplu1get(
                'direct_v2/has_interop_upgraded/')
        except Exception as e:
            self.direct_v2()
            pass


        return True

    def direct_v3(self):

        try:

            status = self.SendRequestloginsonrasitoplu1get(
                'direct_v2/inbox/?visual_message_return_type=unseen&persistentBadging=true&limit=0')
        except Exception as e:
            self.direct_v3()
            pass


        return status

    def ipsor(self):
        try:

            r = requests.get('http://ip6.me/api/', proxies=self.login_after_proxy, verify=True, timeout=20)
            # print(r)

            c = r.content
            d = c.decode("utf-8")
            e = d.split(",")[1]
            print("Şuanki ipniz:", e)
            pass
        except Exception as e:
            self.ipsor()
            pass
        # sleep(20)
        return True

    def direct_v4(self):
        try:

            status = self.SendRequestloginsonrasitoplu1get(
                'direct_v2/inbox/?visual_message_return_type=unseen&thread_message_limit=10&persistentBadging=true&limit=20&fetch_reason=initial_snapshot')
        except Exception as e:
            self.direct_v4()
            pass


        return status

    def write_supported1(self):

        try:

            alfason = {
                "supported_capabilities_new": "[{\"name\":\"SUPPORTED_SDK_VERSIONS\",\"value\":\"90.0,91.0,92.0,93.0,94.0,95.0,96.0,97.0,98.0,99.0,100.0,101.0,102.0,103.0,104.0,105.0,106.0,107.0,108.0,109.0,110.0,111.0,112.0,113.0\"},{\"name\":\"FACE_TRACKER_VERSION\",\"value\":\"14\"},{\"name\":\"COMPRESSION\",\"value\":\"PVR_COMPRESSION\"},{\"name\":\"COMPRESSION\",\"value\":\"ETC2_COMPRESSION\"},{\"name\":\"world_tracker\",\"value\":\"world_tracker_enabled\"}]",
                "_uid": self.userid,
                "_uuid": self.guid
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)
            status = self.SendRequestloginsonrasitoplu1post('creatives/write_supported_capabilities/', signature18)

        except Exception as e:
            self.write_supported1()
            pass


        return status

    def banyan2(self):
        try:

            status = self.SendRequestloginsonrasitoplu2get(
                'banyan/banyan/?views=%5B%22story_share_sheet%22%2C%22direct_user_search_nullstate%22%2C%22forwarding_recipient_sheet%22%2C%22threads_people_picker%22%2C%22direct_inbox_active_now%22%2C%22group_stories_share_sheet%22%2C%22call_recipients%22%2C%22reshare_share_sheet%22%2C%22direct_user_search_keypressed%22%5D')
        except Exception as e:
            self.banyan2()
            pass

        return status

    def loglarbaslangic2(self):
        try:
            nuxid = str(random.randint(1000, 9999))
            self.nuxid = nuxid
            promotionid = str(random.randint(100000000000000, 999999999999999))
            self.promotionid = promotionid

            alfa = {
                "seq": 4,
                "app_id": "567067343352427",
                "app_ver": self.appver,
                "build_num": "289692181",
                "device_id": self.deviceid,
                "family_device_id": self.phoneid,
                "session_id": self.generateUUID(True),
                "channel": "zero_latency",
                "app_uid": self.userid,
                "claims": [
                    self.claim
                ],
                "config_version": "v2",
                "config_checksum": None,
                "data": [
                    {
                        "name": "qp_exposure",
                        "time": self.timestamp1(True),
                        "module": "quick_promotion",
                        "sampling_rate": 1,
                        "extra": {
                            "nux_id": self.nuxid,
                            "promotion_id": self.promotionid,
                            "instance_log_data": "{\"eligibility_status\":\"1\",\"qp_status\":\"Public\",\"qp_start_time\":\"" + self.timestamp2(
                                True) + "\",\"qp_end_time\":\"" + self.timestamp2(
                                True) + "\",\"supports_dark_mode_image\":\"1\",\"uuid\":\"" + self.guid + "\",\"viewer_id\":\"0\",\"is_hscroll_unit\":\"\"}",
                            "pk": self.userid,
                            "release_channel": "prod",
                            "radio_type": "wifi-none"
                        }
                    }
                ],
                "log_type": "client_event"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfa))
            # print("aaaaa", ddd80)

            alfason = 'access_token=' + '567067343352427' + '|' + 'f249176f09e26ce54212b472dbab8fa8' + '&format=json&compressed=' + '0' + '&sent_time=' + self.timestamp1(
                True) + '&message=' + ddd80

            data = alfason

            status = self.SendRequestlogtoplu1(data)
        except Exception as e:
            self.loglarbaslangic2()
            pass

        return status

    def arlink1(self):
        try:
            status = self.SendRequestloginsonrasitoplu2get(
                'users/arlink_download_info/?version_override=2.2.1')
        except Exception as e:
            self.arlink1()
            pass

        return status

    def loglarbaslangic3(self):

        try:

            alfa = {
                "seq": 5,
                "app_id": "567067343352427",
                "app_ver": self.appver,
                "build_num": "289692181",
                "device_id": self.deviceid,
                "family_device_id": self.phoneid,
                "session_id": self.generateUUID(True),
                "channel": "zero_latency",
                "app_uid": self.userid,
                "claims": [
                    self.claim
                ],
                "config_version": "v2",
                "config_checksum": None,
                "data": [
                    {
                        "name": "qp_exposure",
                        "time": self.timestamp1(True),
                        "module": "quick_promotion",
                        "sampling_rate": 1,
                        "extra": {
                            "nux_id": self.nuxid,
                            "promotion_id": self.promotionid,
                            "instance_log_data": "{\"eligibility_status\":\"1\",\"qp_status\":\"Public\",\"qp_start_time\":\"" + self.timestamp2(
                                True) + "\",\"qp_end_time\":\"" + self.timestamp2(
                                True) + "\",\"supports_dark_mode_image\":\"1\",\"uuid\":\"" + self.guid + "\",\"viewer_id\":\"0\",\"is_hscroll_unit\":\"\"}",
                            "pk": self.userid,
                            "release_channel": "prod",
                            "radio_type": "wifi-none"
                        }
                    },
                    {
                        "name": "view",
                        "time": self.timestamp1(True),
                        "module": "quick_promotion",
                        "sampling_rate": 1,
                        "extra": {
                            "trigger": "instagram_feed_header",
                            "nux_id": self.nuxid,
                            "promotion_id": self.promotionid,
                            "instance_log_data": "{\"eligibility_status\":\"1\",\"qp_status\":\"Public\",\"qp_start_time\":\"" + self.timestamp2(
                                True) + "\",\"qp_end_time\":\"" + self.timestamp2(
                                True) + "\",\"supports_dark_mode_image\":\"1\",\"uuid\":\"" + self.guid + "\",\"viewer_id\":\"0\",\"is_hscroll_unit\":\"\"}",
                            "pk": self.userid,
                            "release_channel": "prod",
                            "radio_type": "wifi-none"
                        }
                    }
                ],
                "log_type": "client_event"
            }

            ddd80 = urllib.parse.quote(json.dumps(alfa))
            # print("aaaaa", ddd80)

            alfason = 'access_token=' + '567067343352427' + '|' + 'f249176f09e26ce54212b472dbab8fa8' + '&format=json&compressed=' + '0' + '&sent_time=' + self.timestamp1(
                True) + '&message=' + ddd80

            data = alfason

            status = self.SendRequestlogtoplu1(data)
        except Exception as e:
            self.loglarbaslangic3()
            pass

        return status

    def android_modules1(self):

        try:

            id5 = "".join(random.choices("abcdefhijkmloprstuvyz0123456789", k=64))
            self.id5a = id5

            alfason = {
                "_uid": self.userid,
                "_uuid": self.guid,
                "hashes": [
                    self.id5a
                ]
            }

            ddd80 = urllib.parse.quote(json.dumps(alfason))
            # print("aaaaa", ddd80)

            signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
            # print(signature18)
            status = self.SendRequestloginsonrasitoplu1post('android_modules/download/', signature18)
        except Exception as e:
            self.android_modules1()
            pass

        return status

    ###### sıra numara  45 ###########

    def graphql1(self):
        try:
            data = 'doc_id=' + str(random.randint(1000000000000000,
                                                  9999999999999999)) + '&locale=tr_TR&vc_policy=default&signed_body=SIGNATURE.&strip_nulls=true&strip_defaults=true&query_params=%7B%7D'

            status = self.SendRequestgraphql1(data)
        except Exception as e:
            self.graphql1()
            pass

        return status





    def SendRequestaccountig_steps(self):

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
        response2 = requests.get('https://i.instagram.com/api/v1/devices/ndx/api/async_get_ndx_ig_steps/',
                                 headers=headers,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)
        # print("Status5: ", response2.headers)
        self.rur = response2.headers['ig-set-ig-u-rur']
        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            #print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            #print('shbts: ', self.shbts)
        except Exception as e:
            self.shbid = None
            #print('shbid: ', self.shbid)

            self.shbts = None
            #print('shbts: ', self.shbts)

            pass
        # print("rur: ", self.rur)
        # print("Status5: ", response2.content)

        return response2.status_code



    def graphql2(self):

        try:

            data = 'doc_id=' + str(random.randint(1000000000000000,
                                                  9999999999999999)) + '&locale=tr_TR&vc_policy=default&signed_body=SIGNATURE.&variables=&strip_nulls=true&strip_defaults=true'

            status = self.SendRequestgraphql2(data)
        except Exception as e:
            self.graphql2()
            pass

        return status

    def loglarbaslangic4(self):
        try:

            alfa = {
                "request_info": {},
                "config": {
                    "config_version": "v2",
                    "app_uid": self.userid,
                    "app_ver": self.appver
                },
                "batches": [
                    {
                        "seq": 1,
                        "app_id": "567067343352427",
                        "app_ver": self.appver,
                        "build_num": "289692181",
                        "device_id": self.deviceid,
                        "family_device_id": self.phoneid,
                        "session_id": self.generateUUID(True),
                        "channel": "regular",
                        "log_type": "client_event",
                        "app_uid": "0",
                        "claims": [
                            "0"
                        ],
                        "config_version": "v2",
                        "config_checksum": None,
                        "data": [
                            {
                                "name": "ig_zero_url_rewrite",
                                "time": self.timestamp1(True),  # "1629592319.036",
                                "tags": 1,
                                "extra": {
                                    "rewritten_url": "https://b.i.instagram.com/api/v1/zr/token/result/?device_id=" + self.androidid + "&token_hash=&custom_device_id=" + self.deviceid + "&fetch_reason=token_expired",
                                    "url": "https://i.instagram.com/api/v1/zr/token/result/?device_id=" + self.androidid + "&token_hash=&custom_device_id=" + self.deviceid + "&fetch_reason=token_expired",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "instagram_android_install_with_referrer",
                                "time": self.timestamp1(True),  # "1629592319.045",
                                "module": "install_referrer",
                                "sampling_rate": 1,
                                "extra": {
                                    "referrer": "first_open_waiting_for_referrer",
                                    "waterfall_id": self.waterfall_id,
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "step_view_loaded",
                                "time": self.timestamp1(True),  # "1629592319.055",
                                "tags": 1,
                                "extra": {
                                    "waterfall_id": self.waterfall_id,
                                    "containermodule": "waterfall_log_in",
                                    "elapsed_time": 863,
                                    "start_time": self.timestamp2(True),
                                    "step": "landing",
                                    "guid": self.deviceid,
                                    "is_facebook_app_installed": False,
                                    "messenger_installed": False,
                                    "whatsapp_installed": True,
                                    "fb_lite_installed": False,
                                    "login_userid": [],
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "landing_created",
                                "time": self.timestamp1(True),  # "1629592319.067",
                                "tags": 1,
                                "extra": {
                                    "waterfall_id": self.waterfall_id,
                                    "containermodule": "waterfall_log_in",
                                    "elapsed_time": 878,
                                    "start_time": self.timestamp2(True),
                                    "step": "landing",
                                    "is_facebook_app_installed": False,
                                    "guid": self.deviceid,
                                    "did_facebook_sso": False,
                                    "did_log_in": False,
                                    "network_type": "WIFI",
                                    "app_lang": "tr_TR",
                                    "device_lang": "tr_TR",
                                    "funnel_name": "landing",
                                    "current_time": self.timestamp2(True),
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "app_installations",
                                "time": self.timestamp1(True),  # "1629592319.111",
                                "sampling_rate": 1,
                                "extra": {
                                    str(random.randint(100000000000000, 999999999999999)): False,
                                    str(random.randint(100000000000000, 999999999999999)): False,
                                    str(random.randint(100000000000000, 999999999999999)): True,
                                    str(random.randint(100000000000000, 999999999999999)): False,
                                    str(random.randint(1000000000000000, 9999999999999999)): False,
                                    str(random.randint(100000000000000, 999999999999999)): False,
                                    str(random.randint(100000000000, 999999999999)): False,
                                    str(random.randint(100000000000000, 999999999999999)): False,
                                    str(random.randint(100000000000, 999999999999)): True,
                                    str(random.randint(100000000000000, 999999999999999)): False,
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_zero_url_rewrite",
                                "time": self.timestamp1(True),  # "1629592319.132",
                                "tags": 1,
                                "extra": {
                                    "rewritten_url": "https://b.i.instagram.com/api/v1/qe/sync/",
                                    "url": "https://i.instagram.com/api/v1/qe/sync/",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            }
                        ]
                    },
                    {
                        "seq": 0,
                        "app_id": "567067343352427",
                        "app_ver": self.appver,
                        "build_num": "289692181",
                        "device_id": self.deviceid,
                        "family_device_id": None,
                        "session_id": self.generateUUID(True),
                        "channel": "regular",
                        "log_type": "client_event",
                        "app_uid": "0",
                        "config_version": "v2",
                        "config_checksum": None,
                        "data": [
                            {
                                "name": "perf",
                                "time": self.timestamp1(True),  # "1629592319.838",
                                "extra": {
                                    "marker_id": 15335435,
                                    "instance_id": 1285597345,
                                    "sample_rate": 1,
                                    "time_since_boot_ms": 101224652,
                                    "duration_ns": 3961654404,
                                    "action_id": 467,
                                    "marker_type": 1,
                                    "method": "random_sampling",
                                    "annotations": {
                                        "type": "cold",
                                        "failure_reason": "no_surface_attached",
                                        "trigger": "unknown",
                                        "current_module": "landing_facebook",
                                        "build_type": "prod",
                                        "first_run": "on_install"
                                    },
                                    "annotations_bool": {
                                        "is_successful": False,
                                        "user_logged_in": False
                                    },
                                    "marker": "client_tti",
                                    "points": [
                                        {
                                            "timeSinceStart": 104,
                                            "name": "RELIABILITY_INITIALIZED"
                                        },
                                        {
                                            "timeSinceStart": 1798,
                                            "name": "SOLOADER_INITIALIZED"
                                        },
                                        {
                                            "timeSinceStart": 1799,
                                            "name": "MULTIDEX_INSTALLED"
                                        },
                                        {
                                            "timeSinceStart": 2382,
                                            "name": "APP_ONCREATE_START"
                                        },
                                        {
                                            "timeSinceStart": 3049,
                                            "name": "APP_ONCREATE_END"
                                        },
                                        {
                                            "timeSinceStart": 3071,
                                            "name": "LAUNCHER_ACTIVITY_ONCREATE_START"
                                        },
                                        {
                                            "timeSinceStart": 3152,
                                            "name": "LAUNCHER_ACTIVITY_ONCREATE_END"
                                        },
                                        {
                                            "timeSinceStart": 3236,
                                            "name": "ACTIVITY_ONCREATE_START"
                                        }
                                    ],
                                    "metadata": {
                                        "network_stats": {
                                            "network_type": "wifi",
                                            "network_subtype": "none"
                                        },
                                        "cpu_stats": {
                                            "start_pri": -10,
                                            "stop_pri": -10,
                                            "ps_cpu_ms": 1766,
                                            "th_cpu_ms": 655,
                                            "low_power_state": "not+set"
                                        },
                                        "io_stats": {
                                            "ps_flt": 17,
                                            "proc_delayacct_blkio_ticks": 0,
                                            "th_flt": 1,
                                            "class_load_attempts": 0,
                                            "dex_queries": 0,
                                            "class_loads_failed": 0,
                                            "locator_assists": 0,
                                            "wrong_dfa_guesses": 0,
                                            "ps_min_flt": 7564,
                                            "avail_disk_spc_kb": 19691184
                                        }
                                    },
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            }
                        ]
                    },
                    {
                        "seq": 0,
                        "app_id": "567067343352427",
                        "app_ver": self.appver,
                        "build_num": "289692181",
                        "device_id": self.deviceid,
                        "family_device_id": None,
                        "session_id": self.generateUUID(True),
                        "channel": "regular",
                        "log_type": "client_event",
                        "app_uid": "0",
                        "config_version": "v2",
                        "config_checksum": None,
                        "data": [
                            {
                                "name": "ig_zero_url_rewrite",
                                "time": self.timestamp1(True),  # "1629592318.530",
                                "tags": 1,
                                "extra": {
                                    "rewritten_url": "https://b.i.instagram.com/api/v1/facebook_dod/request_dod_resources/?native_build=289692181&prefer_compressed=True&signed_body=SIGNATURE.&ota_build=289692181&resource_flavor=tr&custom_app_id=124024574287414&resource_name=fbt_language_pack.bin",
                                    "url": "https://i.instagram.com/api/v1/facebook_dod/request_dod_resources/?native_build=289692181&prefer_compressed=True&signed_body=SIGNATURE.&ota_build=289692181&resource_flavor=tr&custom_app_id=124024574287414&resource_name=fbt_language_pack.bin",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_zero_url_rewrite",
                                "time": self.timestamp1(True),  # "1629592318.530",
                                "tags": 1,
                                "extra": {
                                    "rewritten_url": "https://b.i.instagram.com/api/v1/zr/token/result/?device_id=" + self.androidid + "&token_hash=&custom_device_id=" + self.deviceid + "&fetch_reason=token_expired",
                                    "url": "https://i.instagram.com/api/v1/zr/token/result/?device_id=" + self.androidid + "&token_hash=&custom_device_id=" + self.deviceid + "&fetch_reason=token_expired",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "instagram_device_ids",
                                "time": self.timestamp1(True),  # "1629592318.531",
                                "tags": 1,
                                "extra": {
                                    "app_device_id": self.deviceid,
                                    "analytics_device_id": None,
                                    "module": "instagram_device_ids",
                                    "waterfall_id": self.waterfall_id,
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "fbresources_not_available",
                                "time": self.timestamp1(True),  # "1629592318.561",
                                "module": "IgResourcesAnalyticsModule",
                                "tags": 1,
                                "extra": {
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "android_apk_testing_exposure",
                                "time": self.timestamp1(True),  # "1629592318.612",
                                "tags": 1,
                                "extra": {
                                    "build_num": 289692181,
                                    "installer": "com.google.android.packageinstaller",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_zero_token_fetch_success",
                                "time": self.timestamp1(True),  # "1629592319.139",
                                "tags": 1,
                                "extra": {
                                    "carrier_id": 0,
                                    "carrier_name": "",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "apk_signature_v2",
                                "time": self.timestamp1(True),  # "1629592319.555",
                                "module": "IgFamilyApplicationInitializer",
                                "sampling_rate": 1,
                                "extra": {
                                    "package_name": "com.instagram.android",
                                    "previous_signature": None,
                                    "signature": "V2_SIGN_NOT_FOUND",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "fbresources_loading_success",
                                "time": self.timestamp1(True),  # "1629592319.769",
                                "module": "IgResourcesAnalyticsModule",
                                "tags": 1,
                                "extra": {
                                    "locale": "tr",
                                    "source": "downloaded",
                                    "file_format": "fbt",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "android_string_impressions",
                                "time": self.timestamp1(True),  # "1629592323.479",
                                "module": "IgResourcesAnalyticsModule",
                                "tags": 1,
                                "extra": {
                                    "impressions": {
                                        "21" + str(random.randint(10000000, 99999999)): 2,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 3,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 2,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1,
                                        "21" + str(random.randint(10000000, 99999999)): 1
                                    },
                                    "string_locale": "tr_TR",
                                    "pk": "0",
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            }
                        ]
                    },
                    {
                        "seq": 0,
                        "app_id": "567067343352427",
                        "app_ver": self.appver,
                        "build_num": "289692181",
                        "device_id": self.deviceid,
                        "family_device_id": self.phoneid,
                        "session_id": self.generateUUID(True),
                        "channel": "regular",
                        "log_type": "client_event",
                        "app_uid": self.userid,
                        "claims": [
                            self.claim
                        ],
                        "config_version": "v2",
                        "config_checksum": None,
                        "data": [
                            {
                                "name": "ig_zero_url_rewrite",
                                "time": self.timestamp1(True),  # "1629592339.312",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "rewritten_url": "https://b.i.instagram.com/api/v1/zr/token/result/?device_id=" + self.androidid + "&token_hash=&custom_device_id=" + self.deviceid + "&fetch_reason=token_expired",
                                    "url": "https://i.instagram.com/api/v1/zr/token/result/?device_id=" + self.androidid + "&token_hash=&custom_device_id=" + self.deviceid + "&fetch_reason=token_expired",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_zero_url_rewrite",
                                "time": self.timestamp1(True),  # "1629592339.333",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "rewritten_url": "https://b.i.instagram.com/api/v1/launcher/sync/",
                                    "url": "https://i.instagram.com/api/v1/launcher/sync/",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_zero_url_rewrite",
                                "time": self.timestamp1(True),  # "1629592339.338",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "rewritten_url": "https://b.i.instagram.com/api/v1/qe/sync/",
                                    "url": "https://i.instagram.com/api/v1/qe/sync/",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_zero_url_rewrite",
                                "time": self.timestamp1(True),  # "1629592339.339",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "rewritten_url": "https://b.i.instagram.com/api/v1/multiple_accounts/get_account_family/",
                                    "url": "https://i.instagram.com/api/v1/multiple_accounts/get_account_family/",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "push_notification_setting",
                                "time": self.timestamp1(True),  # "1629592339.377",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "status": "enabled",
                                    "extra_setting_data": None,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "push_notification_setting",
                                "time": self.timestamp1(True),  # "1629592339.379",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "status": "enabled",
                                    "extra_setting_data": None,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.379",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_product_announcements",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_friends_on_instagram",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_likes",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_other",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_photos_of_you",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_private_user_follow_request",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_igtv_video_updates",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_mentions_in_bio",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_direct",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "uploads",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_reminders",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_direct_requests",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.380",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_igtv_recommended_videos",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_new_followers",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_likes_and_comments_on_photos_of_you",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_support_requests",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_first_posts_and_stories",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_comment_likes",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_live_videos",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_comments",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_shopping_drops",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_view_counts",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_direct_video_chat",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "notification_channel_enabled",
                                "time": self.timestamp1(True),  # "1629592339.381",
                                "module": "NotificationChannelsHelper",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "channel_id": "ig_posting_status",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_zero_token_fetch_success",
                                "time": self.timestamp1(True),  # "1629592339.685",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "carrier_id": 0,
                                    "carrier_name": "",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_cellular_data_opt",
                                "time": self.timestamp1(True),  # "1629592339.751",
                                "sampling_rate": 1,
                                "extra": {
                                    "data_saver_mode": False,
                                    "high_quality_network_setting": 1,
                                    "os_data_saver_settings": 0,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_dark_mode_opt",
                                "time": self.timestamp1(True),  # "1629592339.751",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "os_dark_mode_settings": False,
                                    "dark_mode_in_app_toggle": 1,
                                    "in_app_dark_mode_setting": -1,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "badging_event",
                                "time": self.timestamp1(True),  # "1629592339.811",
                                "module": "badging",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "event_type": "impression",
                                    "use_case_id": "activity_feed",
                                    "badge_value": 0,
                                    "badge_position": "bottom_navigation_bar",
                                    "badge_display_style": "dot_badge",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "badging_event",
                                "time": self.timestamp1(True),  # "1629592339.826",
                                "module": "badging",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "event_type": "impression",
                                    "use_case_id": "profile",
                                    "badge_value": 0,
                                    "badge_position": "bottom_navigation_bar",
                                    "badge_display_style": "dot_badge",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "instagram_stories_request_sent",
                                "time": self.timestamp1(True),  # "1629592340.125",
                                "module": "reel_feed_timeline",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "tray_session_id": self.generateUUID(True),  # self.generateUUID(True),#,
                                    "request_id": "31ca2135-8201-44b7-9e04-882cea5560cd",
                                    "request_type": "cold_start",
                                    "app_session_id": self.generateUUID(True),  # ,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "badging_event",
                                "time": self.timestamp1(True),  # "1629592340.239",
                                "module": "badging",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "event_type": "impression",
                                    "use_case_id": "profile",
                                    "badge_value": 0,
                                    "badge_position": "bottom_navigation_bar",
                                    "badge_display_style": "dot_badge",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_navigation_tab_impression",
                                "time": self.timestamp1(True),  # "1629592340.249",
                                "module": "feed_timeline",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "app_device_id": self.deviceid,
                                    "headers": [
                                        "main_direct"
                                    ],
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_sessions_chain_update",
                                "time": self.timestamp1(True),  # "1629592340.261",
                                "module": "feed_timeline",
                                "sampling_rate": 1,
                                "extra": {
                                    "sessions_chain": "039:feed_timeline:1",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "navigation",
                                "time": self.timestamp1(True),  # "1629592340.262",
                                "module": "login",
                                "sampling_rate": 1,
                                "extra": {
                                    "click_point": "cold+start",
                                    "nav_depth": 0,
                                    "nav_chain": "039:feed_timeline:1",
                                    "source_module": "login",
                                    "dest_module": "feed_timeline",
                                    "seq": 0,
                                    "nav_time_taken": 124,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_android_story_screenshot_directory",
                                "time": self.timestamp1(True),  # "1629592340.385",
                                "module": "screenshot_detector",
                                "sampling_rate": 1,
                                "extra": {
                                    "screenshot_directory_exists": False,
                                    "phone_model": "MRD-LX1",
                                    "has_read_external_storage_permission": False,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "reel_tray_impression",
                                "time": self.timestamp1(True),  # "1629592340.477",
                                "module": "feed_timeline",
                                "sampling_rate": 1,
                                "extra": {
                                    "has_my_reel": "1",
                                    "viewed_reel_count": 0,
                                    "new_reel_count": 0,
                                    "live_reel_count": 0,
                                    "muted_reel_count": 0,
                                    "muted_live_reel_count": 0,
                                    "unfetched_reel_count": 0,
                                    "tray_position": 0,
                                    "tray_session_id": self.generateUUID(True),
                                    # "507ba942-dc1f-44af-90d6-7b30ec0bcee9",
                                    "viewer_session_id": None,
                                    "is_live_reel": "0",
                                    "is_live_questions_reel": "0",
                                    "is_new_reel": "0",
                                    "reel_type": "story",
                                    "story_ranking_token": None,
                                    "reel_id": self.userid,
                                    "is_besties_reel": False,
                                    "a_pk": self.userid,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_navigation_tab_impression",
                                "time": self.timestamp1(True),  # "1629592340.511",
                                "module": "feed_timeline",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "app_device_id": self.deviceid,
                                    "tabs": [
                                        "main_home",
                                        "main_search",
                                        "main_camera",
                                        "main_inbox",
                                        "main_profile"
                                    ],
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "badging_event",
                                "time": self.timestamp1(True),  # "1629592340.846",
                                "module": "badging",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "event_type": "impression",
                                    "use_case_id": "profile",
                                    "badge_value": 0,
                                    "badge_position": "bottom_navigation_bar",
                                    "badge_display_style": "dot_badge",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "instagram_stories_request_completed",
                                "time": self.timestamp1(True),  # "1629592340.846",
                                "module": "reel_feed_timeline",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "tray_session_id": self.generateUUID(True),  # self.generateUUID(True),#,
                                    "request_type": "cold_start",
                                    "app_session_id": self.generateUUID(True),  # ,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "reel_tray_refresh",
                                "time": self.timestamp1(True),  # "1629592340.849",
                                "module": "feed_timeline",
                                "sampling_rate": 1,
                                "extra": {
                                    "has_my_reel": "1",
                                    "viewed_reel_count": 0,
                                    "new_reel_count": 0,
                                    "live_reel_count": 0,
                                    "muted_reel_count": 0,
                                    "muted_live_reel_count": 0,
                                    "unfetched_reel_count": 0,
                                    "tray_refresh_time": 0.725,
                                    "tray_refresh_type": "network",
                                    "tray_refresh_reason": "cold_start",
                                    "tray_session_id": self.generateUUID(True),  # self.generateUUID(True),#,
                                    "was_successful": True,
                                    "story_ranking_token": self.generateUUID(True),  # ,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "reel_tray_impression",
                                "time": self.timestamp1(True),  # "1629592340.859",
                                "module": "feed_timeline",
                                "sampling_rate": 1,
                                "extra": {
                                    "has_my_reel": "1",
                                    "viewed_reel_count": 0,
                                    "new_reel_count": 0,
                                    "live_reel_count": 0,
                                    "muted_reel_count": 0,
                                    "muted_live_reel_count": 0,
                                    "unfetched_reel_count": 0,
                                    "tray_position": 0,
                                    "tray_session_id": self.generateUUID(True),  # self.generateUUID(True),#,
                                    "viewer_session_id": None,
                                    "is_live_reel": "0",
                                    "is_live_questions_reel": "0",
                                    "is_new_reel": "0",
                                    "reel_type": "story",
                                    "story_ranking_token": self.generateUUID(True),  # ,
                                    "reel_id": self.userid,
                                    "is_besties_reel": False,
                                    "a_pk": self.userid,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "reel_tray_refresh",
                                "time": self.timestamp1(True),  # "1629592341.022",
                                "module": "feed_timeline",
                                "sampling_rate": 1,
                                "extra": {
                                    "has_my_reel": "1",
                                    "viewed_reel_count": 0,
                                    "new_reel_count": 0,
                                    "live_reel_count": 0,
                                    "muted_reel_count": 0,
                                    "muted_live_reel_count": 0,
                                    "unfetched_reel_count": 0,
                                    "tray_refresh_time": 0.899,
                                    "tray_refresh_type": "disk",
                                    "tray_refresh_reason": "cold_start",
                                    "tray_session_id": self.generateUUID(True),  # self.generateUUID(True),#,
                                    "was_successful": False,
                                    "story_ranking_token": self.generateUUID(True),  # ,
                                    "status_code": -1,
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_push_token_registration",
                                "time": self.timestamp1(True),  # "1629592341.151",
                                "module": "push_token_analytics",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "device_id": self.deviceid,
                                    "device_type": "android_mqtt",
                                    "result": "success",
                                    "error": None,
                                    "error_class": None,
                                    "device_sub_type": "1",
                                    "event": "token_result_received",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            },
                            {
                                "name": "ig_push_token_registration",
                                "time": self.timestamp1(True),  # "1629592341.155",
                                "module": "push_token_analytics",
                                "sampling_rate": 1,
                                "tags": 1,
                                "extra": {
                                    "device_id": self.deviceid,
                                    "device_type": "android_mqtt",
                                    "result": "success",
                                    "error": None,
                                    "error_class": None,
                                    "device_sub_type": "2",
                                    "event": "registration_initiated",
                                    "pk": self.userid,
                                    "release_channel": "prod",
                                    "radio_type": "wifi-none"
                                }
                            }
                        ]
                    }
                ]
            }

            ddd80 = urllib.parse.quote(json.dumps(alfa))
            # print("aaaaa", ddd80)

            alfason = 'access_token=' + '567067343352427' + '|' + 'f249176f09e26ce54212b472dbab8fa8' + '&format=json&compressed=' + '0' + '&sent_time=' + self.timestamp1(
                True) + '&message=' + ddd80

            data = alfason

            status = self.SendRequestlogcheksum(data)
            return status
        except Exception as e:
            print(e)
            self.loglarbaslangic4()
            pass

        





    ######### FİNALL ########

    # follow1 ##########

    def useridbul(self):

        link1 = "users/" + self.kullaniciuseridbul + "/usernameinfo/?from_module=deep_link_util"

        self.SendRequestloginsonrasitoplu2get(link1)

        print("çıktı: ", self.json1)

        self.hesapidbul = str(int(self.json1['user']['pk']))
        # print(self.hesapidbul)

        return True

    def hesabigor(self):

        self.followuserid = self.hesapidbul

        link1 = "friendships/show/" + self.followuserid + "/"

        self.SendRequestloginsonrasitoplu2get(link1)

        # print("çıktı: ",self.json1)

        return True

    def follow1(self):

        alfason = {
            "user_id": self.followuserid,
            "radio_type": "wifi-none",
            "_uid": self.userid,
            "device_id": self.androidid,
            "_uuid": self.guid
        }

        ddd80 = urllib.parse.quote(json.dumps(alfason))
        # print("aaaaa", ddd80)

        signature18 = "signed_body=SIGNATURE.{}".format(ddd80)
        # print(signature18)

        link = "friendships/create/" + self.followuserid + "/"

        self.SendRequestloginsonrasitoplu2post(link, signature18)

        print("çıktı: ", self.json1)

        return True

    def discover2(self):

        self.followuserid = self.hesapidbul

        link1 = "discover/chaining/?module=profile&target_id=" + self.followuserid

        self.SendRequestloginsonrasitoplu2get(link1)

        # print("çıktı: ",self.json1)

        return True

    def infowho1(self):

        try:

            link2 = "accounts/current_user/?edit=true"
            status_code = self.SendRequestloginsonrasitoplu2get(link2)

            # print("çıktı: ",self.json1)

            phone_number = str(self.json1["user"]["phone_number"])
            print("phone_number: ", phone_number)

            if phone_number:
                ulke_kodu = str(self.json1["user"]["country_code"])
                print("ulke_kodu: ", ulke_kodu)
            else:
                ulke_kodu = None

            cinsiyet = str(self.json1["user"]["gender"])
            print("cinsiyet: ", cinsiyet)

            email = str(self.json1["user"]["email"])
            print("email: ", email)


        except Exception as e:

            if self.cc < 2:

                self.cc += 1

                print('Hata es geçildi.3')

                print("bbbbbbbbbb", e)
                self.infowho1()

                # pass

            else:
                raise Exception("hesap verilerinde sıkıntı var.  hesap hatalı olarak kaydedildi: ")

        return {'ulke_kodu': ulke_kodu, 'phone_number': phone_number, 'cinsiyet': cinsiyet, 'email': email,
                'status_code': status_code}

    def loglarfollow1(self):

        alfa = alfa = {
            "request_info": {},
            "config": {
                "config_version": "v2",
                "app_uid": self.userid,
                "config_checksum": self.checksum,
                "app_ver": self.appver
            },
            "batches": [
                {
                    "seq": 3,
                    "app_id": "567067343352427",
                    "app_ver": self.appver,
                    "build_num": "289692181",
                    "device_id": self.deviceid,
                    "family_device_id": self.phoneid,
                    "session_id": self.generateUUID(True),
                    "channel": "regular",
                    "log_type": "client_event",
                    "app_uid": self.userid,
                    "claims": [
                        self.claim
                    ],
                    "config_version": "v2",
                    "config_checksum": None,
                    "data": [
                        {
                            "name": "fx_master_account_client_cache",
                            "time": self.timestamp1(True),  # ,
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_name": "cache_eviction",
                                "use_case": "fx_android_internal",
                                "services": None,
                                "debug_data": None,
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "fx_master_account_client_cache",
                            "time": self.timestamp1(True),  # , "1629541231.323",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_name": "cache_access",
                                "use_case": "fx_android_legacy_need_migration",
                                "services": None,
                                "debug_data": {
                                    "caller_class": "9qv"
                                },
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "fx_master_account_client_cache",
                            "time": self.timestamp1(True),  # , "1629541231.337",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_name": "manual_fetch_attempt",
                                "use_case": "app_start",
                                "services": None,
                                "debug_data": {
                                    "caller_class": "BKR"
                                },
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541231.337",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.i.instagram.com/api/v1/wwwgraphql/ig/query/",
                                "url": "https://i.instagram.com/api/v1/wwwgraphql/ig/query/",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541231.409",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.i.instagram.com/api/v1/qp/batch_fetch/",
                                "url": "https://i.instagram.com/api/v1/qp/batch_fetch/",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541231.520",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen&persistentBadging=true&limit=0",
                                "url": "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen&persistentBadging=true&limit=0",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_navigation_tab_impression",
                            "time": self.timestamp1(True),  # , "1629541231.547",
                            "module": "feed_timeline",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "app_device_id": self.deviceid,
                                "headers": [
                                    "main_direct"
                                ],
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541231.553",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.i.instagram.com/api/v1/banyan/banyan/?views=%5B%22story_share_sheet%22%2C%22direct_user_search_Nonestate%22%2C%22forwarding_recipient_sheet%22%2C%22threads_people_picker%22%2C%22direct_inbox_active_now%22%2C%22group_stories_share_sheet%22%2C%22call_recipients%22%2C%22reshare_share_sheet%22%2C%22direct_user_search_keypressed%22%5D",
                                "url": "https://i.instagram.com/api/v1/banyan/banyan/?views=%5B%22story_share_sheet%22%2C%22direct_user_search_Nonestate%22%2C%22forwarding_recipient_sheet%22%2C%22threads_people_picker%22%2C%22direct_inbox_active_now%22%2C%22group_stories_share_sheet%22%2C%22call_recipients%22%2C%22reshare_share_sheet%22%2C%22direct_user_search_keypressed%22%5D",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_xposting_destination_setting",
                            "time": self.timestamp1(True),  # , "1629541231.632",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_name": "server_fetch_success",
                                "ig_account_type": "PERSONAL",
                                "entry_point": "app_start",
                                "user_interaction": False,
                                "target_account_id": None,
                                "target_destination_id": None,
                                "target_destination_type": None,
                                "debug_test_data": {
                                    "page_token_id": ""
                                },
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_xposting_destination_setting",
                            "time": self.timestamp1(True),  # , "1629541231.636",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_name": "local_destination_write",
                                "ig_account_type": "PERSONAL",
                                "entry_point": "legacy_setting_unlink",
                                "user_interaction": False,
                                "target_destination_type": "fb_user",
                                "debug_test_data": {
                                    "server_user_id": "",
                                    "server_page_id": "",
                                    "page_token_id": ""
                                },
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_xposting_destination_setting",
                            "time": self.timestamp1(True),  # , "1629541231.637",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_name": "destination_picker_flag_reset",
                                "ig_account_type": "PERSONAL",
                                "entry_point": "app_start",
                                "user_interaction": False,
                                "debug_test_data": {
                                    "reason": "no_server_link",
                                    "page_token_id": ""
                                },
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "badging_event",
                            "time": self.timestamp1(True),  # , "1629541231.951",
                            "module": "badging",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_type": "impression",
                                "use_case_id": "profile",
                                "badge_value": 0,
                                "badge_position": "bottom_navigation_bar",
                                "badge_display_style": "dot_badge",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541231.966",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.graph.instagram.com/logging_client_events",
                                "url": "https://graph.instagram.com/logging_client_events",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_api_prefetch_usage_event",
                            "time": self.timestamp1(True),  # , "1629541232.063",
                            "module": "api_prefetch_logger",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "ig_user_id": self.userid,
                                "response_fetch_time": self.timestamp2(True),
                                "source": "network",
                                "status": "success",
                                "action": "prefetch",
                                "request_tag": "self.userid_user_info",
                                "response_id": str(random.randint(2000000000, 9999999999)),
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_graphql_subscription_event",
                            "time": self.timestamp1(True),  # , "1629541232.114",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_type": "client_subscribe",
                                "ig_user_id": self.userid,
                                "mqtt_subtopic": "1/graphqlsubscriptions/" + str(random.randint(10000000000000000,
                                                                                                99999999999999999)) + "/{\"input_data\":{\"client_subscription_id\":\"" + self.generateUUID(
                                    True) + "\"}}",  #
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_graphql_subscription_event",
                            "time": self.timestamp1(True),  # , "1629541232.114",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_type": "client_subscribe",
                                "ig_user_id": self.userid,
                                "mqtt_subtopic": "1/graphqlsubscriptions/" + str(random.randint(10000000000000000,
                                                                                                99999999999999999)) + "/{\"input_data\":{\"client_subscription_id\":\"" + self.generateUUID(
                                    True) + "\",\"device_id\":\"" + self.deviceid + "\"}}",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_graphql_subscription_event",
                            "time": self.timestamp1(True),  # , "1629541232.114",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_type": "client_subscribe",
                                "ig_user_id": self.userid,
                                "mqtt_subtopic": "1/graphqlsubscriptions/" + str(random.randint(10000000000000000,
                                                                                                99999999999999999)) + "/{\"input_data\":{\"client_subscription_id\":\"" + self.generateUUID(
                                    True) + "\"}}",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_graphql_subscription_event",
                            "time": self.timestamp1(True),  # , "1629541232.114",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_type": "client_subscribe",
                                "ig_user_id": self.userid,
                                "mqtt_subtopic": "1/graphqlsubscriptions/" + str(random.randint(10000000000000000,
                                                                                                99999999999999999)) + "/{\"input_data\":{\"user_id\":\"self.userid\"}}",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_graphql_subscription_event",
                            "time": self.timestamp1(True),  # , "1629541232.114",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_type": "client_subscribe",
                                "ig_user_id": self.userid,
                                "mqtt_subtopic": "1/graphqlsubscriptions/" + str(random.randint(10000000000000000,
                                                                                                99999999999999999)) + "/{\"input_data\":{\"client_subscription_id\":\"" + self.generateUUID(
                                    True) + "\",\"build_number\":\"289692181\"}}",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541232.378",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.graph.instagram.com/logging_client_events",
                                "url": "https://graph.instagram.com/logging_client_events",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541232.499",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.i.instagram.com/api/v1/android_modules/download/",
                                "url": "https://i.instagram.com/api/v1/android_modules/download/",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_direct_inbox_fetch_success_rate",
                            "time": self.timestamp1(True),  # , "1629541232.561",
                            "module": "ig_direct",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "action": "success",
                                "fetch_uuid": self.generateUUID(True),
                                "fetch_type": "snapshot",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_direct_iris_subscription",
                            "time": self.timestamp1(True),  # , "1629541232.603",
                            "module": "ig_direct_realtime",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "action": "attempt",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_direct_iris_subscription",
                            "time": self.timestamp1(True),  # , "1629541233.009",
                            "module": "ig_direct_realtime",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "action": "success",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_api_prefetch_usage_event",
                            "time": self.timestamp1(True),  # , "1629541233.173",
                            "module": "api_prefetch_logger",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "ig_user_id": self.userid,
                                "response_fetch_time": self.timestamp2(True),
                                "source": "network",
                                "status": "success",
                                "action": "prefetch",
                                "request_tag": "explore_prefetch",
                                "response_id": str(random.randint(2000000000, 9999999999)),
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "fx_master_account_client_cache",
                            "time": self.timestamp1(True),  # , "1629541234.565",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_name": "manual_fetch_success",
                                "use_case": "app_start",
                                "services": None,
                                "debug_data": {
                                    "caller_class": "BKR"
                                },
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "fx_master_account_client_cache",
                            "time": self.timestamp1(True),  # , "1629541234.566",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "event_name": "cache_write",
                                "use_case": "app_start",
                                "services": None,
                                "debug_data": {
                                    "caller_class": "BKR"
                                },
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "follow_button_tapped",
                            "time": self.timestamp1(True),  # , "1629541248.752",
                            "module": "feed_timeline",
                            "sampling_rate": 1,
                            "extra": {
                                "request_type": "create",
                                "nav_events": "[{\"module\":\"login\",\"click_point\":\"cold+start\"}]",
                                "user_id": self.followuserid,
                                "follow_status": "following",
                                "entity_id": self.followuserid,
                                "entity_type": "user",
                                "entity_follow_status": "following",
                                "nav_stack_depth": 0,
                                "nav_stack": None,
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541248.753",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.i.instagram.com/api/v1/friendships/create/" + self.followuserid + "/",
                                "url": "https://i.instagram.com/api/v1/friendships/create/" + self.followuserid + "/",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "recommended_follow_button_tapped",
                            "time": self.timestamp1(True),  # , "1629541248.753",
                            "module": "feed_timeline",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "target_id": self.followuserid,
                                "position": 0,
                                "view_module": "hscroll_aymf_feed_unit",
                                "algorithm": "super_users_algorithm",
                                "view_state_item_type": 0,
                                "container_module": "feed_timeline",
                                "request_type": "create",
                                "follow_status": "following",
                                "follow_impression_id": self.userid + "|" + self.timestamp2(True),
                                # "self.userid|1629325778",
                                "ranking_algorithm": "su_default",
                                "social_context": "Popüler",
                                "insertion_context": None,
                                "display_format": "fish-eye",
                                "netego_unit_id": None,
                                "context_type": None,
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "ig_zero_url_rewrite",
                            "time": self.timestamp1(True),  # , "1629541248.802",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "rewritten_url": "https://z-p42.graph.instagram.com/logging_client_events",
                                "url": "https://graph.instagram.com/logging_client_events",
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                        {
                            "name": "recommended_user_impression",
                            "time": self.timestamp1(True),  # , "1629541248.896",
                            "module": "feed_timeline",
                            "sampling_rate": 1,
                            "tags": 1,
                            "extra": {
                                "target_id": self.followuserid,
                                "position": 0,
                                "follow_impression_id": self.userid + "|" + self.timestamp2(True),
                                # "self.userid|1629325778",
                                "view_module": "hscroll_aymf_feed_unit",
                                "algorithm": "super_users_algorithm",
                                "view_state_item_type": 0,
                                "container_module": "feed_timeline",
                                "follow_impression_length": 134,
                                "ranking_algorithm": "su_default",
                                "social_context": "Popüler",
                                "insertion_context": None,
                                "display_format": None,
                                "netego_unit_id": None,
                                "context_type": None,
                                "pk": self.userid,
                                "release_channel": "prod",
                                "radio_type": "wifi-none"
                            }
                        },
                    ]
                }
            ]
        }

        ddd80 = urllib.parse.quote(json.dumps(alfa))
        # print("aaaaa", ddd80)

        alfason = 'access_token=' + '567067343352427' + '|' + 'f249176f09e26ce54212b472dbab8fa8' + '&format=json&compressed=' + '0' + '&sent_time=' + self.timestamp1(
            True) + '&message=' + ddd80

        data = alfason

        status = self.SendRequestlogtoplu1(data)

        return status

    def followcount(self):

        self.followuserid = self.hesapidbul

        link1 = "users/" + self.followuserid + "/info/?from_module=self_profile" + self.followuserid

        self.SendRequestloginsonrasitoplu2get(link1)

        # print("çıktı: ",self.json1)

        follower_count = str(int(self.json1['user']['follower_count']))
        print("follower_count: ", follower_count)

        return True


    ######### istek yapıları #########

    def SendRequestcookieal1(self):

        headers = {
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-Bloks-Version-Id': self.BloksVersionId,
            'X-IG-WWW-Claim': '0',
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'IG-INTENDED-USER-ID': '0',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'b.i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
        }

        self.urlm1 = 'https://b.i.instagram.com/api/v1/zr/token/result/?device_id=' + self.androidid + '&token_hash=&custom_device_id=' + self.deviceid + '&fetch_reason=token_expired'
        response1b = requests.get(self.urlm1, headers=headers,verify=True,proxies=self.login_after_proxy,timeout=35)
        print("Status1:", response1b.status_code)
        # self.LastResponse1g = response1b

        self.sonmid = response1b.headers
        self.mid = self.sonmid["ig-set-x-mid"]
        # print("mid son: ", self.mid)
        return response1b.status_code






    def SendRequestcookieal2(self):

        

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
            'X-IG-WWW-Claim': '0',
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'IG-INTENDED-USER-ID': '0',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'b.i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
        }
        self.urlm1 = 'https://b.i.instagram.com/api/v1/zr/token/result/?device_id=' + self.androidid + '&token_hash=&custom_device_id=' + self.deviceid + '&fetch_reason=token_expired'
        response1b = requests.get(self.urlm1, headers=headers,verify=True,proxies=self.login_after_proxy,timeout=35)
        print("Status2:", response1b.status_code)
        self.LastResponse1g = response1b

        return response1b.status_code

    def SendRequestlog1(self, post=None):

        

        headers = {
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'zstd, gzip, deflate',
            'Host': 'graph.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'874'
        }
        response2 = requests.post('https://graph.instagram.com/logging_client_events', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestprefill(self, post=None):

        

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
            'X-IG-WWW-Claim': '0',
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'X-MID': self.mid,
            'IG-INTENDED-USER-ID': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'b.i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'117'
        }
        response2 = requests.post('https://b.i.instagram.com/api/v1/accounts/contact_point_prefill/', headers=headers,data=post, verify=True, proxies=self.login_after_proxy, timeout=30)

        print("Status6: ", response2.status_code)

        # print(response2.content)

        return True

    def SendRequest2pwd(self, endpoint, post=None):
        headersbg = {

            "x-device-id": self.deviceid,
            "x-ig-app-locale": "tr_TR",
            "x-ig-device-locale": "tr_TR",
            "x-ig-mapped-locale": "tr_TR",
            "x-pigeon-session-id": self.pigeonid,
            "x-pigeon-rawclienttime": self.timestamp1(True),
            "x-ig-connection-speed": "-1kbps",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-bloks-version-id": self.BloksVersionId,
            "x-ig-www-claim": "0",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-is-panorama-enabled": "false",
            "x-ig-device-id": self.deviceid,
            "x-ig-android-id": self.androidid,
            "x-ig-connection-type": "MOBILE(LTE)",
            "x-ig-capabilities": "3brTvx0=",
            "x-ig-app-id": "567067343352427",
            "user-agent": self.USER_AGENT,
            "accept-language": "tr-TR, en-US",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "content-length": str(post),
            "accept-encoding": "gzip, deflate",
            "x-fb-http-engine": "Liger",
            "x-fb-client-ip": "True",
            "Host": "b.i.instagram.com",

        }
        response2 = requests.post(self.API_URL2 + endpoint, data=post, headers=headersbg,
                                  verify=True, proxies=self.login_after_proxy, timeout=15)  # proxies=proxy
        print("Status1: ", response2.status_code)
        self.LastJsona2 = json.loads(response2.text)
        self.HeadersJsona2 = response2.headers
        self.Cookie = response2.cookies
        # self.csrf = response2.cookies["csrftoken"]
        return True

    def SendRequestlaunch(self, post=None):

        

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
            'X-IG-WWW-Claim': '0',
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'X-MID': self.mid,
            'IG-INTENDED-USER-ID': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'123'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/launcher/sync/', headers=headers, data=post,verify=True, proxies=self.login_after_proxy, timeout=30)

        print("Status6: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestlaunch1b(self, post=None):

        

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
            'X-IG-WWW-Claim': '0',
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'X-MID': self.mid,
            'IG-INTENDED-USER-ID': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'123'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/launcher/sync/', headers=headers,data=post, verify=True, timeout=30, proxies=self.login_after_proxy)

        print("Status6: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestlaunch1c(self, post=None):

        

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            'Host': 'b.i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'190'
        }
        response2 = requests.post('https://b.i.instagram.com/api/v1/launcher/sync/', headers=headers,data=post, verify=True, timeout=30, proxies=self.login_after_proxy)

        print("Status6: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestgetprefill(self, post=None):

        

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
            'X-IG-WWW-Claim': '0',
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'X-MID': self.mid,
            'IG-INTENDED-USER-ID': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
        }
        response2 = requests.post('https://i.instagram.com/api/v1/accounts/get_prefill_candidates/', headers=headers, data=post, verify=True, proxies=self.login_proxy, timeout=30)

        print("Status6: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestgetprefill1a(self, post=None):

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
            'X-IG-WWW-Claim': '0',
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'X-MID': self.mid,
            'Accept-Language': 'tr-TR, en-US',
            'IG-INTENDED-USER-ID': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
        }
        #headers['Content-Length'] = '275'
        response2 = requests.post('https://i.instagram.com/api/v1/accounts/contact_point_prefill/',headers = headers,data=post,verify=True, timeout=30,proxies=self.login_proxy)

        print("Status6: ", response2.status_code)

        #print(response2.content)

        return  response2.status_code

    def SendRequestattribution(self, post=None):



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
            'X-IG-WWW-Claim': '0',
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'X-MID': self.mid,
            'IG-INTENDED-USER-ID': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'83'

        }
        response2 = requests.post('https://i.instagram.com/api/v1/attribution/log_attribution/', headers=headers,data=post, verify=True, proxies=self.login_after_proxy, timeout=30)

        print("Status6: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestlogin(self, post=None):


        try:

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
                'X-IG-WWW-Claim': '0',
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
                'X-MID': self.mid,
                'IG-INTENDED-USER-ID': '0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'z-p42.i.instagram.com',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'Connection': 'keep-alive',
                'Content-Length': str(int(len(post)))
            }
            # print(self.proxyson)
            response2 = requests.post('https://z-p42.i.instagram.com/api/v1/accounts/login/', headers=headers,data=post, verify=True, proxies=self.login_proxy,timeout=30)  # proxies=proxy
            print("Status5: ", response2.status_code)
            print("Status5: ", response2.json())
            # print("Status5: ", response2.headers)

            if response2.status_code == 200:
                self.userid1 = response2.json()['logged_in_user']['pk']
                self.userid = str(int(self.userid1))
                print("userid: ", self.userid)

                self.authorization = response2.headers['ig-set-authorization']
                print("authorization: ", self.authorization)

                self.claim = response2.headers['x-ig-set-www-claim']
                print("claim: ", self.claim)
        except Exception as e:
            print("aaaa ", e)
            pass
        return {'status_code': response2.status_code, 'status5': response2.json()}

    def SendRequesttoken1(self):

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTv10=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'X-MID': self.mid,
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
        self.urlm2 = 'https://b.i.instagram.com/api/v1/zr/token/result/?device_id=' + self.androidid + '&token_hash=&custom_device_id=' + self.deviceid + '&fetch_reason=token_expired'
        response1b = requests.get(self.urlm2, headers=headers,verify=True,proxies=self.login_after_proxy,timeout=35)
        print("Status1:", response1b.status_code)
        # print("Status5: ", response1b.headers)
        self.rur = response1b.headers['ig-set-ig-u-rur']
        # print("rur: ", self.rur)

        return response1b.status_code

    def SendRequestaccountfamily(self):

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTv10=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'X-MID': self.mid,
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
        response2 = requests.get('https://b.i.instagram.com/api/v1/multiple_accounts/get_account_family/',
                                 headers=headers,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)
        # print("Status5: ", response2.headers)
        self.rur = response2.headers['ig-set-ig-u-rur']
        try:
            self.shbid = response2.headers['ig-set-ig-u-shbid']
            print('shbid: ', self.shbid)

            self.shbts = response2.headers['ig-set-ig-u-shbts']
            print('shbts: ', self.shbts)
        except Exception as e:
            self.shbid = None
            #print('shbid: ', self.shbid)

            self.shbts = None
            #print('shbts: ', self.shbts)

            pass
        # print("rur: ", self.rur)
        # print("Status5: ", response2.content)

        return response2.status_code

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTv10=',
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
            'Host': 'b.i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
            'Content-Length': str(int(len(post)))
        }
        response2 = requests.post('https://b.i.instagram.com/api/v1/qe/sync/', headers=headers,data=post, verify=True, proxies=self.login_after_proxy, timeout=30)

        print("Status6: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']
        # print("rur: ", self.rur)

        # print(response2.content)

        return True

    def SendRequestsync2(self, post=None):

        

        headers = {
            'X-DEVICE-ID': self.deviceid,
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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            'Host': 'b.i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
            # 'Content-Length':'10567'
        }
        response2 = requests.post('https://b.i.instagram.com/api/v1/launcher/sync/', headers=headers,data=post, verify=True, proxies=self.login_after_proxy, timeout=30)

        print("Status6: ", response2.status_code)

        self.rur = response2.headers['ig-set-ig-u-rur']
        # print("rur: ", self.rur)

        # print(response2.content)

        return True

    def SendRequestnotifications1(self, post=None):

        

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            'Connection': 'keep-alive'
            # 'Content-Length':'156'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/notifications/badge/', headers=headers,data=post, verify=True, proxies=self.login_after_proxy, timeout=30)

        print("Status6: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']

        # print(response2.content)

        return response2.status_code

    def SendRequestloginsonrasitoplu2post(self, endpoint, post=None):

        

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            # 'Content-Length':'779'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/' + endpoint, headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=15)  # proxies=proxy
        print("Status1: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']
        self.json1 = response2.json()

        return True

    def SendRequestbatchfetch(self, post=None):

        

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            # 'Content-Length':'6840'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/qp/batch_fetch/', headers=headers,data=post, verify=True, proxies=self.login_after_proxy, timeout=15)
        print("Status1: ", response2.status_code)
        print("Status1: ", response2.content)
        self.rur = response2.headers['ig-set-ig-u-rur']
        self.json1 = response2.json()

        return True

    def SendRequestloginsonrasitoplu1post(self, endpoint, post=None):

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            'Connection': 'keep-alive'
            # 'Content-Length':'779'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/' + endpoint, headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=15)  # proxies=proxy
        print("Status1: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']

        return response2.status_code


    def SendRequesttimeline1(self, post=None):

        

        headers = {
            'X-Ads-Opt-Out': '0',
            'X-Google-AD-ID': self.adid,
            'X-DEVICE-ID': self.deviceid,
            'X-CM-Bandwidth-KBPS': '-1.000',
            'X-CM-Latency': str(random.randint(10, 99)) + '.000',
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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            # 'Content-Length':'467'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/feed/timeline/', headers=headers,data=post, verify=True, proxies=self.login_after_proxy, timeout=30)

        print("Status6: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']

        # print(response2.content)

        return response2.status_code

    def SendRequestloginsonrasitoplu2get(self, endpoint):

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
        response2 = requests.get('https://i.instagram.com/api/v1/' + endpoint, headers=headers,verify=True, proxies=self.login_after_proxy, timeout=15)  # proxies=proxy
        print("Status1: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']
        self.json1 = response2.json()
        # print("rur: ", self.rur)
        # print("Status1: ", response2.content)

        return response2.status_code

    def SendRequestloginsonrasitoplu1get(self, endpoint):

        

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'X-MID': self.mid,
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
        response2 = requests.get('https://i.instagram.com/api/v1/' + endpoint, headers=headers,verify=True, proxies=self.login_after_proxy, timeout=15)  # proxies=proxy
        print("Status1: ", response2.status_code)
        print("Status1: ", response2.content)

        self.rur = response2.headers['ig-set-ig-u-rur']
        self.json1 = response2.json()
        # print("rur: ", self.rur)
        # print("Status1: ", response2.content)

        return response2.status_code

    def SendRequestconfigget(self, endpoint):

        

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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'X-MID': self.mid,
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
        response2 = requests.get('https://i.instagram.com/api/v1/' + endpoint, headers=headers,verify=True, proxies=self.login_after_proxy, timeout=15)  # proxies=proxy
        print("Status1: ", response2.status_code)
        print("Status1: ", response2.content)

        self.rur = response2.headers['ig-set-ig-u-rur']
        self.json1 = response2.json()
        # print("rur: ", self.rur)
        # print("Status1: ", response2.content)

        return response2.status_code

    def SendRequestlogcheksum(self, post=None):

        headers = {
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'graph.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
            # 'Content-Length':'874'
        }
        response2 = requests.post('https://graph.instagram.com/logging_client_events', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)
        # print("Status5: ", response2.content)
        # print("Status5: ", response2.json())
        self.checksum = response2.json()['checksum']
        print("checksum: ", self.checksum)
        self.checksum = response2.json()['checksum']
        if not self.checksum:
            self.loglarbaslangic4()

        return response2.status_code

    def SendRequestlogtoplu1(self, post=None):

        

        headers = {
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'graph.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
            # 'Content-Length':'874'
        }
        response2 = requests.post('https://graph.instagram.com/logging_client_events', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestactivate(self, post=None):

        headers = {

            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'graph.facebook.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'230'
        }
        response2 = requests.post('https://graph.facebook.com/v2.3/124024574287414/activities', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestactivate1(self):

        headers = {

            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'graph.facebook.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'230'
        }
        response2 = requests.post('https://graph.facebook.com/v2.3/124024574287414/activities', headers=headers,data=self.payload42, files=self.files1,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)

        # print(response2.content)

        return True

    def SendRequestquery1(self, post=None):

        

        headers = {
            'X-FB-Friendly-Name': 'IGFxLinkedAccountsQuery',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Authorization': self.authorization,
            'X-MID': self.mid,
            'IG-U-DS-USER-ID': self.userid,
            'IG-U-RUR': self.rur,
            # ,48819707837,1658771748:01f766e5abad0eba29a32d19a72e4aa2327431983718d1e5509da5825884c070290edde3'
            'IG-INTENDED-USER-ID': self.userid,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'134'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/wwwgraphql/ig/query/', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)

        # print(response2.content)

        return True

    def SendRequestgraphql1(self, post=None):
        headers = {
                'X-FB-Friendly-Name': 'FxIGMasterAccountQuery',
                'X-IG-Connection-Type': 'MOBILE(LTE)',
                'X-IG-Capabilities': '3brTvx0=',
                'X-IG-App-ID': '567067343352427',
                'User-Agent': self.USER_AGENT,
                'Accept-Language': 'tr-TR, en-US',
                'Authorization': self.authorization,
                'X-MID': self.mid,
                'IG-U-IG-DIRECT-REGION-HINT': 'FRC',
                'IG-U-DS-USER-ID': self.userid,
                'IG-U-RUR': self.rur,
                'IG-INTENDED-USER-ID': self.userid,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'graphql.instagram.com',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'Connection': 'keep-alive'
                }
        #headers['Content-Length'] = '125'
        response2 = requests.post('https://graphql.instagram.com/graphql', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestgraphql2(self, post=None):

        

        headers = {
            'X-FB-Friendly-Name': 'FxIGMasterAccountQuery',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            'Host': 'graphql.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'125'
        }
        response2 = requests.post('https://graphql.instagram.com/graphql', headers=headers,data=post,verify=True, proxies=self.login_after_proxy, timeout=30)  # proxies=proxy
        print("Status5: ", response2.status_code)

        # print(response2.content)

        return response2.status_code

    def SendRequestsync1b(self, post=None):

        

        headers = {
            'X-DEVICE-ID': self.deviceid,
            'X-IG-App-Locale': 'tr_TR',
            'X-IG-Device-Locale': 'tr_TR',
            'X-IG-Mapped-Locale': 'tr_TR',
            'X-Pigeon-Session-Id': self.pigeonid,
            'X-Pigeon-Rawclienttime': self.timestamp1(True),
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-Bloks-Version-Id': self.BloksVersionId,
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'X-MID': self.mid,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'10567'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/qe/sync/', headers=headers,data=post, verify=True, timeout=30, proxies=self.login_proxy)

        print("Status6: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']
        # print("rur: ", self.rur)

        # print(response2.content)

        return response2.status_code

    def SendRequestsync1a(self, post=None):

        

        headers = {
            'X-DEVICE-ID': self.deviceid,
            'X-IG-App-Locale': 'tr_TR',
            'X-IG-Device-Locale': 'tr_TR',
            'X-IG-Mapped-Locale': 'tr_TR',
            'X-Pigeon-Session-Id': self.pigeonid,
            'X-Pigeon-Rawclienttime': self.timestamp1(True),
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-Bloks-Version-Id': self.BloksVersionId,
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'true',
            'X-IG-Device-ID': self.deviceid,
            'X-IG-Family-Device-ID': self.phoneid,
            'X-IG-Android-ID': self.androidid,
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
            'X-IG-App-ID': '567067343352427',
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'tr-TR, en-US',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'10567'
        }
        response2 = requests.post('https://i.instagram.com/api/v1/qe/sync/', headers=headers,data=post, verify=True, timeout=30, proxies=self.login_after_proxy)

        print("Status6: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']
        # print("rur: ", self.rur)

        # print(response2.content)

        return response2.status_code

    def SendRequestsync2a(self, post=None):

        

        headers = {
            'X-DEVICE-ID': self.deviceid,
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
            'X-IG-Timezone-Offset': '3600',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': '3brTvx0=',
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
            'Host': 'b.i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive'
            # 'Content-Length':'10567'
        }
        response2 = requests.post('https://b.i.instagram.com/api/v1/qe/sync/', headers=headers,data=post, verify=True, timeout=30, proxies=self.login_after_proxy)

        print("Status6: ", response2.status_code)

        self.rur = response2.headers['ig-set-ig-u-rur']
        # print("rur: ", self.rur)

        # print(response2.content)

        return response2.status_code

