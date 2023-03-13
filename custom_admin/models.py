from django.db import models
from services.models import Orders
from ckeditor.fields import RichTextField


class Article(models.Model):
    content = RichTextField(verbose_name='İçerik', blank=True)

    class Meta:
        ordering = ['-id']


class ImportFiles(models.Model):

    file = models.FileField(verbose_name="Dosya",upload_to="user_data")
    class Meta:

        verbose_name_plural = "Kullanıcı Import Dosyaları"

class Mentions(models.Model):
    
    rootfile = models.FileField(verbose_name="Dosya",upload_to="mentionlogs")
    status = models.BooleanField(verbose_name='Durum',default=False)
    date = models.DateTimeField(verbose_name="date",auto_now_add=True)

    def __str__(self):
    
        return str(self.date)

    class Meta:

        verbose_name_plural = "Mention Kontrol Kayıtları"
        ordering = ['-date']


class UsersScanner(models.Model):
    
    rootfile = models.FileField(verbose_name="Dosya",upload_to="usersscannerlogs")
    status = models.BooleanField(verbose_name='Durum',default=False)
    date = models.DateTimeField(verbose_name="date",auto_now_add=True)

    def __str__(self):
    
        return str(self.date)

    class Meta:

        verbose_name_plural = "Kullanıcı Tarama Kayıtları"
        ordering = ['-date']


class Proxy(models.Model):
    
    proxy = models.CharField(verbose_name="Proxy",max_length=1000)
    ip_port_proxy = models.BooleanField(default=False,verbose_name="İp Port Proxy")
    
    auth_proxy = models.BooleanField(default=False,verbose_name="Şifreli Proxy")
    login_after_proxy = models.BooleanField(default=False,verbose_name="Login Öncesi Proxy")
    login_proxy = models.BooleanField(default=False,verbose_name="Login Proxy")
    process_proxy = models.BooleanField(default=False,verbose_name="İşlem Proxy")
    auto_process_proxy = models.BooleanField(default=False,verbose_name="Oto İşlem Proxy")
    video_proxy = models.BooleanField(default=False,verbose_name='Video İzleme Proxy')
    
    def __str__(self):

        return self.proxy

    class Meta:

        verbose_name_plural = "Proxyler"
        ordering = ['-id']



class SeoSettings(models.Model):
    
    google_tag = models.CharField(verbose_name="google tag kodu",max_length=100)
    ana_title = models.CharField(verbose_name="site başlığı",max_length=1000)
    description = models.CharField(verbose_name="description, açıklama",max_length=1000)
    keywords = models.CharField(verbose_name="keywords , anahtar kelimeler",max_length=1000)
    site_logo =  models.ImageField(verbose_name='Site Logo')
    admin_logo =  models.ImageField(verbose_name='Admin Logo')
    fav_icon =  models.ImageField(verbose_name='Fav İcon')
    proxy_limit = models.IntegerField(verbose_name="Proxy anlık işlem limiti ",default=1)
    proxy_limit_video = models.IntegerField(verbose_name="Video izleme thread limiti ",default=1)
    proxy_limit_login = models.IntegerField(verbose_name="User ekleme thread limiti ",default=1)
    user_balance = models.IntegerField(verbose_name="Kullanıcı Kredi Yenileme Miktarı ",default=0)
    user_logins = models.BooleanField(default=True,verbose_name="Dışarıdan instagram kullanıcı Girişleri")
    process_queue_disabled = models.BooleanField(default=False,verbose_name="İşlem Sırasını Devre Dışı Bırak")
    
    class Meta:

        verbose_name_plural = "Seo ve Genel ayarlar"

        ordering = ['-id']

class SeoSettingsNew(models.Model):
    
    google_tag = models.CharField(verbose_name="google tag kodu",max_length=100,blank=True,null=True)
    
    site_title = models.CharField(verbose_name="site başlığı",max_length=1000,blank=True,null=True)
    description = models.CharField(verbose_name="description, açıklama",max_length=1000,blank=True,null=True)
    keywords = models.CharField(verbose_name="keywords , anahtar kelimeler",max_length=1000,blank=True,null=True)

    play_store_link = models.CharField(verbose_name='Play Store Linki',max_length=250,blank=True,null=True) 

    company_name = models.CharField(verbose_name='Marka/Şirket Adı',max_length=50,blank=True,null=True) 
    site_message = models.CharField(verbose_name='Site Sol Mesaj',max_length=1000,blank=True,null=True)

    twitter_link = models.CharField(verbose_name='Twitter Linki',max_length=250,blank=True,null=True)
    facebook_link = models.CharField(verbose_name='Facebook Linki',max_length=250,blank=True,null=True)
    instagram_link = models.CharField(verbose_name='Instagram Linki',max_length=250,blank=True,null=True)

    fav_icon =  models.ImageField(verbose_name='Fav İcon')


    class Meta:

        verbose_name_plural = "Seo ve Genel ayarlar (Yeni)"
        ordering = ['-id']


class NotLoginUsers(models.Model):

    user = models.CharField(verbose_name='user',max_length=250,null=True,blank=True)

    class Meta:

        verbose_name_plural = "Giriş Yapamayan Kullanıcılar"
        ordering = ['-id']


