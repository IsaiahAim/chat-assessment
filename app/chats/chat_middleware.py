from urllib.parse import parse_qs

from channels.db import database_sync_to_async

from chats.models import Conversation


@database_sync_to_async
def get_conversation(scope):
    try:
        query_param = parse_qs(scope["query_string"].decode("utf8"))
        sender = query_param['sender'][0]
        receiver = query_param['receiver'][0]
        print(query_param)
        conversation = Conversation.objects.get_or_create_personal_thread(
            user1=sender, user2=receiver)
        print(conversation)
        return conversation
    except Exception as e:
        return None


class QueryAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope['conversation'] = await get_conversation(scope)
        print(scope)
        return await self.app(scope, receive, send)
