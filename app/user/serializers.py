from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the users object
    """
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # Add properties for password
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """
        Create new user with encrypted password (done in user manager)
        and return it,
        overwriting create to use our custom user manager instead of default
        """
        return get_user_model().objects.create_user(**validated_data)
