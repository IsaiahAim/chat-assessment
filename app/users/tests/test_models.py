from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser


class UserModelTest(TestCase):

    def setUp(self) -> None:
        self.customer_data = {
            "first_name": "test",
            "last_name": "user",
            "gender": "Male",
            "phone_no": "08174637364",
            "address":"test user address",
            "city": "test user city",
            "state": "test user state",
            "country": "test user country",
            "document_type": "Passport",
            "profile_picture": None,
            "document": SimpleUploadedFile('document.jpg', b'profile image content'),
            "email": "testuser@mail.com",
            "password": "password123",
            "is_active":True,
            "is_staff": False,
            "is_superuser":False
        }
        self.user = CustomUser.objects.create_user(**self.customer_data)

    def test_create_user(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(self.user.first_name, self.customer_data["first_name"])
        self.assertEqual(self.user.last_name, self.customer_data["last_name"])
        self.assertEqual(self.user.email, self.customer_data["email"])
        self.assertEqual(self.user.password, self.customer_data["password"])
        self.assertIsNone(self.user.profile_picture, self.customer_data["profile_picture"])
