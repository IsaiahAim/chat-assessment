import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from chats.models import Conversation, Message
from chats.serializers import MessageSerializer, ConversationSerializer, CreateMessageSerializer, \
    UpdateReadStatusSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter


header = extend_schema(
    parameters=[OpenApiParameter(
        "x-api-key", OpenApiTypes.STR,
        OpenApiParameter.HEADER, required=True)])


@extend_schema_view(
    list=header,
    retrieve=header,
    get_messages_by_conversation=header,
    get_messages_by_recipient=header,
    create_message=header,
    update_read_status=header,

)
class ConversationViewset(viewsets.GenericViewSet,
                          viewsets.generics.RetrieveAPIView,
                          viewsets.generics.ListAPIView,
                          viewsets.generics.DestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    http_method_names = ["get", "delete", 'post']
    permission_classes = [AllowAny]

    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(users=self.request.user).prefetch_related(
            'users').order_by('-latest_message_time')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="page",
                description="Page number within the paginated result",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="page_size",
                description="Num of results to return per page",
                required=False,
                type=int,
            )
        ],
        methods=["GET"],
    )
    @action(methods=['GET'], detail=True, serializer_class=MessageSerializer,
            url_path='messages-conversation')
    def get_messages_by_conversation(self, request, pk=None):
        """ Get all messages """
        qs = Message.objects.filter(conversation=pk).select_related(
            'conversation', 'sender', )
        return self.paginate_results(qs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="page",
                description="Page number within the paginated result",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="page_size",
                description="Num of results to return per page",
                required=False,
                type=int,
            )
        ],
        methods=["GET"],
    )
    @action(methods=['GET'], detail=False, serializer_class=MessageSerializer,
            url_path=r'(?P<authenticated_user_id>[\w-]+)/(?P<recipient_id>[\w-]+)/messages')
    def get_messages_by_recipient(self, request, recipient_id, authenticated_user_id, pk=None):
        """ Get all messages """
        conversation = Conversation.objects.get_or_create_personal_thread(
            user1=authenticated_user_id, user2=recipient_id)

        if not conversation:
            return self.paginate_results([])
        qs = conversation.message.all().select_related(
            'conversation', 'sender')
        return self.paginate_results(qs)

    @action(methods=['POST'], detail=False, serializer_class=CreateMessageSerializer,
            url_path=r'create-message')
    def create_message(self, request, pk=None):
        """ Create  all messages  """
        serializer = CreateMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Message  created successfully",
                         'data': serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, serializer_class=UpdateReadStatusSerializer,
            url_path=r'update-read-status')
    def update_read_status(self, request, pk=None):
        """ Update Message read status """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Message Read status Updated Succesfully"},
                        status=status.HTTP_200_OK)
