from django import forms
from django.contrib.auth import models
from .models import ImportFiles,SeoSettings,Article,Mentions,UsersScanner,SeoSettingsNew
from services.models import Services, UserPackpages
from user.models import UsersCategories
from .models import MailSMTPInfo


class SmtpForm(forms.ModelForm):
    
    class Meta:
        model = MailSMTPInfo

        fields  = '__all__'



class UserCategoriesForm(forms.ModelForm):
    
    class Meta:
        model = UsersCategories

        fields  = '__all__'


class ImportFileForm(forms.ModelForm):

    class Meta:
        model = ImportFiles

        fields  = ['file']

class MentionForm(forms.ModelForm):
    
    class Meta:
        model = Mentions

        fields  = ['rootfile']

class UsersScannerForm(forms.ModelForm):
    
    class Meta:
        model = UsersScanner

        fields  = ['rootfile']


class seoFilesForm(forms.ModelForm):

    class Meta:
        model = SeoSettings

        fields  = ['google_tag','ana_title','description','keywords','site_logo','admin_logo','fav_icon','proxy_limit','proxy_limit_video','proxy_limit_login','user_balance','user_logins','process_queue_disabled']

class SeoNewForm(forms.ModelForm):

    class Meta:
        model = SeoSettingsNew

        fields  = '__all__'


class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article

        fields  = ['content']

from api.models import Services as api_services

class UpdateServiceform(forms.ModelForm):

    class Meta:
        model = api_services
        fields  = ['packpages','name','min','max','rate']


class UpdatePackpageform(forms.ModelForm):
    
    class Meta:
        model = UserPackpages
        fields  = ['name','gender','country_code']