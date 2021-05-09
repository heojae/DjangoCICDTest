from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from faker import Faker


class TestSetUp(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse('register')
        cls.login_url = reverse('login')
        cls.faker = Faker()
        return super().setUpTestData()

    def setUp(self) -> None:
        self.user_data = {
            'email': self.faker.email(),
            'username': self.faker.email().split('@')[0],
            'password': self.faker.email(),
        }
        self.client = APIClient()

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
