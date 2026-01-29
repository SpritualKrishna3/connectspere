from channels.generic.websocket import AsyncWebsocketConsumer
import json

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.channel_layer.group_add("online_users", self.channel_name)
            await self.accept()
            await self.channel_layer.group_send(
                "online_users",
                {"type": "user.online", "user_id": self.user.id}
            )

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_send(
                "online_users",
                {"type": "user.offline", "user_id": self.user.id}
            )