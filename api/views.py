from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BaseRenderer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.throttling import SimpleRateThrottle

from api.permissions import CustomPermission
from api.serializers import ChangePasswordSerializer, InstagramSerializers, ProfilSerializers, \
    UserSerializers, ProfilFotoSerializer, ServiceSerializers, ServicePriceSerializers, \
    EarnListSerializer, OrdersSerializers, BalanceRequestSerializer
from api.models import InstagramAccounts, Profil, ServicePrices, EarnList, Services, OrderList, BalanceRequest
from api.static.choices import choices
import json
import pandas as pd
import os

HOME=os.getcwd()

### Get price list from excel file
df=pd.read_excel(f'{HOME}/api/static/excel/prices.xlsx', index_col=0)
service_prices=list( df.to_dict('dict').values() )


class UserViewSet(ModelViewSet):
    queryset=User.objects.all()
    serializer_class= UserSerializers
    permissions_classes = [IsAdminUser, CustomPermission]
    
    def post(self, request, *args, **kwargs):
        print('>>> view: ',request.data)
        
    
       
class ProfilViewSet(ModelViewSet):
    queryset=Profil.objects.all()
    serializer_class= ProfilSerializers
    permissions_classes = [IsAdminUser, CustomPermission]
    """ filter_backends = [SearchFilter]
    search_fields = ['id'] #instagramdan gelen userName
     """
    

class ProfilFotoUpdateView(generics.UpdateAPIView):
    serializer_class = ProfilFotoSerializer
    permissions_classes = [CustomPermission]
    
    def get_object(self):
        profil_nesnesi = self.request.user.profil  # type: ignore
        return profil_nesnesi

    
class InstagramViewSet(ModelViewSet):
    
    queryset=InstagramAccounts.objects.all()
    serializer_class= InstagramSerializers
    permissions_classes = [CustomPermission, IsAdminUser]
    
    
    def perform_create(self, serializer):
        print('>>> InstagramViewSet', self.request.user)
        profil = self.request.user.profil  # type: ignore
        serializer.save(profil=profil) 
        
class ServicesPriceViewSet(ModelViewSet):
    queryset=ServicePrices.objects.all()
    serializer_class= ServicePriceSerializers
    permissions_classes = [CustomPermission]
    

@csrf_exempt
@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer, BaseRenderer])
def getServices(request):
    key = request.POST.get('key', None) or request.GET.get('key', None)
    action = request.POST.get('action', None) or request.GET.get('action', None)
    service = request.POST.get('service', None) or request.GET.get('service', None)
    link = request.POST.get('link', None) or request.GET.get('link', None)
    quantity = request.POST.get('quantity', None) or request.GET.get('quantity', None)
   
    if service: service=int(service)
    
    comments = request.POST.get('comments', None) or request.GET.get('comments', None)
    if comments and not quantity: 
        comments = comments.replace('\\r','').replace('\\n', '\n')
        quantity=len(comments.split('\n'))

            
    orders = request.POST.get('orders', None) or request.GET.get('orders', None) or \
             request.POST.get('order', None) or request.GET.get('order', None)

        
    data={"key":key, "action":action, "service":service, "link":link, "quantity":quantity, "comments":comments }
    print('4>> \nData_________>', data)
    
    
    #data = JSONParser().parse(request)
    #action = data.get('action', None)
    #key = data.get('key', None)
    userKey = Token.objects.filter(key=key)
    
    if action=="add":            
        try:
            serviceObj = get_object_or_404(Services, service=service)
        except:
            return Response({'error': 'Service number not exists'}, status=400)

        order_serializer = OrdersSerializers(data=data)
        print('5 >>', order_serializer.is_valid())
        if order_serializer.is_valid():
            order_serializer.save(service=serviceObj)
            proceed_order(order_serializer.data) #, serviceObj.comm ) # data, comm=action namelike 'usersToFollow'
             
            return Response({'order': order_serializer.data.get('id', None)}, status=200)
        else:
            return Response({'error': 'Order data(s) missing or wrong '},status=401) 
        
    if action=="status":
        # example orders: '22' or '22,23'
        print("orders   : ", orders)
        try:
            orders =[ int(i) for i in orders.split(',')]  # type: ignore
        except: return Response({'error': 'Order(s) numbers not exists'}, status=401)
        stat=OrderList.objects.filter(id__in=orders).values('id', 'charge', 'start_count', 'status', 'remains', 'currency')
        
        result={}
        if len(stat)==1:
            print("stat  >>>>> ", stat[0] )
            result = stat[0]
            
        elif len(stat)>1:
            print( orders)
            for order in orders:
                rr = [item for item in stat if item['id']==order]
                result[str(order)] = rr[0] if len(rr)>0 else {"error": "Incorrect order ID"}
            for res in result:
                try:
                    result[res].pop('id')
                except:
                    print(result[res])  
        else:
            result={'error':'{} Incorrect order ID'.format(orders)}

        return Response(result , status=200 )
    
    if action=="balance":
        
        response= {
                    "balance": 100.00,
                    "currency": "TRY"  }
        return Response(response, status=200)
    
    # if none of above than;
    services = Services.objects.all() #values('category', 'dripfeed', 'max', 'min', 'name', 'orders', 'rate', 'refill', 'service', 'type')
    serializer = ServiceSerializers(services, many=True)  
    return Response(serializer.data)


