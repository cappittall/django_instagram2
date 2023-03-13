from django.contrib import admin
from .models import (Proxy,SeoSettings,ImportFiles,NotLoginUsers,GetFollowDataLog,AutoLikeUser,
                AutoLikeUserLog,AutoLikeQueue,Mentions,UsersScanner,AutoFollowUser,AutoFollowQueue,AutoFollowUserLog,SmsLoginLog,SMSApi)

admin.site.register(Proxy)
admin.site.register(SeoSettings)
admin.site.register(ImportFiles)
admin.site.register(NotLoginUsers)
admin.site.register(GetFollowDataLog)
admin.site.register(AutoLikeUser)
admin.site.register(AutoLikeUserLog)
admin.site.register(AutoLikeQueue)
admin.site.register(Mentions)
admin.site.register(UsersScanner)

admin.site.register(AutoFollowUser)
admin.site.register(AutoFollowQueue)
admin.site.register(AutoFollowUserLog)
admin.site.register(SmsLoginLog)
admin.site.register(SMSApi)







