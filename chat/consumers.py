import json
from contextlib import suppress

from channels.generic.websocket import AsyncWebsocketConsumer

USERS = {}


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        with suppress(KeyError):
            del USERS[f"{self.scope['client'][0]}::{self.scope['client'][1]}"]

    # Receive message from WebSocket
    async def receive(self, text_data):
        with suppress(json.decoder.JSONDecodeError, KeyError):
            text_data_json = json.loads(text_data)
            print(
                self.scope['client'],
                USERS.get(f"{self.scope['client'][0]}::{self.scope['client'][1]}"),
                text_data_json
            )

            if command := text_data_json.get('command'):
                if command == 'auth':
                    user = text_data_json['username']
                    if user not in USERS.values():
                        USERS[f"{self.scope['client'][0]}::{self.scope['client'][1]}"] = user
                elif command == 'sendmessage':
                    user = USERS.get(f"{self.scope['client'][0]}::{self.scope['client'][1]}")
                    if user:
                        message = text_data_json['message']

                        # Send message to room group
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {'type': 'chat_message', 'username': user, 'message': message}
                        )

    # Receive message from room group
    async def chat_message(self, event):
        user = event['username']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'username': user, 'message': message}))