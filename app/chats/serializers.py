from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from rest_framework import serializers
from users.serializers import ListUserSerializer
from .models import Message, Conversation


def notify_message(message, consumer_type='chat_message'):
    channel_layer = get_channel_layer()
    notification_data = {
        'type': consumer_type,
        'data': MessageSerializer(message).data,
        "code": 200,
    }
    async_to_sync(channel_layer.group_send)(f'{str(message.conversation.id)}', notification_data)
    return True


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['conversation'] = str(instance.conversation.id)
        data['sender'] = ListUserSerializer(instance.sender).data
        return data


class CreateMessageSerializer(serializers.Serializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    message = serializers.CharField(required=True)

    def validate(self, attrs):
        if len({attrs['sender'], attrs['receiver']}) == 1:
            raise serializers.ValidationError(
                {'recipients': 'recipient user must be different from the sender'})

        return attrs

    def to_representation(self, instance):
        return MessageSerializer(instance).data

    def create(self, validated_data):
        conversation = Conversation.objects.get_or_create_personal_thread(
            user1=validated_data['sender'], user2=validated_data['receiver'])
        message = Message.objects.create(**validated_data, conversation=conversation)
        notify_message(message)
        return message


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

    def to_representation(self, instance: Conversation):
        data = super().to_representation(instance)
        data['users'] = ListUserSerializer(instance.users, many=True).data
        return data


class UpdateReadStatusSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    message = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=True)

    def validate(self, attrs):
        if attrs['user'].id != attrs['message'].receiver.id:
            raise serializers.ValidationError(
                {'user': 'User must the recipient of the message'})
        return attrs

    def create(self, validated_data):
        message = validated_data['message']
        message.is_read = True
        message.save(update_fields=['is_read'])
        channel_layer = get_channel_layer()
        notify_message(message, 'update_read_status')
        notification_data = {
            'type': 'update_read_status',
            'message': f'Read receipt updated',
            'data': MessageSerializer(message).data,
            "code": 200,
        }
        async_to_sync(channel_layer.group_send)(f'{str(message.conversation.id)}', notification_data)
        return message
