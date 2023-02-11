from os import name
from user.models import OtherInfo
from django.core.management.base import BaseCommand
from services.models import ServiceCategory,CategoryType,Genders,Services

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        service_types = ['Default','Custom Comments']
        service_categories_default = ['Takipçi','Beğeni','Canlı Yayın Beğeni','Canlı Yayın İzleme 4 Saat',
                    'Canlı Yayın İzleme 30 Dakika','Oto Takipçi','Oto Beğeni 7','Oto Beğeni 14','Oto Beğeni 30','Fotoğraf Kaydetme','Kullanıcı Takiçilerini Çekme',
                    'DM Toplu Link Kullanıcı Takipçi Taramalı Mesaj','DM Resim Toplu Kullanıcı Takipçi Taramalı Mesaj','DM Video Toplu Kullanıcı Takipçi Taramalı Mesaj',
                    'DM IGTV Toplu Kullanıcı Takipçi Taramalı Mesaj','DM Reel Video Toplu Kullanıcı Takipçi Taramalı Mesaj','PostImage+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
                    'PostVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM','Igtv+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
                    'ReelVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM','Profil Sayfası + Mesaj Kullanıcı Takipçi Taramalı DM',
                    'Profil Sayfası + Mesaj + Link Kullanıcı Takipçi Taramalı DM','Profil Ziyaret','Video İzleme',


                    ]
        service_categories_custom_comments = ['Yorum','Canlı Yayın Yorum','DM Mesaj','DM Toplu Link Mesaj','DM Toplu Resimli Mesaj','DM Toplu Videolu Mesaj',
                                            'DM Toplu IGTV Mesaj','DM Toplu Reel Mesaj','Igtv+Mesaj Link+Mesaj Toplu DM','ReelVideo+Mesaj Link+Mesaj Toplu DM',
                                            'PostVideo+Mesaj Link+Mesaj Toplu DM','PostImage+Mesaj Link+Mesaj Toplu DM','Profil Sayfası + Mesaj Toplu DM',
                                            'Profil Sayfası + Mesaj + Link Toplu DM']
        genders = ['1','2']

        print('Genders')
        for x in genders:
            if not Genders.objects.filter(name=x):
        
                Genders.objects.create(name=x)
                print('created[%s]'%(x))
        
        print('CategoryTypes')
        for y in service_types:
            if not CategoryType.objects.filter(type_name=y):
            
                CategoryType.objects.create(type_name=y)
                print('created[%s]'%(y))

        print('CategoryTypes Default')
        for z in service_categories_default:
            if not ServiceCategory.objects.filter(category_name=z):

                type_ = CategoryType.objects.filter(type_name='Default').last()
                ServiceCategory.objects.create(category_name=z,category_type=type_)
                print('created[%s]'%(z))

        print('CategoryTypes Custom Comments')
        for w in service_categories_custom_comments:
            if not ServiceCategory.objects.filter(category_name=w):
                type_ = CategoryType.objects.filter(type_name='Custom Comments').last()
                ServiceCategory.objects.create(category_name=w,category_type=type_)
                print('created[%s]'%(w))
        if Services.objects.all().count() == 0:
            print('girdi 1')

            servicesDict = [
                {
                    'name':'Beğeni',
                    'category':ServiceCategory.objects.filter(category_name='Beğeni').last(),
                    'max':10000,
                    'min':1,
                },
                {
                    'name':'Takipçi',
                    'category':ServiceCategory.objects.filter(category_name='Takipçi').last(),
                    'max':10000,
                    'min':1,
                },
                {
                    'name':'Yorum',
                    'category':ServiceCategory.objects.filter(category_name='Yorum').last(),
                    'max':10000,
                    'min':1,
                },
                {
                    'name':'Canlı Yayın Beğeni',
                    'category':ServiceCategory.objects.filter(category_name='Canlı Yayın Beğeni').last(),
                    'max':10000,
                    'min':1,
                },
                {
                    'name':'Canlı Yayın İzleme 4 Saat',
                    'category':ServiceCategory.objects.filter(category_name='Canlı Yayın İzleme 4 Saat').last(),
                    'max':10000,
                    'min':1,
                },
                {
                    'name':'Canlı Yayın İzleme 30 Dakika',
                    'category':ServiceCategory.objects.filter(category_name='Canlı Yayın İzleme 30 Dakika').last(),
                    'max':10000,
                    'min':1,
                },
                  {
                    'name':'Oto Takipçi',
                    'category':ServiceCategory.objects.filter(category_name='Oto Takipçi').last(),
                    'max':9999999,
                    'min':1,
                },
                            {
                    'name':'Oto Beğeni 7',
                    'category':ServiceCategory.objects.filter(category_name='Oto Beğeni 7').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'Oto Beğeni 14',
                    'category':ServiceCategory.objects.filter(category_name='Oto Beğeni 14').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'Oto Beğeni 30',
                    'category':ServiceCategory.objects.filter(category_name='Oto Beğeni 30').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'Fotoğraf Kaydetme',
                    'category':ServiceCategory.objects.filter(category_name='Fotoğraf Kaydetme').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'Kullanıcı Takiçilerini Çekme',
                    'category':ServiceCategory.objects.filter(category_name='Kullanıcı Takiçilerini Çekme').last(),
                    'max':5000000,
                    'min':1,
                },
                            {
                    'name':'Canlı Yayın Yorum',
                    'category':ServiceCategory.objects.filter(category_name='Canlı Yayın Yorum').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'DM Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Mesaj').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'DM Toplu Link Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Toplu Link Mesaj').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'DM Toplu Resimli Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Toplu Resimli Mesaj').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'DM Toplu Videolu Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Toplu Videolu Mesaj').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'DM Toplu IGTV Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Toplu IGTV Mesaj').last(),
                    'max':10000,
                    'min':1,
                },
                            {
                    'name':'DM Toplu Reel Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Toplu Reel Mesaj').last(),
                    'max':10000,
                    'min':1,
                },
                {
                    'name':'Igtv+Mesaj Link+Mesaj Toplu DM',
                    'category':ServiceCategory.objects.filter(category_name='Igtv+Mesaj Link+Mesaj Toplu DM').last(),
                    'max':999999,
                    'min':1,
                },
                {
                    'name':'ReelVideo+Mesaj Link+Mesaj Toplu DM',
                    'category':ServiceCategory.objects.filter(category_name='ReelVideo+Mesaj Link+Mesaj Toplu DM').last(),
                    'max':999999,
                    'min':1,
                },
                {
                    'name':'PostVideo+Mesaj Link+Mesaj Toplu DM',
                    'category':ServiceCategory.objects.filter(category_name='PostVideo+Mesaj Link+Mesaj Toplu DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'PostImage+Mesaj Link+Mesaj Toplu DM',
                    'category':ServiceCategory.objects.filter(category_name='PostImage+Mesaj Link+Mesaj Toplu DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'Profil Sayfası + Mesaj Toplu DM',
                    'category':ServiceCategory.objects.filter(category_name='Profil Sayfası + Mesaj Toplu DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'Profil Sayfası + Mesaj + Link Toplu DM',
                    'category':ServiceCategory.objects.filter(category_name='Profil Sayfası + Mesaj + Link Toplu DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'DM Toplu Link Kullanıcı Takipçi Taramalı Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Toplu Link Kullanıcı Takipçi Taramalı Mesaj').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'DM Resim Toplu Kullanıcı Takipçi Taramalı Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Resim Toplu Kullanıcı Takipçi Taramalı Mesaj').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'DM Video Toplu Kullanıcı Takipçi Taramalı Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Video Toplu Kullanıcı Takipçi Taramalı Mesaj').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'DM IGTV Toplu Kullanıcı Takipçi Taramalı Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM IGTV Toplu Kullanıcı Takipçi Taramalı Mesaj').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'DM Reel Video Toplu Kullanıcı Takipçi Taramalı Mesaj',
                    'category':ServiceCategory.objects.filter(category_name='DM Reel Video Toplu Kullanıcı Takipçi Taramalı Mesaj').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'PostImage+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
                    'category':ServiceCategory.objects.filter(category_name='PostImage+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'PostVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
                    'category':ServiceCategory.objects.filter(category_name='PostVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'Igtv+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
                    'category':ServiceCategory.objects.filter(category_name='Igtv+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'ReelVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM',
                    'category':ServiceCategory.objects.filter(category_name='ReelVideo+Mesaj Link+Mesaj Toplu Kullanıcı Takipçi Taramalı DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'Profil Sayfası + Mesaj Kullanıcı Takipçi Taramalı DM',
                    'category':ServiceCategory.objects.filter(category_name='Profil Sayfası + Mesaj Kullanıcı Takipçi Taramalı DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'Profil Sayfası + Mesaj + Link Kullanıcı Takipçi Taramalı DM',
                    'category':ServiceCategory.objects.filter(category_name='Profil Sayfası + Mesaj + Link Kullanıcı Takipçi Taramalı DM').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'Profil Ziyaret',
                    'category':ServiceCategory.objects.filter(category_name='Profil Ziyaret').last(),
                    'max':999999,
                    'min':1,
                },
                                {
                    'name':'Video İzleme',
                    'category':ServiceCategory.objects.filter(category_name='Video İzleme').last(),
                    'max':999999,
                    'min':1,
                },
            ]
            
            packpages = None
            for sv in servicesDict:
                Services.objects.create(name=sv['name'],packpages=packpages,category=sv['category'],min=sv['min'],max=sv['max'])
                print('{} servisi oluşturuldu.'.format(sv['name']))


