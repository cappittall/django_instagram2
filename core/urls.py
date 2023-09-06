from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from root.views import logoutView,homeView
from api.views import index
from core.settings import admin_url,custom_admin_url
from custom_admin.views import loginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('{}login/'.format(admin_url), loginView),
    path(admin_url, admin.site.urls),
    path('', index, name='index'),
    #path('login/',loginView,name='login'),
    #path('logout/',logoutView,name='logout'),
    path('user/',include('user.urls')),
    path('api/',include('services.urls')),

    #Password Reset Url
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path(custom_admin_url,include('custom_admin.urls')),
    path('i/', include('api.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)