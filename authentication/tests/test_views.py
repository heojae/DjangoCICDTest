from rest_framework import status
from rest_framework.response import Response

from authentication.models import User
from authentication.tests.test_setup import TestSetUp


class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        res: Response = self.client.post(
            self.register_url, self.user_data, format='json'
        )

        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res: Response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_login_after_verification(self):
        response: Response = self.client.post(self.register_url, self.user_data, format="json")
        email = response.data['email']
        User.objects.filter(email=email).update(is_verified=True)
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)
