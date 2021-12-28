from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_success(self):
        """
        Test user creation with email successfully
        """
        email = "test@testmail.com"
        password = "test_password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_normalization(self):
        """
        Test that the user's email domain is normalized
        """
        email = "test@UPPERCASE.com"
        password = "test_password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())
