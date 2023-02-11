from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from api.views import CustomAuthToken

from root.views import loginView,logoutView,homeView
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('',homeView,name='home'),
    path('login/',loginView,name='login'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('logout/',logoutView,name='logout'),
    path('user/',include('user.urls')),
    #path('api/',include('api.urls')),
    path('api/',include('services.urls')),
    path('custom_admin/',include('custom_admin.urls')),
    path('i/', include('api.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False,
)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
