from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')


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

    def test_create_token_for_user(self):
        """
        Test that a token is created for user
        """
        data = {
            'email': 'test@email.com',
            'password': 'password',
        }
        create_user(**data)
        resp = self.client.post(TOKEN_URL, data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)

    def test_create_token_invalid_credential(self):
        """
        Test that token is not created for invalid credentials in request
        """
        create_user(email='test@email.com', password='password')
        data = {
            'email': 'test@email.com',
            'password': 'wrong_password'
        }
        resp = self.client.post(TOKEN_URL, data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', resp.data)

    def test_create_token_user_not_exist(self):
        """
        Test that token is not created if user does not exist
        """
        data = {
            'email': 'test@email.com',
            'password': 'wrong_password'
        }
        resp = self.client.post(TOKEN_URL, data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', resp.data)

    def test_create_token_missing_field(self):
        """
        Test that token is not created if request data misses fields
        """
        resp = self.client.post(TOKEN_URL, {})

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', resp.data)

    def test_retrieve_user_unauthorized(self):
        """
        Test that auth is required for users
        """
        resp = self.client.get(PROFILE_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserProfileApi(TestCase):
    """
    Test User Profile API, these requests require auth
    """
    def setUp(self) -> None:
        """
        Setup authenticated user
        """
        self.user = create_user(
            email='test@email.com', password='password', name='Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile(self):
        """
        Test that auth is required for getting user profile
        """
        resp = self.client.get(PROFILE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed_on_profile(self):
        """
        Test that POST is not allowed in profile url
        """
        resp = self.client.post(PROFILE_URL, {})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating user profile
        """
        data = {
            'name': 'New Name',
            'password': 'new_password'
        }
        resp = self.client.patch(PROFILE_URL, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data['name'])
        self.assertTrue(self.user.check_password(data['password']))
