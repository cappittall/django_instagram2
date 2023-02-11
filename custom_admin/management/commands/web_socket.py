import threading
from django.core.management.base import BaseCommand
from pathlib import Path
from core.get_path import outpath
from insta_scripts.serilog import Scanner
from custom_admin.models import Proxy,SeoSettings
BASE_DIR = Path(__file__).resolve().parent.parent
import random
from django.contrib.auth.models import User
from user.models import InstagramCookies


import logging
import json
import os
import pickle
import sys
import asyncio
from datetime import datetime
from instagram_private_api import Client, ClientCookieExpiredError, ClientLoginRequiredError
from dateutil.relativedelta import relativedelta
from fbns_mqtt.fbns_mqtt import FBNSMQTTClient, FBNSAuth
from urllib.parse import urlsplit, parse_qs


################################################


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)




class ExtendedClient(Client):
    pass


stop={}
client={}
async def instagram_listener_worker(m,data):
    

    ### İçeri aldım (Fonksiyon dışındaydı, her tread için ayrı ayrı gerekir)
    client[m] = FBNSMQTTClient()
    stop[m] = asyncio.Event()
   

    print("777 >> Client : ", client[m])
    user_register_key =  json.loads(str(data.register_key.replace("'",'"')))
    user_ck_data = json.loads(str(data.ck_data.replace("'",'"')))
    fbns_auth = user_ck_data


    if fbns_auth:
        client[m].set_fbns_auth(FBNSAuth(fbns_auth))
        print("555 ",FBNSAuth(fbns_auth))


    def on_fbns_auth(auth):
        fbns_auth = user_ck_data
        fbns_auth_received = datetime.now()
        print("a22222222222", auth)


    def on_fbns_token(token):
        fbns_token = user_register_key

        fbns_token_received = datetime.now()
        print("a33333333333", token)

    def on_fbns_message(push):
        if push.payload:
            notification = InstagramNotification(push.payload)
            print("44444",push.payload)
            if notification.collapseKey == 'comment':
                print("aaaa: ",notification.message)
            elif notification.collapseKey == 'direct_v2_message':
                print("bbb: ",notification.it)

    client[m].on_fbns_auth = on_fbns_auth
    print("11111",on_fbns_auth)
    client[m].on_fbns_token = on_fbns_token
    print("22222",on_fbns_token)
    client[m].on_fbns_message = on_fbns_message
    print("333333",on_fbns_message)

    await client[m].connect('mqtt-mini.facebook.com', 443, ssl=True, keepalive=900)
    await stop[m].wait()
    await client[m].disconnect()






def _spop(d, k):
    if k in d:
        return d.pop(k)
    return None

class BadgeCount(object):
    def __init__(self, data):
        print("a4444444", data)

        if isinstance(data,str):

            data = json.loads(data)
        self.direct = _spop(data, 'di')
        self.ds = _spop(data, 'ds')
        self.td = _spop(data, 'dt')
        self.activities = _spop(data, 'ac')
        if data:
            raise Exception('BadgeCount unexpected data: {data}'.format(**locals()))


class InstagramNotification(object):
    def __str__(self):
        return str(self.__dict__)

    def __init__(self, data):
        print("a55555555555555", data)

        if isinstance(data, str):
            print("a9000000", data)
            data = json.loads(data)

        # For sentry debug
        original_data = dict(data)

        self.title = _spop(data, 't')
        self.message = _spop(data, 'm')
        self.tickerText = _spop(data, 'tt')

        self.igAction = _spop(data, 'ig')
        self.actionPath = None
        self.actionParams = None

        if self.igAction:
            scheme, netloc, path, query_string, fragment = urlsplit(self.igAction)
            query_params = parse_qs(query_string)
            query_params = dict((k, v if len(v) > 1 else v[0]) for k, v in query_params.items())
            if path:
                self.actionPath = path
            if query_params:
                self.actionParams = query_params

        self.collapseKey = _spop(data, 'collapse_key')
        self.optionalImage = _spop(data, 'i')
        self.optionalAvatarUrl = _spop(data, 'a')
        self.sound = _spop(data, 'sound')
        self.pushId = _spop(data, 'pi')
        if 'PushNotifID' in data:
            _spop(data, 'PushNotifID')

        self.pushCategory = _spop(data, 'c')

        # Идентификатор чей пост прокомментировали
        self.intendedRecipientUserId = _spop(data, 'u')
        self.sourceUserId = _spop(data, 's')
        self.igActionOverride = _spop(data, 'igo')
        self.badgeCount = _spop(data, 'bc')
        if self.badgeCount:
            self.badgeCount = BadgeCount(self.badgeCount)
        self.inAppActors = _spop(data, 'ia')
        self.suppressBadge = _spop(data, 'SuppressBadge')

        self.it = _spop(data, 'it')
        self.si = _spop(data, 'si')
        self.badge = _spop(data, 'badge')

        if data:
            raise Exception('InstagramNotification unexpected data: {data}'.format(**locals()))




class Command(BaseCommand):

    async def main(self,x,users):

        await asyncio.gather(*(instagram_listener_worker(i,data=users[i]) for i in range(x)))

    def handle(self, *args, **kwargs):

        users = InstagramCookies.objects.filter(active=True,user__is_superuser=False)
        asyncio.run(self.main(x=len(users),users=users))
