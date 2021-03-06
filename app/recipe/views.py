from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe.serializers import TagSerializer, IngredientSerializer,\
    RecipeSerializer, RecipeDetailSerializer, RecipeImageSerializer


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

    def get_serializer_class(self):
        """
        return appropriate serializer class
        """
        # for api detail view
        if self.action == 'retrieve':
            return RecipeDetailSerializer

        if self.action == 'upload_image':
            return RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create new recipe , assign the authenticated user
        """
        serializer.save(user=self.request.user)

    @action(methods=["GET", "POST"], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """
        Endpoint to upload image to recipe
        detail=True as we want to update specific recipe
        """
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