class GetFollowDataLog(models.Model):

    username = models.CharField(verbose_name='Username',max_length=250)
    users_list_username = models.TextField(verbose_name='Kullanıcı Listesi Username',default='') 
    users_list_user_id = models.TextField(verbose_name='Kullanıcı Listesi User Id',default='')
    success =  models.BooleanField(default=False,verbose_name="Tamamlanma Durumu")
    cancelled = models.BooleanField(default=False,verbose_name="İptal Durumu")
    sending_mail = models.BooleanField(default=False,verbose_name="Sistem Tarafından Mail Gönderilme Durumu")
    usersValue = models.IntegerField(default=0,verbose_name='Çekin Takipçi Sayısı')
    api_order = models.ForeignKey(Orders,on_delete=models.CASCADE,verbose_name='API Order',null=True,blank=True)
    api_contact_mail = models.CharField(verbose_name='Api Siparişi İletişim Maili',max_length=250,null=True,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):

        return self.username

    class Meta:
        verbose_name_plural = "Kullanıcı Takipçilerini Getirme"
        ordering = ['-id']



class AutoLikeUser(models.Model):
    username = models.CharField(verbose_name="Kullanıcı Adı",max_length=150)
    quantity = models.IntegerField(default=0,verbose_name="Beğeni Miktarı")
    timeout = models.IntegerField(default=0,verbose_name="Emir Süresi (Gün)")
    date = models.DateTimeField(auto_now_add=True,verbose_name='Emir Tarihi')
    order = models.ForeignKey(Orders,on_delete=models.CASCADE,verbose_name='order')

    def __str__(self):
    
        return self.username

    class Meta:
        verbose_name_plural = "Oto Post Beğeni Kullanıcılar"
        ordering = ['-id']


class AutoLikeUserLog(models.Model):
    auto_like_user = models.ForeignKey(AutoLikeUser,on_delete=models.CASCADE,verbose_name='Auto Like')
    media_id = models.CharField(verbose_name='post media id',max_length=250)

    def __str__(self):
    
        return self.media_id

    class Meta:
        verbose_name_plural = "Oto Post Beğeni Kullanıcı Log"
        ordering = ['-id']


class AutoLikeQueue(models.Model):
    auto_like_user = models.ForeignKey(AutoLikeUser,on_delete=models.CASCADE,verbose_name='Auto Like')
    success = models.BooleanField(default=False,verbose_name="Oto Beğeni İşlem Sırası")
    successful_value =  models.IntegerField(default=0,verbose_name="Başarılı İşlem")
    media_id = models.CharField(verbose_name='post media id',max_length=250)

    def __str__(self):
        
        return str(self.success)

    class Meta:
        verbose_name_plural = "Oto Post Beğeni İşlem Sırası"
        ordering = ['-id']



class AutoFollowUser(models.Model):
    username = models.CharField(verbose_name="Kullanıcı Adı",max_length=150)
    quantity = models.IntegerField(default=0,verbose_name="Beğeni Miktarı")
    date = models.DateTimeField(auto_now_add=True,verbose_name='Emir Tarihi')
    order = models.ForeignKey(Orders,on_delete=models.CASCADE,verbose_name='order')

    def __str__(self):
    
        return self.username

    class Meta:
        verbose_name_plural = "Oto Follow Kullanıcılar"
        ordering = ['-id']


class AutoFollowUserLog(models.Model):
    auto_follow_user = models.ForeignKey(AutoFollowUser,on_delete=models.CASCADE,verbose_name='Auto Like')
    user_id = models.CharField(verbose_name='user_id',max_length=250)
    username = models.CharField(verbose_name="Kullanıcı Adı",max_length=250)

    def __str__(self):
    
        return self.user_id

    class Meta:
        verbose_name_plural = "Oto Follow Kullanıcı Log"
        ordering = ['-id']


class AutoFollowQueue(models.Model):
    auto_follow_user = models.ForeignKey(AutoFollowUser,on_delete=models.CASCADE,verbose_name='Auto Follow')
    success = models.BooleanField(default=False,verbose_name="Oto Follow İşlem Sırası")
    successful_value =  models.IntegerField(default=0,verbose_name="Başarılı İşlem") 
    target_user = models.CharField(verbose_name='hedef user',max_length=250)

    def __str__(self):
        
        return str(self.success)

    class Meta:
        verbose_name_plural = "Oto Follow İşlem Sırası"
        ordering = ['-id']



class MailSMTPInfo(models.Model):
    
    EMAIL_HOST = models.CharField(verbose_name="Email Host",max_length=100)
    EMAIL_PORT = models.IntegerField(verbose_name="Email Port",default=0)
    EMAIL_HOST_USER = models.CharField(verbose_name="EMAIL_HOST_USER(Email)",max_length=100)
    EMAIL_HOST_PASSWORD = models.CharField(verbose_name="EMAIL_HOST_PASSWORD(Password)",max_length=100)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Mail SMTP Bilgileri'



class VideoSayacLog(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE,verbose_name='order')
    sayac_value = models.IntegerField(verbose_name='sayac value',default=0)


from django.contrib.auth.models import User

class SmsLoginLog(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='user')
    ip = models.CharField(verbose_name='ip',max_length=50)
    session_id = models.CharField(verbose_name='session_id',max_length=100)
    code = models.CharField(verbose_name='Kod',max_length=6)
    date = models.DateTimeField(auto_now_add=True,verbose_name='Tarih')
    remaining = models.IntegerField(default=3,verbose_name='Kalan')

    class Meta:

        ordering = ['-date']
        verbose_name_plural = 'SMS Onay Kodları'

    

class SMSApi(models.Model):

    username = models.CharField(verbose_name='username',max_length=50)
    password = models.CharField(verbose_name='password',max_length=50)

    class Meta:
    
        ordering = ['-id']
        verbose_name_plural = 'SMS Api Bilgileri'