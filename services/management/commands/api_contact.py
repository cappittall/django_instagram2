from user.models import OtherInfo
from django.core.management.base import BaseCommand
import requests
from services.models import HostKeys
from django.conf import settings as conf_settings

class Command(BaseCommand):


    def handle(self, *args, **kwargs):

        host = conf_settings.ALLOWED_HOSTS[0]
        r = requests.post('https://instatogether.com/api/generated_key/',data={'host':host})
        key = r.json()['created_key']

        HostKeys.objects.create(key=key,host='instatogether.com')
