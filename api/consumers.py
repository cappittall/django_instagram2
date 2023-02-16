import json
#from Api.models import User
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from asgiref.sync import async_to_sync

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
        print(' 2 >>>>', close_code)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from Websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json  # ['message']
    
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
        #print(' 4 >>>>',event )
        message = event['message']

        #send message to Websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))




## CHAT VE GAME CUNSOMERS 
""" 
GAME CUNSOMER 
class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('CONNECTED-->', self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        #Receive message from WebSocket.
        #Get the event and send the appropriate event
 
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        if event == 'MOVE':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "MOVE"
            })

        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START"
            })

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END"
            })

    async def send_message(self, res):
        #Receive message from room group
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))
 """
""" 

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        #Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from Websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
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
        message = event['message']

        #send message to Websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
 """
# 
"""
     def connect(self):
        print(self.scope[">>>>>>>>>uery_string"])
        user_id = str(self.scope["query_string"]).split("=")[1][:-1]
        print(user_id)
        User.objects.filter(id=user_id).update(is_online=True)

        self.room_name = "users"
        self.channel_name = user_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name)
        self.accept()

        async_to_sync(self.channel_layer.send)(self.channel_name,
                                               { "type": "socket.message",
                                                 "text": "accapted"
                                               })

    def disconnect(self, close_code):
        User.objects.filter(
            id=self.channel_name).update(is_online=False)

        async_to_sync(self.channel_layer.group_discard)(
            "connectedusers", self.channel_name)
        pass

    def socket_message(self, event):
        print('>>>>>>> def socket_message socket_message...: ', event.get("text"))
        self.send(text_data=event.get("text"))


    def receive(self, text_data):
        print('>>>>>>> def receive ...: ',  json.loads(text_data))
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.send)(self.channel_name,
                                               {"type": "socket.message",
                                                "text": str(data)
                                               })
"""