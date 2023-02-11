from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import Orders, Services
from django.contrib.auth.models import User
from user.models import OtherInfo,InstagramCookies


class ServicesSerializer(serializers.ModelSerializer):
  
    category = serializers.CharField(source='category.category_name')
    type = serializers.CharField(source='category.category_type.type_name')

    class Meta:
        
            model = Services
            fields = ('service','name','type','category','rate','min','max','dripfeed','refill')




class OtherInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OtherInfo

        fields = '__all__'

class InstagramCookiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstagramCookies
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    otherinfo = OtherInfoSerializer()
    instagramcookies = InstagramCookiesSerializer()

    class Meta:
        model = User

        fields = '__all__'
