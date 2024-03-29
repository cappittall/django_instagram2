# Generated by Django 3.2 on 2023-09-06 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0004_auto_20230306_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramVersions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='0.0.0', max_length=50)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Instagram Version',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('key', models.CharField(max_length=50)),
                ('action', models.CharField(max_length=50)),
                ('service', models.CharField(blank=True, max_length=50, null=True)),
                ('link', models.CharField(blank=True, max_length=200)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('runs', models.CharField(blank=True, max_length=200, null=True)),
                ('interval', models.CharField(blank=True, max_length=200, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('charge', models.FloatField(blank=True, default=10)),
                ('start_count', models.IntegerField(blank=True, default=0, null=True)),
                ('insta_start_count', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('remains', models.IntegerField(blank=True, default=0, null=True)),
                ('currency', models.CharField(blank=True, default='TRY', max_length=3, null=True)),
                ('successful_value', models.IntegerField(default=0, verbose_name='Başarılı İşlem Miktarı')),
                ('process', models.IntegerField(default=0, verbose_name='İşlem Sayısı')),
                ('cancelled', models.BooleanField(default=False, verbose_name='İptal Durumu')),
                ('target', models.CharField(blank=True, max_length=500, null=True, verbose_name='Hedef')),
                ('user_order', models.BooleanField(default=False, verbose_name='Kullanıcı Siparişi')),
                ('auto_process', models.BooleanField(default=False, verbose_name='Oto İşlem')),
            ],
            options={
                'verbose_name_plural': 'order Listesi',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='RefEarnList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normal_user', models.CharField(max_length=260, verbose_name='Kullanıcı')),
                ('ref_code', models.CharField(max_length=260, verbose_name='Referans Kullanıcı')),
                ('amount', models.FloatField(default=0.005)),
                ('time_stampt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Referans Kazanc Tablosu',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ServicePrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followerCount', models.CharField(choices=[('TAM', 'TAM'), ('0-100', '0-100'), ('100-500', '100-500'), ('500-1000', '500-1000'), ('1000-3000', '1000-3000'), ('3000-5000', '3000-5000'), ('5000- ??', '5000- ??')], default='0-100', max_length=10)),
                ('usersToFollow', models.FloatField(default=0.005)),
                ('postLikes', models.FloatField(default=0.005)),
                ('postComments', models.FloatField(default=0.005)),
                ('postSaves', models.FloatField(default=0.005)),
                ('commentLikes', models.FloatField(default=0.005)),
                ('reelsLikes', models.FloatField(default=0.005)),
                ('reelsComments', models.FloatField(default=0.005)),
                ('igTVLikes', models.FloatField(default=0.005)),
                ('igTVComments', models.FloatField(default=0.005)),
                ('liveBroadCastLikes', models.FloatField(default=0.005)),
                ('liveBroadCastComments', models.FloatField(default=0.005)),
                ('liveWatches', models.FloatField(default=0.005)),
                ('postShares', models.FloatField(default=0.005)),
                ('suicideSpams', models.FloatField(default=0.005)),
                ('storyShares', models.FloatField(default=0.005)),
                ('videoShares', models.FloatField(default=0.005)),
                ('singleUserDMs', models.FloatField(default=0.005)),
                ('multiUserDMs', models.FloatField(default=0.005)),
                ('spams', models.FloatField(default=0.005)),
                ('time_stampt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Birim Fiy',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('service', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('comm', models.CharField(blank=True, max_length=30, null=True)),
                ('type', models.CharField(default='Default', max_length=200)),
                ('category', models.CharField(blank=True, max_length=200, null=True, verbose_name='APP Kategori')),
                ('rate', models.FloatField(blank=True, null=True)),
                ('min', models.IntegerField(default=1)),
                ('max', models.IntegerField(default=99999)),
                ('dripfeed', models.BooleanField(default=False)),
                ('refill', models.BooleanField(default=True)),
                ('packpages', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='packpage', to='services.userpackpages', verbose_name='Kullanıcı Paketi')),
                ('panel_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='panel_category', to='services.servicecategory', verbose_name='Panel Kategori')),
            ],
            options={
                'verbose_name_plural': 'Servisler',
            },
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, default='', max_length=20)),
                ('birth_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('tc', models.CharField(blank=True, default='', max_length=15)),
                ('iban', models.CharField(blank=True, default='TR', max_length=50)),
                ('bank', models.CharField(blank=True, default='Banka', max_length=50)),
                ('coin', models.CharField(blank=True, default='', max_length=50)),
                ('coin_adresi', models.CharField(blank=True, default='', max_length=50)),
                ('info', models.JSONField(blank=True, default=dict, null=True)),
                ('place', models.JSONField(blank=True, default=dict, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='profil_fotoları/%Y/%m/')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('ref', models.CharField(blank=True, default=None, max_length=260, null=True, verbose_name='Referans')),
                ('ref_code', models.CharField(max_length=260, verbose_name='Referans Kodu')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profiller',
            },
        ),
        migrations.CreateModel(
            name='OrderUserLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, verbose_name='user_id')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orderlist', verbose_name='order')),
            ],
            options={
                'verbose_name_plural': 'Sipariş Bot User Kayıtları',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='orderlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.profil'),
        ),
        migrations.CreateModel(
            name='InstagramAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('user_name', models.CharField(default='', max_length=100)),
                ('password', models.CharField(default='', max_length=100)),
                ('pwd_password', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('claim', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('auth_token', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('csrftoken', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('rur', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('ds_user_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('session_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('mid', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('user_agent', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('blokversion_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('pigeon_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('android_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('device_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('phone_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('waterfall_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('guid', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('adid', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('shbid', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('shbts', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('region_hint', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('phone_number', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('country_code', models.IntegerField(blank=True, default=0, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('followers_count', models.IntegerField(blank=True, default=0, null=True)),
                ('ghost', models.BooleanField(default=False)),
                ('gender', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('admin_area', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('locality', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('subLocality', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('bot_user', models.BooleanField(default=False)),
                ('default_user', models.BooleanField(default=True)),
                ('error', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instagram', to='api.profil')),
            ],
            options={
                'verbose_name_plural': 'instagram',
            },
        ),
        migrations.CreateModel(
            name='EarnList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_id', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('pdflink', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.FloatField(default=0.005)),
                ('ghost', models.BooleanField(default=False)),
                ('ref_earn', models.BooleanField(default=False)),
                ('operation_data', models.JSONField(default=dict, unique=True)),
                ('time_stampt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Kazanclar', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Kazanc Tablosu',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='CompletedOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('instagramaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completed_orders', to='api.instagramaccounts')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completed_orders', to='api.orderlist')),
            ],
            options={
                'verbose_name_plural': 'Tamamlanan Siparişler',
            },
        ),
        migrations.CreateModel(
            name='BalanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.005)),
                ('status', models.BooleanField(default=False, max_length=50)),
                ('time_stampt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BalanceRequests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Balance Requests',
                'ordering': ('-id',),
            },
        ),
    ]
