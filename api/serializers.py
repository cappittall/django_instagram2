from api.models import InstagramAccounts, Profil, ServicePrices, Services, EarnList, OrderList, BalanceRequest, InstagramVersions,RefEarnList
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.authtoken.models import Token
import uuid
from dj_rest_auth.serializers  import PasswordResetSerializer
from core.settings import ref_earn

class InstagramSerializers(serializers.ModelSerializer):
    class Meta:
        model = InstagramAccounts
        fields = '__all__'
                  
    def create(self, validated_data):
        insta = InstagramAccounts.objects.create(**validated_data)
        return insta
    
class ServicePriceSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicePrices
        fields = '__all__'
        
    def create(self, validated_data):
        print(validated_data )
        service_prices = ServicePrices.objects.create(**validated_data)
        return service_prices
    
    def update(self, instance, validated_data):
        print(instance, '\n', validated_data)
        pass

class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        exclude = ('comm',)
        
    def create(self, validated_data):
        print(validated_data )
        services = Services.objects.create(**validated_data)
        return services
    
class OrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderList
        fields = '__all__'   
          
    def create(self, validated_data):
        return OrderList.objects.create(**validated_data)

class InstagramVersionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = InstagramVersions
        fields = '__all__'   
          
    def create(self, validated_data):
        return InstagramVersions.objects.create(**validated_data)
    
class EarnListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = EarnList
        fields = '__all__'
        
    def create(self, validated_data):                      
        earn = EarnList.objects.create(**validated_data)
        if earn.user.profil.ref:
            get_ref = Profil.objects.get(ref_code=earn.user.profil.ref)
            ref_pay = earn.amount / 100 * ref_earn
            earn.amount -= ref_pay

            get_ref_earn = RefEarnList.objects.fitler(user=earn.user.username,ref_code=earn.user.profil.ref).last()
            if get_ref_earn:
                get_ref_earn.amount += ref_pay
                get_ref_earn.save()
            else:
                RefEarnList.objects.create(user=earn.user.username,ref_code=earn.user.profil.ref,amount=ref_pay)

            earn.save()
            EarnList.objects.create(user=get_ref,amount=ref_pay,ref_earn=True)
        return earn


class RefEarnListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = RefEarnList
        fields = '__all__'
        
      
class BalanceRequestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = BalanceRequest
        fields = '__all__'
        
    def create(self, validated_data):
        earning = BalanceRequest.objects.create(**validated_data)
        return earning 
    
class ProfilSerializers(serializers.ModelSerializer):
    instagram = InstagramSerializers(many=True, read_only=True)    
    foto = serializers.ImageField(read_only=True)
    
    class Meta:
        model = Profil
        fields = '__all__'
class ProfilFotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profil
        fields=['foto']
        
class UserSerializers(serializers.ModelSerializer):
    profil = ProfilSerializers(read_only=True)      
    class Meta:
        model= User
        fields=['id', 'username', 'password', 'email', 'first_name', 'last_name', 'profil']
        
    def create(self, validated_data): 
        
        profile_data = self.context.get('request', None).data.get('profil', {})
        #profile_data = validated_data.pop('profil', None) 
        
        print( self.context.get('request', None).data) 
        print('Valişdated data: ',validated_data ,'\nProfil_Data :', profile_data )
        
        user = User.objects.create_user(**validated_data)
        token,_ = Token.objects.get_or_create(user=user)
        
        
        if profile_data:
            while True:
                create_ref_code = "{}#{}".format(user.username,str(uuid.uuid4().hex)[0:4].lower())
                if Profil.objects.filter(ref_code=create_ref_code).count() == 0:
                    break
            
            profile_data.update({'token': token.key,'ref_code':create_ref_code})
       
        Profil.objects.create(user=user, **profile_data)
        return user 
    
    def update(self, instance, validated_data):  

        profile_data = self.context.get('request').data.get('profil', {})
        
        print('Profil Data :', profile_data, '\nValidated Data',validated_data) 
        profile = instance.profil

        # Update User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)    
        instance.save() 
               
        # update Profil
        profile.token = profile_data.get('token', profile.token )
        profile.phone = profile_data.get('phone', profile.phone )
        profile.birth_date = profile_data.get('birth_date', profile.birth_date )
        profile.tc = profile_data.get('tc', profile.tc )
        profile.iban = profile_data.get('iban', profile.iban)
        profile.bank = profile_data.get('bank', profile.bank)
        profile.coin = profile_data.get('coin', profile.coin )
        profile.coin_adresi = profile_data.get('coin_adresi', profile.coin_adresi )
        profile.info  = profile_data.get('info', profile.info)
        profile.place = profile_data.get('place', profile.place)
        profile.is_online = profile_data.get('is_online', profile.is_online )
        profile.save()
        print('Updated instance : ', instance)
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    def validate_new_password(self, value):
        validate_password(value)
        return value
