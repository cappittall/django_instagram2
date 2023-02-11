
from django.urls import path
from .views import getServices,outData,generateKey,outUserInfo

urlpatterns = [
    path('get_services/',getServices),
    path('out_data/',outData),
    path('out_user_info/',outUserInfo),
    path('generated_key/',generateKey),
]

