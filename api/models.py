
from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Profil(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    token=models.CharField(max_length=50, blank=True, )
    phone=models.CharField(max_length=20, blank=True, default="")
    birth_date=models.DateTimeField(default=timezone.now, blank=True,)  
    tc=models.CharField(max_length=15, blank=True, default='')
    iban=models.CharField(max_length=50, default='TR',  blank=True)
    bank=models.CharField(max_length=50, default='Banka', blank=True )
    coin=models.CharField(max_length=50, default='', blank=True)
    coin_adresi=models.CharField(max_length=50,default='', blank=True)
    info = models.JSONField(default=dict, blank=True, null=True)
    place= models.JSONField(default=dict, blank=True, null=True)
    is_online = models.BooleanField(default=False)
    foto = models.ImageField(null=True, blank=True, upload_to="profil_fotoları/%Y/%m/" )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            img = Image.open(self.foto.path)
            if img.height> 600 or img.width>600:
                outputsize=(600,600)
                img.thumbnail(outputsize)
                img.save(self.foto.path)
    class Meta:
        verbose_name_plural="Profiller"



class InstagramAccounts(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='instagram')
    user_id = models.CharField(default="", max_length=100, blank=True, null=True)
    user_name = models.CharField(default="", max_length=100)
    password = models.CharField(default="", max_length=100)
    pwd_password = models.CharField(default="", max_length=100, blank=True, null=True)
    claim = models.CharField(default="", max_length=100, blank=True, null=True)
    auth_token = models.CharField(default="", max_length=250, blank=True, null=True)
    csrftoken = models.CharField(default="", max_length=100, blank=True, null=True)
    rur = models.CharField(default="", max_length=100, blank=True, null=True)
    ds_user_id = models.CharField(default="", max_length=50, blank=True, null=True)
    session_id = models.CharField(default="", max_length=50, blank=True, null=True)
    mid = models.CharField(default="", max_length=50, blank=True, null=True)
    shbid = models.CharField(default="", max_length=250, blank=True, null=True)
    shbts= models.CharField(default="", max_length=250, blank=True, null=True)
    region_hint= models.CharField(default="", max_length=250, blank=True, null=True)
    phone_number= models.CharField(default="", max_length=20, blank=True, null=True)
    country_code= models.IntegerField(default=0, blank=True, null=True)
    email= models.CharField(default="", max_length=50, blank=True, null=True)
    followers_count= models.IntegerField(default=0, blank=True, null=True)  
    ghost = models.BooleanField(default=False)
    gender = models.CharField(default="", max_length=50, blank=True, null=True)
    country = models.CharField(default="", max_length=50, blank=True, null=True)
    admin_area = models.CharField(default="", max_length=50, blank=True, null=True)
    locality = models.CharField(default="", max_length=50, blank=True, null=True)
    subLocality = models.CharField(default="", max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    bot_user = models.BooleanField(default=False)
    default_user = models.BooleanField(default=True)
    error=models.CharField(default="", max_length=50, blank=True, null=True)
    
    def __str__(self):
        return str(self.profil)
    
    class Meta:
        verbose_name_plural="instagram"


class Services(models.Model):
    service = models.AutoField(primary_key=True, verbose_name="Id")
    name = models.CharField(max_length=200, null=True, blank=True)
    comm = models.CharField(max_length=30, null=True,blank=True)
    type = models.CharField(max_length=200, default='Default')
    category = models.CharField(max_length=200, blank=True)
    rate = models.FloatField(blank=True, null=True) 
    min = models.IntegerField(default=1)
    max = models.IntegerField(default=99999)
    dripfeed = models.BooleanField(default=False)
    refill = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Servisler" 
class OrderList(models.Model):
    user=models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='orders')
    id=models.AutoField(primary_key=True, verbose_name="Id")
    key=models.CharField(max_length=50)	#Your API KEY
    action=models.CharField(max_length=50)	#add
    service =models.CharField(max_length=50, blank=True, null=True)
    link=models.CharField(max_length=200, blank=True)	#Link to page
    quantity=models.IntegerField(default=0, blank=True, null=True) #Needed quantity
    runs=models.CharField(max_length=200, null=True, blank=True) #(optional)	Runs to deliver
    interval=models.CharField(max_length=200, null=True, blank=True)  #(optional)	Interval in minutes
    comments=models.TextField(null=True, blank=True)
    charge=models.FloatField(default=10, blank=True)             # ": "0.27819",
    ## takip ve beğeni işlemlerinde kullanılacak
    start_count=models.IntegerField(default=0, null=True, blank=True)        #": "3572",
    insta_start_count=models.IntegerField(default=0, null=True, blank=True)        #": "3572",
    status=models.CharField(max_length=20, default="", null=True, blank=True)             #": "Partial",
    remains=models.IntegerField(default=0, null=True, blank=True)            #": "157",
    currency=models.CharField(max_length=3, default="TRY", null=True, blank=True )           #": "TRY"
    
    def difference(self):
        return self.quantity - self.remains
    class Meta:
        verbose_name_plural="order Listesi"
        ordering = ('-id', )

class InstagramVersions(models.Model):
    version=models.CharField(max_length=50, default="0.0.0")
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural="Instagram Version"
        ordering = ('-id', )
        
class CompletedOrders(models.Model):
    instagramaccount=models.ForeignKey(InstagramAccounts, on_delete=models.CASCADE, related_name='completed_orders')
    order=models.ForeignKey(OrderList, on_delete=models.CASCADE, related_name='completed_orders')
    create_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.instagramaccount)
    class Meta:
        verbose_name_plural="Tamamlanan Siparişler"
    
        

       
