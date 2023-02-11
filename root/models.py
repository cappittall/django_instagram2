from django.db import models


class HomeData(models.Model):

    title = models.CharField(verbose_name="Başlık",max_length=150)
    explanation = models.CharField(verbose_name="Açıklama",max_length=1000)
    button1 = models.CharField(verbose_name="button 1 ismi",max_length=100)
    button2 = models.CharField(verbose_name="button 2 ismi",max_length=100)
    button1_link = models.CharField(verbose_name="button 1 link",max_length=500)
    button2_link = models.CharField(verbose_name="button 2 link",max_length=500)



    def __str__(self):
        return self.title

    class Meta:

        ordering = ['-id']
        verbose_name_plural = "Anasayfa İçeriği"




class LoginQueue(models.Model):

    date = models.DateTimeField(auto_now_add=True)
    process = models.IntegerField(default=0,verbose_name="İşlem Sayısı")
    end = models.BooleanField(default=False,verbose_name='Bitiş Durumu')
    class Meta:

        ordering = ['-date']
        verbose_name_plural = "Instagram Giriş Sırası"