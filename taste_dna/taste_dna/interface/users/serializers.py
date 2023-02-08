# django imports
from rest_framework import serializers
from taste_dna.domain.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "date_joined"]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, required=True)
