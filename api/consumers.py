import json
import re
import time
#from Api.models import User
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from api.static.choices import choices
from django.db.models import F
from api.models import OrderList
from threading import Thread


from asgiref.sync import async_to_sync

def my_background_task(data):
    data = json.loads(re.sub(r'(?!:)(\w+)', r'"\1"', data))
    print('2.1. data', data, type(data))
    ## 201 = alacak işlenmiş, 202 = free işlem   
    if int(data['alacak'])==201 or int(data['alacak'])==202:
        OrderList.objects.filter( id=int(data['order_id']) ).update(remains=F('remains')-1)
        order = OrderList.objects.get(id=int(data['order_id']))
        status= "Completed" if order.remains <=0 else "Partial"
        order.status = status
        order.save()
        print('işlem başarılı')
    return True

class ApiConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'inchat' # 'chat_%s' % self.room_name
        print( '1>>>', self.room_group_name, self.channel_name )

        #Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(' 2.Channel disconnected >>>>', close_code)
        time.sleep(5)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from Websocket
    async def receive_json(self, message):
        print(' 3.1 >>>>', message, type(message))
        if message['action']=='mobileAction':
            data = message['message']
            Thread(target=my_background_task, args=(data,)).start()
                  
        #send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # Receive message from room group
    async def chat_message(self, event):
        
        print(' 4 >>>>', event, type(event))
        
        if 'message' in event:
            message = event['message']
                
            #send message to Websocket
            await self.send(text_data=json.dumps({
                'message': message
            }))