class ServicePrices(models.Model):
    class FollowCount(models.TextChoices):
        TAM='TAM'
        YUZ = '0-100'
        BESYUZ = '100-500'
        BIN = '500-1000'
        UCBIN= '1000-3000'
        BESBIN = '3000-5000'
        BESBINUSTU = '5000- ??'
        
    
    followerCount = models.CharField(
        max_length=10,
        choices=[(tag, tag.value) for tag in FollowCount],
        default=FollowCount.YUZ,
    )
    usersToFollow=models.FloatField(default=0.005)
    postLikes=models.FloatField(default=0.005)
    postComments=models.FloatField(default=0.005)
    postSaves=models.FloatField(default=0.005)
    commentLikes=models.FloatField(default=0.005)
    reelsLikes=models.FloatField(default=0.005)
    reelsComments=models.FloatField(default=0.005)
    igTVLikes=models.FloatField(default=0.005)
    igTVComments=models.FloatField(default=0.005)
    liveBroadCastLikes=models.FloatField(default=0.005)
    liveBroadCastComments=models.FloatField(default=0.005)
    liveWatches=models.FloatField(default=0.005)
    postShares=models.FloatField(default=0.005)
    suicideSpams=models.FloatField(default=0.005)
    storyShares=models.FloatField(default=0.005)
    videoShares=models.FloatField(default=0.005)
    singleUserDMs=models.FloatField(default=0.005)
    multiUserDMs=models.FloatField(default=0.005)
    spams=models.FloatField(default=0.005)
    time_stampt= models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural="Birim Fiy"
        
class EarnList(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='Kazanclar') 
    operation_id=models.CharField(max_length=50, null=True, blank=True)
    type= models.CharField(max_length=50, null=True, blank=True)
    pdflink=models.CharField(max_length=200, null=True, blank=True)
    amount=models.FloatField(default=0.005)
    ghost=models.BooleanField(default=False)
    operation_data=models.JSONField(default=dict, unique=True)
    time_stampt= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="Kazanc Tablosu"
        ordering = ('-id', )        

class BalanceRequest(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='BalanceRequests') 
    amount=models.FloatField(default=0.005)
    status=models.BooleanField(max_length=50, default=False)
    time_stampt= models.DateTimeField(auto_now_add=True)    
    class Meta:
        verbose_name_plural="Balance Requests"
        ordering = ('-id', )
        