"""
class ServicesViewSet(ModelViewSet):
    queryset=Services.objects.all()
    serializer_class= ServiceSerializers
    permissions_classes = [CustomPermission]
    
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        method = request.method.lower()
        key = request.POST.get('key', None)  or request.GET.get('key', None)
        action = request.POST.get('action', None) or request.GET.get('action', None)        
        userKey = Token.objects.get(user=request.user)
        print('Method : ',method, request, '\nKey : ',key,'->', userKey ,'\nAction : ', action)
        
        
        if action=="services":
            serializer = ServiceSerializers(Services.objects.all(), many=True)
            print('>>>> ', serializer.data)
            return request
        if action=="add":
            print('>>>>>>Add')
            return request
        if action=="status":
            print('>>>>>>Statüs')
            return request
        return request
"""

class OrdersViewSet(ModelViewSet):
    queryset=OrderList.objects.all()
    serializer_class= OrdersSerializers
    permissions_classes = [CustomPermission]
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class EarnListViewSet(ModelViewSet):

    queryset=EarnList.objects.all()
    serializer_class= EarnListSerializer
    permissions_classes = [CustomPermission]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user) 
        
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return EarnList.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if response.data:
            response.data['sum'] = self.get_queryset().aggregate(Sum('amount'))['amount__sum']
        return response
    
    
#one user can create one record in a month
class BalanceRequestThrottle(SimpleRateThrottle):
    scope = 'balance_request'
    def get_cache_key(self, request, view):
        return self.get_ident(request)
    
class BalanceRequestViewSet(ModelViewSet):
    queryset=BalanceRequest.objects.all()
    serializer_class= BalanceRequestSerializer
    permissions_classes = [CustomPermission]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]

    
    def perform_create(self, serializer):
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = now
        # Check if the user has already made a request in the current month
        user_requests = BalanceRequest.objects.filter(user=self.request.user, time_stampt__range=(start_of_month, end_of_month))
        if user_requests.exists():
            return Response({'error': 'You can only make one request per month'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = self.request.user
            serializer.save(user=user) 
        
        
    def get_queryset(self):
        """
        This view should return a list of all the balance requests
        for the currently authenticated user.
        """
        user = self.request.user
        return BalanceRequest.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if response.data:
            response.data['sum'] = self.get_queryset().aggregate(Sum('amount'))['amount__sum']
        return response
    
class CustomAuthToken(ObtainAuthToken):
    permissions_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']       # type: ignore
        token, created = Token.objects.get_or_create(user=user)
        
                
        return Response( UserSerializers(user).data )

def messages(request):
    context = {}
    context['room']=0
    context['choices']= choices
    # {c[0]:c[1] for c in Services.objects.values_list('comm', 'name')}
    return render(request, 'api/messages.html', context=context)

def index(request):
    context = {}
    template = 'api/index.html'
    return render(request, template, context)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permissions_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt 
def update_location(request, *args, **kwargs):
    if request.method=="POST":
        body = json.loads(request.body.decode('utf-8'))
        place = body['place']
        id= body['id']
        profil=Profil.objects.get(pk=id)
        profil.place=place
        profil.save();
        return JsonResponse({'status': 'success', 'message': 'Location updated successfully', 'data': json.dumps(place)}, status=200)


def proceed_order(data):
    
    
    channel_layer = get_channel_layer()
    
    """ 
    link = data['link']
    qty= data['quantity']
    comments = data['comments']
    message = { 'action' : data['action'],'sender' : 0, 'receiver': data['receivers'],
                'data': link + "| get_comment" if comments else '| No_comment'} """
    
    ## Send order to websocket 
    print('Data...> ', data)
    async_to_sync(channel_layer.group_send)(
        'inchat',
        {
            'type': 'chat_message',
            'message': data
        }
    )
    
    
def get_image_urls(request):
    # get list of files in the static/images directory    
    host='https://inmansdj.herokuapp.com/static/most_earners/'
    # get host url automatically
    host1= request.build_absolute_uri('/static/most_earners/')
    print('>>>> auto host : ', host1)
    image_urls = [host1 + image for image in os.listdir(f'{HOME}/api/static/most_earners') 
                  if (image.endswith('.jpg') or image.endswith('.jpeg') or image.endswith('.png'))]
    image_urls.sort()
    image_names=open(f'{HOME}/api/static/most_earners/names.txt', 'r').read().splitlines()
    data={"urls": image_urls, "names": image_names}
    
    return JsonResponse(data, safe=False)

def kazancTablosu(request):

    return JsonResponse({'results': service_prices}, safe=False)
     
def privacyPolicy(request):
    context = {}
    template = 'api/privacyPolicy1.html'
    return render(request, template, context)

    
def returnAdminToken(request):
    print('Admin token istendi ...')
    try:
        superuser = User.objects.get(is_superuser=True)
    except User.MultipleObjectsReturned:
        superuser = User.objects.filter(is_superuser=True).first()
        
    token= Token.objects.get(user=superuser)
    return JsonResponse({'token': token.key}, safe=False) 
