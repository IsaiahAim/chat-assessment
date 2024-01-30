from django.contrib.auth import get_user_model

User = get_user_model()

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from chats.models import Conversation, Message
from client.models import Client


class ConversationViewSetTests(TestCase):
    def setUp(self):
        # Create a client for testing
        self.client_model = Client.objects.create(name='Testclient', key='Testkeysvalues')

        # Fetch the API key for the client
        self.api_key = self.client_model.key
        self.client = APIClient()

        # Create users for testing
        self.user1 = User.objects.create(username='User1')
        self.user2 = User.objects.create(username='User3')

        # Create a conversation for testing
        self.conversation = Conversation.objects.get_or_create_personal_thread(
            user1=self.user1, user2=self.user2
        )

        # Create messages for testing
        self.message1 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            message='Hello, user2!',
            receiver=self.user2
        )
        self.message2 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            message='Hi, user1!',
            receiver=self.user1
        )

    def test_get_messages_by_conversation(self):
        headers = {'X-API-Key': self.api_key}
        url = f'/api/v1/conversation/{self.conversation.pk}/messages-conversation/'
        response = self.client.get(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)  # Ensure data is a list

        # Assuming message is still present in each dictionary
        messages = [item.get('message') for item in response.data]

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], 'Hello, user2!')
        self.assertEqual(messages[1], 'Hi, user1!')

    def test_get_messages_by_recipient(self):
        headers = {'x-api-key': self.api_key}
        url = f'/api/v1/conversation/{self.user1.id}/{self.user2.id}/messages/'
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)  # Ensure data is a list

        # Assuming message is still present in each dictionary
        messages = [item.get('message') for item in response.data]

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], 'Hello, user2!')
        self.assertEqual(messages[1], 'Hi, user1!')

    def test_create_message(self):
        headers = {'X-API-Key': self.api_key}
        url = '/api/v1/conversation/create-message/'
        data = {
            'sender': self.user1.id,
            'receiver': self.user2.id,
            'message': 'New message from user1 to user2'
        }
        response = self.client.post(url, data, format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(Message.objects.count(), 3)

    def test_update_read_status(self):
        headers = {'X-API-Key': self.api_key}
        url = '/api/v1/conversation/update-read-status/'
        data = {
            'user': self.user1.id,
            'message': self.message2.id,
        }
        response = self.client.post(url, data, format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.message2.refresh_from_db()
        self.assertTrue(self.message2.is_read)


