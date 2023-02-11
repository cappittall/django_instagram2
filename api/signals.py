from django.contrib.auth.models import User
from api.models import Profil, InstagramAccounts
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail 
from rest_framework.authtoken.models import Token

#Signali iptal edip userserilizer da oluşturduk
""" @receiver(post_save, sender=User)
def create_profil(sender, instance, created, **kwargs ):
    
    print('Signal den: ',sender, instance, created )
    token, _ = Token.objects.get_or_create(user=instance)   
    
    if created:
        Profil.objects.create(user=instance , **{'token':token.key})  """
        
## Eğer hazır instagram hesabı açmak gerekirse anında hesap açmak için.
""" @receiver(post_save, sender=Profil)
def create_profil(sender, instance, created, **kwargs ):
    if created:
        InstagramAccounts.objects.create(profil=instance
                                         ## Ve mecburi doldurulması gereken alanları tanımla
                                         ) """
                                         
""" @receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    print('> look>>>>><<',email_plaintext_message);

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    ) """