from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tag object
    """

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for Ingredient object
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serialize a Recipe
    """
    # we use objects.all() to give list of ids
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags',
                  'time_minutes', 'price', 'link')
        read_only = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """
    Serialize the recipe details
    """
    # Pass the objects to their respective serializers
    ingredients = IngredientSerializer(
        many=True,
        read_only=True
    )

    tags = TagSerializer(
        many=True,
        read_only=True
    )


class RecipeImageSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading images to recipe
    """
    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
