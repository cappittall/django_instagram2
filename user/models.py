from django.db import models
from django.contrib.auth.models import User




class UsersCategories(models.Model):

    category_name = models.CharField(verbose_name='Kategori Adı',max_length=500)

    def __str__(self):
        return self.category_name

    class Meta:
        
        ordering = ['-id']
        verbose_name_plural = 'Instagram Kullanıcı Kategorileri'
        

class OtherInfo(models.Model):

    user = models.OneToOneField(User,verbose_name='user', on_delete=models.CASCADE)
    picture_url = models.TextField(verbose_name='picture url')
    country_code = models.CharField(max_length=100,verbose_name='Ülke Kodu',blank=True,null=True)
    gender =  models.CharField(max_length=10,verbose_name='Cinsiyet',blank=True,null=True)
    phone = models.CharField(max_length=100,verbose_name="Telefon No",blank=True,null=True)
    balance = models.IntegerField(default=0,verbose_name='balance')
    default_user = models.BooleanField(verbose_name="Normal Kullanıcı",default=True)
    bot_user = models.BooleanField(verbose_name="bot instagram user",default=False)
    category = models.ManyToManyField(UsersCategories,blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
    
        ordering = ['-id']
        verbose_name_plural = 'Kullanıcı Bilgileri'
    
class InstagramCookies(models.Model):
    
    user = models.OneToOneField(User,verbose_name='user', on_delete=models.CASCADE)
    default_password = models.CharField('password',max_length=250)
    userid = models.CharField(verbose_name='userid',max_length=1000)
    authorization = models.CharField(verbose_name='authorization',max_length=1000)
    claim = models.CharField(verbose_name='claim',max_length=1000)
    phoneid = models.CharField(verbose_name='phoneid',max_length=1000)
    pigeonid = models.CharField(verbose_name='pigeonid',max_length=1000)
    rur = models.CharField(verbose_name='rur',max_length=1000)
    mid = models.CharField(verbose_name='mid',max_length=1000)
    waterfallid = models.CharField(verbose_name='waterfallid',max_length=1000)
    deviceid = models.CharField(verbose_name='deviceid',max_length=1000)
    androidid = models.CharField(verbose_name='androidid',max_length=1000)
    user_agent = models.CharField(verbose_name='user_agent',max_length=1000)
    guid = models.CharField(verbose_name='guid',max_length=1000)
    adid = models.CharField(verbose_name='adid',max_length=1000)
    key = models.CharField(verbose_name='key',max_length=1000,blank=True)
    checksum = models.CharField(verbose_name='checksum',max_length=1000,blank=True)
    active = models.BooleanField(verbose_name="Hesap Aktifliği",default=True)
    device_type = models.CharField('device_type',max_length=250)
    brand = models.CharField('brand',max_length=250)
    manufacturer = models.CharField('manufacturer',max_length=250)
    os_type = models.CharField('os_type',max_length=250)
    os_ver = models.CharField('os_ver',max_length=250)
    error_count = models.IntegerField(default=0,verbose_name="ard arda hata sayısı")
    challenge = models.BooleanField(default=False,verbose_name='challenge durumu')
    feedback  = models.BooleanField(default=False,verbose_name='feedback durumu')
    checkpoint  = models.BooleanField(default=False,verbose_name='checkpoint durumu')
    login_required  = models.BooleanField(default=False,verbose_name='login_required durumu')
    new_account = models.BooleanField(default=True,verbose_name='new_account durumu')
    old_account = models.BooleanField(default=False,verbose_name='old_account durumu')
    ck_data = models.TextField(verbose_name='ck,cs,sr,di,ds data',blank=True)
    register_key = models.TextField(verbose_name='register key',blank=True)
    web_socket_controling = models.BooleanField(default=False,verbose_name='web socket control')
    last_process_time = models.IntegerField(default=0,verbose_name='Son İşlem Zamanı')

    def __str__(self):
        return self.user.username

    class Meta:

        ordering = ['-id']
        verbose_name_plural = 'Kullanıcıların Instagmram Cookieleri'

