from django.contrib import admin

from api.models import Profil, InstagramAccounts, Services, ServicePrices, EarnList, OrderList, BalanceRequest, InstagramVersions
# Register your models here.
admin.site.register(Profil)
admin.site.register(InstagramAccounts)
admin.site.register(EarnList)
admin.site.register(ServicePrices)
admin.site.register(Services)
admin.site.register(OrderList)
admin.site.register(BalanceRequest)
admin.site.register(InstagramVersions)
