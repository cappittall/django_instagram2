from statistics import mode
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from user.models import UsersCategories
from django.utils.translation import ugettext_lazy as _

class CategoryType(models.Model):
    type_name = models.CharField(verbose_name="Type",max_length=250)

    class Meta:

        verbose_name_plural = 'Servis Type'
        ordering = ['-id']

    def __str__(self):
        return self.type_name

class ServiceCategory(models.Model):
    category_name = models.CharField(verbose_name="Kategori",max_length=250)
    category_type = models.ForeignKey(CategoryType,on_delete=models.CASCADE,verbose_name='Type')

    class Meta:
    
        verbose_name_plural = 'Servis Kategorileri'
        ordering = ['-id']

    def __str__(self):
        return self.category_name



class Genders(models.Model):

    name = models.CharField(verbose_name="Cinsiyet",max_length=1)


    def __str__(self):

        return self.name

    class Meta:

        ordering = ['-id']
        verbose_name_plural = 'Cinsiyetler'


class CountryCodes(models.Model):
    name = models.CharField(verbose_name="Ülke Kodu",max_length=50)

    def __str__(self):
        return self.name

    class Meta:

        ordering = ['-id']
        verbose_name_plural = 'Ülke Kodları'

class UserPackpages(models.Model):

    name = models.CharField(verbose_name="Paket Adı",max_length=150)
    gender = models.ForeignKey(Genders,on_delete=models.CASCADE,verbose_name='Cinsiyet',null=True,blank=True)
    country_code =models.ForeignKey(CountryCodes,on_delete=models.CASCADE,verbose_name='Ülke Kodu',null=True,blank=True)
    category = models.ManyToManyField(UsersCategories,blank=True)

    def __str__(self):
        return self.name


    class Meta:

        ordering = ["-id"]
        verbose_name_plural = 'Kullanıcı Paketleri'


class Services(models.Model):
    
    service = models.AutoField(primary_key=True,verbose_name="ID")
    packpages = models.ForeignKey(UserPackpages,on_delete=models.CASCADE,verbose_name="Kullanıcı Paketi",null=True,blank=True)
    category = models.ForeignKey(ServiceCategory,verbose_name='Kategori',on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Servis İsmi",max_length=150)
    rate = models.FloatField(default=150.0,verbose_name=_('Fiyat'))
    min = models.IntegerField(default=0,verbose_name="min")
    max = models.IntegerField(default=0,verbose_name="max")
    dripfeed = models.BooleanField(default=False,verbose_name="dripfeed")
    refill = models.BooleanField(default=True,verbose_name="refill")


    class Meta:

        verbose_name_plural = "Servisler"
        ordering = ['-service']

    def __str__(self):
        return self.name



class ServicesSuccessfulLog(models.Model):

    service_id = models.CharField(verbose_name='servis id',max_length=100)
    service_name = models.CharField(verbose_name='Servis Adı',max_length=500)
    successful_value = models.IntegerField(verbose_name='Başarılı İşlem Sayısı',default=0)

    def __str__(self):

        return self.service_name

    class Meta:
        verbose_name_plural = 'Başarılı İşlem Kayıtları'

class Orders(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='user')
    service = models.ForeignKey(Services,on_delete=models.CASCADE,verbose_name='service',blank=True,null=True)
    charge = models.FloatField(default=0,verbose_name='charge')
    start_count = models.IntegerField(default=0,verbose_name="start_count")
    status = models.CharField(verbose_name='status',max_length=50)
    remains = models.IntegerField(default=0,verbose_name="remains")
    currency = models.CharField(verbose_name='currency',max_length=10)
    successful_value = models.IntegerField(default=0,verbose_name="Başarılı İşlem Miktarı")
    process = models.IntegerField(default=0,verbose_name="İşlem Sayısı")
    cancelled = models.BooleanField(default=False,verbose_name="İptal Durumu")
    target = models.CharField(verbose_name='Hedef',max_length=500)
    user_order = models.BooleanField(default=False,verbose_name="Kullanıcı Siparişi")
    auto_process = models.BooleanField(default=False,verbose_name="Oto İşlem")

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Siparişler'


class Affirmations(models.Model):

    order = models.ForeignKey(Orders,on_delete=models.CASCADE,verbose_name='order')
    service = models.ForeignKey(Services,on_delete=models.CASCADE,verbose_name='service')
    users = models.TextField(verbose_name='Hedef Kullanıcılar',blank=True,null=True)
    target_user = models.CharField(verbose_name='target_user',max_length=250,blank=True,null=True)
    users_value = models.IntegerField(verbose_name='Hedef Kullanıcı Sayısı',default=0)
    media_link = models.CharField(verbose_name='Media Link',max_length=500)
    message1 = models.TextField(verbose_name='Media Mesajı')
    link = models.CharField(verbose_name='Link',max_length=500)
    message2 = models.TextField(verbose_name='Link Mesajı')
    date = models.DateTimeField(verbose_name='Tarih',auto_now_add=True)
    user_follower_scanner = models.BooleanField(default=False)

    def __str__(self):
        return self.media_link

    class Meta:

        ordering = ['id']
        verbose_name_plural = 'Api Sipariş Onaylamaları'


class Keys(models.Model):
    key = models.CharField(default=0, verbose_name="API-KEY", max_length=50)
    createdby = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Created by")
    creatdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class HostKeys(models.Model):
    
    key = models.CharField(default=0, verbose_name="API-KEY", max_length=50)
    host = models.CharField(verbose_name='Sağlayıcı',max_length=150)
    creatdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
