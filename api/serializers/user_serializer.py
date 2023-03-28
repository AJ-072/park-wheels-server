from rest_framework import serializers
from webapp.models.user import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class LoginCredentialSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    phone = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'updated_at',
            'date_joined',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'id'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        user.save()
        return user
