# Generated by Django 3.2 on 2023-02-09 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=500, verbose_name='Kategori Adı')),
            ],
            options={
                'verbose_name_plural': 'Instagram Kullanıcı Kategorileri',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OtherInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture_url', models.TextField(verbose_name='picture url')),
                ('country_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ülke Kodu')),
                ('gender', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cinsiyet')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Telefon No')),
                ('balance', models.IntegerField(default=0, verbose_name='balance')),
                ('default_user', models.BooleanField(default=True, verbose_name='Normal Kullanıcı')),
                ('bot_user', models.BooleanField(default=False, verbose_name='bot instagram user')),
                ('category', models.ManyToManyField(blank=True, to='user.UsersCategories')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'Kullanıcı Bilgileri',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='InstagramCookies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_password', models.CharField(max_length=250, verbose_name='password')),
                ('userid', models.CharField(max_length=1000, verbose_name='userid')),
                ('authorization', models.CharField(max_length=1000, verbose_name='authorization')),
                ('claim', models.CharField(max_length=1000, verbose_name='claim')),
                ('phoneid', models.CharField(max_length=1000, verbose_name='phoneid')),
                ('pigeonid', models.CharField(max_length=1000, verbose_name='pigeonid')),
                ('rur', models.CharField(max_length=1000, verbose_name='rur')),
                ('mid', models.CharField(max_length=1000, verbose_name='mid')),
                ('waterfallid', models.CharField(max_length=1000, verbose_name='waterfallid')),
                ('deviceid', models.CharField(max_length=1000, verbose_name='deviceid')),
                ('androidid', models.CharField(max_length=1000, verbose_name='androidid')),
                ('user_agent', models.CharField(max_length=1000, verbose_name='user_agent')),
                ('guid', models.CharField(max_length=1000, verbose_name='guid')),
                ('adid', models.CharField(max_length=1000, verbose_name='adid')),
                ('key', models.CharField(blank=True, max_length=1000, verbose_name='key')),
                ('checksum', models.CharField(blank=True, max_length=1000, verbose_name='checksum')),
                ('active', models.BooleanField(default=True, verbose_name='Hesap Aktifliği')),
                ('device_type', models.CharField(max_length=250, verbose_name='device_type')),
                ('brand', models.CharField(max_length=250, verbose_name='brand')),
                ('manufacturer', models.CharField(max_length=250, verbose_name='manufacturer')),
                ('os_type', models.CharField(max_length=250, verbose_name='os_type')),
                ('os_ver', models.CharField(max_length=250, verbose_name='os_ver')),
                ('error_count', models.IntegerField(default=0, verbose_name='ard arda hata sayısı')),
                ('challenge', models.BooleanField(default=False, verbose_name='challenge durumu')),
                ('feedback', models.BooleanField(default=False, verbose_name='feedback durumu')),
                ('checkpoint', models.BooleanField(default=False, verbose_name='checkpoint durumu')),
                ('login_required', models.BooleanField(default=False, verbose_name='login_required durumu')),
                ('new_account', models.BooleanField(default=True, verbose_name='new_account durumu')),
                ('old_account', models.BooleanField(default=False, verbose_name='old_account durumu')),
                ('ck_data', models.TextField(blank=True, verbose_name='ck,cs,sr,di,ds data')),
                ('register_key', models.TextField(blank=True, verbose_name='register key')),
                ('web_socket_controling', models.BooleanField(default=False, verbose_name='web socket control')),
                ('last_process_time', models.IntegerField(default=0, verbose_name='Son İşlem Zamanı')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'Kullanıcıların Instagmram Cookieleri',
                'ordering': ['-id'],
            },
        ),
    ]
