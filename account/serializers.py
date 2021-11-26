from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.views import APIView

from account.models import MyUser
from account.utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    repeat_password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'repeat_password')

    def validate(self, validated_data):
        password = validated_data.get('password')
        repeat_password = validated_data.get('repeat_password')
        if password != repeat_password:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                message = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = "Must include 'email' and 'password'!"
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs




