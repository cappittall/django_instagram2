from user.models import OtherInfo
from django.core.management.base import BaseCommand
from custom_admin.models import SeoSettings

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        allUserInfo = OtherInfo.objects.filter(bot_user=False)
        last_seo = SeoSettings.objects.all().last()

        for oi in allUserInfo:
            
            oi.balance = last_seo.user_balance
            oi.save()


