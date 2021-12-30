from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class TestTagApiPublic(TestCase):
    """
    Test the tags endpoints which do not require auth
    """
    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that auth is required to get tags
        """
        resp = self.client.get(TAGS_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTagApiPrivate(TestCase):
    def setUp(self) -> None:
        """
        Setup authenticated user
        """
        self.user = get_user_model().objects.create_user(
            email='test@email.com', password='password', name='Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """
        Test get tags successfully, same order
        """
        Tag.objects.create(user=self.user, name="Italian")
        Tag.objects.create(user=self.user, name="Chinese")

        resp = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_tags_for_current_user(self):
        """
        Test that tags are returned for the authenticated user
        """
        other_user = get_user_model().objects.create_user(
            email='other@email.com', password='password', name='Other Name'
        )

        tag = Tag.objects.create(user=self.user, name="Italian")
        Tag.objects.create(user=other_user, name="Dessert")

        resp = self.client.get(TAGS_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], tag.name)
