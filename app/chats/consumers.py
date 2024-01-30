import json

from channels.generic.websocket import AsyncWebsocketConsumer

class EchoChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation = self.scope['conversation']
        if not self.conversation:
            await self.close(4001)
        self.room_name = f'{str(self.conversation.id)}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def chat_message(self, data):
        returned_data = {
            'type': 'new_message',
            'message': f'you have a new message',
            'data': data['data'],
            "code": data["code"]
        }
        await self.send(json.dumps(returned_data))

    async def update_read_status(self, data):
        returned_data = {
            'type': 'update_read_status',
            "message": "Read receipt updated",
            'data': data['data'],
            "code": data["code"]
        }
        await self.send(json.dumps(returned_data))

    async def disconnect(self, close_code):
        if self.room_name:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
