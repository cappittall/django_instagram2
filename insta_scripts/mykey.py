import hashlib
import datetime
from time import sleep
import time
import urllib
import uuid
import random
import requests
from queue import Queue
import json
import urllib.parse
from datetime import datetime
import base64
import json
import os
import sys
import socket
import tempfile

import base64
import time
from random import randint
import hmac
import hashlib

from pathlib import Path
from user.models import InstagramCookies
BASE_DIR = Path(__file__).resolve().parent.parent


class GetMyKey:

    def __init__(self, username='', password='', dm_user=''):

        self.username = username
        self.password = password
        self.kullaniciuseridbul = dm_user
        self.BloksVersionId = '54a609be99b71e070ffecba098354aa8615da5ac4ebc1e44bb7be28e5b244972'
        self.deviceid = ''
        self.userid = ''
        self.claim = ''
        self.authorization = ''
        self.checksum = ''
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
        self.dm_message_count = 0
        self.error_users = []
        self.success_users = []
        self.cookie_user_id = 0

        self.ip_port_proxy = None
        self.auth_proxy = None
        self.root_proxy = None

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

    # user_agent = "Instagram 187.0.0.32.120 Android (28/9; 360dpi; 720x1422; HUAWEI; MRD-LX1; HWMRD-M1; mt6761; tr_TR; 289692181)"

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

    def gen_user_breadcrumb(self, size):

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

    def dmMessageStart(self, cookie_user_id, message, ip_port_proxy, auth_proxy, db_pigeonid, db_claim, db_deviceid,
                       db_phoneid, db_androidid, db_USER_AGENT, db_checksum, db_authorization, db_mid, db_userid,
                       db_rur, db_waterfallid, db_adid, db_guid, db_mykey):
        self.dmmesaj = message

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

        self.appver = '212.0.0.38.119'

        ########

        veriler = self.user_agent_compile(self.db_USER_AGENT)
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

        ##

        ### işlem başlangıç  ####
        statusDM = False
        try:
            ## DM mykey alma ##

            self.banyan2()


            self.success_users.append(self.cookie_user_id)


        except Exception as e:
            self.error_users.append(self.cookie_user_id)
            print(e)

        return statusDM

    #### DM MYKEY #######


    def banyan2(self):


        self.SendRequestloginsonrasitoplu2get(
            'banyan/banyan/?views=%5B%22story_share_sheet%22%2C%22direct_user_search_nullstate%22%2C%22forwarding_recipient_sheet%22%2C%22threads_people_picker%22%2C%22direct_inbox_active_now%22%2C%22group_stories_share_sheet%22%2C%22call_recipients%22%2C%22reshare_share_sheet%22%2C%22direct_user_search_keypressed%22%5D')

        print("aaa: ",self.json1)
        catak = self.json1['ranking'][1]['score_map']
        print(catak)

        keys_ = catak.keys()
        self.mykey = ''
        for x in keys_:
            if len(x) == 39:
                self.mykey = x
        print(self.mykey)


        return True

    ####################

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
            'X-IG-Capabilities': '3brTvx0=',
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
            'Connection': 'keep-alive'
        }
        response2 = requests.get('https://i.instagram.com/api/v1/' + endpoint, headers=headers, proxies=self.root_proxy,verify=True, timeout=15)
        print("Status1: ", response2.status_code)
        self.rur = response2.headers['ig-set-ig-u-rur']
        self.json1 = response2.json()

        try:

            message = self.json1['message']
            get_user_oi = InstagramCookies.objects.filter(user__id=self.cookie_user_id).last()

            if get_user_oi:

                
                if message == 'feedback_required':
                    get_user_oi.feedback = True
                    get_user_oi.active = False
                    get_user_oi.save()
                elif message == 'challenge_required':
                    get_user_oi.challenge = True
                    get_user_oi.active = False
                    get_user_oi.save()
                elif message == 'checkpoint_required':
                    get_user_oi.checkpoint = True
                    get_user_oi.active = False
                    get_user_oi.save()
                elif message == 'login_required':
                    get_user_oi.login_required = True
                    get_user_oi.active = False
                    get_user_oi.save()        
        except:
            pass
        # print("rur: ", self.rur)
        # print("Status1: ", response2.content)

        return True

