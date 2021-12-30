from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class TestIngredientApiPublic(TestCase):
    """
    Test the ingredients endpoints which do not require auth
    """
    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that auth is required to get ingredients
        """
        resp = self.client.get(INGREDIENT_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class TestIngredientApiPrivate(TestCase):
    def setUp(self) -> None:
        """
        Setup authenticated user
        """
        self.user = get_user_model().objects.create_user(
            email='test@email.com', password='password', name='Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients(self):
        """
        Test get ingredients successfully, same order
        """
        Ingredient.objects.create(user=self.user, name="Potato")
        Ingredient.objects.create(user=self.user, name="Tomato")

        resp = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_ingredients_for_current_user(self):
        """
        Test that ingredients are returned for the authenticated user
        """
        other_user = get_user_model().objects.create_user(
            email='other@email.com', password='password', name='Other Name'
        )

        ingredient = Ingredient.objects.create(user=self.user, name="Potato")
        Ingredient.objects.create(user=other_user, name="Tomato")

        resp = self.client.get(INGREDIENT_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """
        Test ingredient creation
        """
        data = {
            'name': 'test_ingredient'
        }

        self.client.post(INGREDIENT_URL, data)

        ingredient_exists = Ingredient.objects.\
            filter(user=self.user, name=data['name'])\
            .exists()
        self.assertTrue(ingredient_exists)

    def test_create_ingredient_invalid_field(self):
        """
        Test ingredient creation
        """
        data = {
            'name': ''
        }

        resp = self.client.post(INGREDIENT_URL, data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
