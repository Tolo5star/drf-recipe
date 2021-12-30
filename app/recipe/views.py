from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe.serializers import TagSerializer, IngredientSerializer,\
    RecipeSerializer


class BaseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """
    Base view set that can be used to create and
    list objects based on serializer and queryset
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Add queryset and serializer here for the given model
    def get_queryset(self):
        """
        Return objects for the current authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """
        Create new object
        """
        serializer.save(user=self.request.user)


class TagViewSet(BaseViewSet):
    """
    Manage tags in the database
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseViewSet):
    """
    Manage Ingredients in the database
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Manage recipes in db
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Retrieve the recipes for the authenticated user
        """
        return self.queryset.filter(user=self.request.user)
