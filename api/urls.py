from django.urls import path, include
from api import views
from api.consumers import ApiConsumer
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
router = DefaultRouter()

router.register(r'users', views.UserViewSet )
router.register(r'profile', views.ProfilViewSet )
router.register(r'instagram', views.InstagramViewSet )
router.register(r'serviceprices', views.ServicesPriceViewSet )
router.register(r'earnlist', views.EarnListViewSet )
router.register(r'orders', views.OrdersViewSet )
router.register(r'balancerequest', views.BalanceRequestViewSet )
router.register(r'versioncontrol', views.VersionControlViewSet )




urlpatterns = [
    # Below imported more functional user paths 
    path('api/', include(router.urls) ),
    path('update-location/', views.update_location, name="update-location"),  # type: ignore
    path('get_image_urls/', views.get_image_urls, name="get-image-urls"),  # type: ignore
    path('api/get_services/', views.getServices, name='get-services'),   # type: ignore
    path('api/privacy-policy/', views.privacyPolicy, name='privacy-policy'),   # type: ignore
    path('api/kazanctablosu/', views.kazancTablosu, name='kazanc-tablosu'),   # type: ignore
    path('websocket/', views.messages, name="messages"),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api-token-auth'),
    path('jibAaQNZD30RwR+82JIcogQVs8LClBbMrm9/tyJm3ig=/', views.returnAdminToken, name='admin-token'),
    
]
