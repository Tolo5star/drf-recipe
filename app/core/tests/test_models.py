from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag, Ingredient, Recipe, recipe_image_file_path


def get_sample_user(email='test@test.com', password='password'):
    """
    Create sample user for testing
    """
    return get_user_model().objects.create_user(email=email, password=password)


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

    def test_new_user_invalid_email(self):
        """
        Test user creation without email provided results in error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="test_password"
            )

    def test_create_superuser_with_create_staff_true(self):
        """
        Test creating new superuser
        """
        email = "test@UPPERCASE.com"
        password = "test_password"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """
        Test Tag string representation
        """
        tag = Tag.objects.create(
            user=get_sample_user(),
            name="Italian"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """
        Test Ingredient string representation
        """
        ing = Ingredient.objects.create(
            user=get_sample_user(),
            name="Potato"
        )

        self.assertEqual(str(ing), ing.name)

    def test_recipe_str(self):
        """
        Test the recipe str representation
        """
        recipe = Recipe.objects.create(
            user=get_sample_user(),
            title="Butter Chicken",
            time_minutes=50,
            price=300.0
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_gen(self, mock_uuid):
        """
        Test that image is saved with generated file_name
        and corresponding location
        """
        uuid = "test_uuid"
        mock_uuid.return_value = uuid
        file_path = recipe_image_file_path(instance=None, file_name="test_image.jpg")
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
