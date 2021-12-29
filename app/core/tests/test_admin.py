from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self) -> None:
        """
        Creates a test client, login as admin and
        creates a normal user
        """
        self.client = Client()
        password = "test_password"
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@testmail.com",
            password=password
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="normal_user@testmail.com",
            password=password,
            name="User Name"
        )

    def test_users_listed(self):
        """
        Test that users are listed on user page
        """
        url = reverse('admin:core_user_changelist')
        resp = self.client.get(url)

        self.assertContains(resp, self.user.name)
        self.assertContains(resp, self.user.email)

    def test_user_change_page(self):
        """
        Test that the user edit page works with our custom user changes
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_create_user_page(self):
        """
        Test that the create user page works with our custom user changes
        """
        url = reverse('admin:core_user_add')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
