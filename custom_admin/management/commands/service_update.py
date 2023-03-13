from django.core.management.base import BaseCommand
from api.models import InstagramAccounts
from api.models import Services as new_services
class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        get_services = new_services.objects.all()

        for x in get_services:

            print('[{}] - [max limit:{}]'.format(x.name,x.max))
            if x.packpages:

                if x.packpages.subLocality:
                    instagram_accounts= InstagramAccounts.objects.filter(subLocality=x.packpages.subLocality,locality=x.packpages.locality,country=x.packpages.country)
                elif x.packpages.locality:
                    instagram_accounts= InstagramAccounts.objects.filter(locality=x.packpages.locality,country=x.packpages.country)
                elif x.packpages.country:
                    instagram_accounts= InstagramAccounts.objects.filter(country=x.packpages.country)
                else:
                    instagram_accounts= InstagramAccounts.objects.all()
            else:
                instagram_accounts= InstagramAccounts.objects.all()

            if x.packpages.country_code and x.packpages.gender:
                get_users_count = instagram_accounts.filter(country_code=int(x.packpages.country_code.name),gender=x.packpages.gender).count()
            elif x.packpages.country_code:
                get_users_count = instagram_accounts.filter(country_code=int(x.packpages.country_code.name)).count()
            elif x.packpages.gender:
                get_users_count = instagram_accounts.filter(gender=x.packpages.gender).count()
            else:
                get_users_count = instagram_accounts.count()


            if x.max != get_users_count:

                x.max =  get_users_count
                x.save()
                print('[{}]Uygun kullanıcı sayısı :{} [max limit:{}] Güncellendi.'.format(x.name,get_users_count,get_users_count))
            else:
                print('[{}] - [max limit:{}] Güncel'.format(x.name,get_users_count))

