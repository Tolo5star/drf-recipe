from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**kwargs):
    """
    Utility to create user
    """
    return get_user_model().objects.create_user(**kwargs)


class TestUsersApi(TestCase):
    """
    Test user API
    """
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test successful user creation with valid parameters
        """
        data = {
            'email': 'test@email.com',
            'password': 'password',
            'name': 'Test Name'
        }
        resp = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**resp.data)
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', resp.data)

    def test_user_exists(self):
        """
        Test that a user that already exists
        is not created again and the request fails
        """
        data = {
            'email': 'test@email.com',
            'password': 'password',
        }
        create_user(**data)
        data['name'] = 'Test Name'
        resp = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_min_length(self):
        """
        Test that user cannot have a password with less than the min length
        """
        data = {
            'email': 'test@email.com',
            'password': 'pass',
            'name': 'Test Name'
        }
        resp = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model()\
            .objects.filter(email=data['email']).exists()
        self.assertFalse(user_exists)
