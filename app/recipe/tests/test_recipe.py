from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """
    Returns recipe detail url for given id
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def get_sample_tag(user, name="Italian"):
    """
    Return sample tag
    """
    return Tag.objects.create(user=user, name=name)


def get_sample_ingredient(user, name="Cheese"):
    """
    Return sample ingredient
    """
    return Ingredient.objects.create(user=user, name=name)


def get_sample_recipe(user, **params):
    """
    Create and return recipe
    """
    defaults = {
        "title": "Sample Recipe",
        "time_minutes": 50,
        "price": 300.0
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class TestRecipeApiPublic(TestCase):
    """
    Test unauthenticated Recipe API
    """
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test authentication required
        """
        resp = self.client.get(RECIPE_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class TestRecipeApiPrivate(TestCase):
    """
    Test authenticated recipe API
    """
    def setUp(self) -> None:
        """
        Setup authenticated user
        """
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="password",
            name="Test"
        )
        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        """
        Test get list of recipes
        """
        resp = self.client.get(RECIPE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(resp.data, serializer.data)

    def test_recipe_returned_for_user(self):
        """
        Test that the recipes returned are only for the
        authenticated user
        """
        other_user = get_user_model().objects.create_user(
            email="other@test.com",
            password="password",
            name="Other"
        )

        get_sample_recipe(self.user, title="test")
        get_sample_recipe(other_user)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        resp = self.client.get(RECIPE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), len(serializer.data))
        self.assertEqual(resp.data, serializer.data)

    def test_recipe_detail(self):
        """
        Test recipe detail API
        """
        recipe = get_sample_recipe(user=self.user)

        recipe.tags.add(get_sample_tag(user=self.user))
        recipe.tags.add(get_sample_tag(user=self.user, name="Indian"))

        recipe.ingredients.add(get_sample_ingredient(user=self.user))
        recipe.ingredients.add(
            get_sample_ingredient(user=self.user, name="Mushroom"))

        url = detail_url(recipe.id)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(resp.data, serializer.data)