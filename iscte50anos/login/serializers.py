
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class SocialSerializer(serializers.Serializer):
    # Serializer which accepts an OAuth2 access token.
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(max_length=30, required=True)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True, trim_whitespace=True)
    email = serializers.EmailField()
    affiliation_name = serializers.CharField(max_length=100, required=True, trim_whitespace=True)
    affiliation_type = serializers.CharField(max_length=100, required=True, trim_whitespace=True)
    password = serializers.CharField(max_length=30, required=True)
    password_confirmation = serializers.CharField(max_length=30, required=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(max_length=30, required=True, trim_whitespace=True)
    affiliation_name = serializers.CharField(max_length=100, required=True)
    affiliation_type = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user