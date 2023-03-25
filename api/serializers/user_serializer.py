from rest_framework import serializers
from webapp.models.user import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"  # ("username", "first_name", "last_name", "phone", "email")


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    phone = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("username", "email", 'phone', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            password=self.validated_data['password']
        )
        user.save()
        return user
