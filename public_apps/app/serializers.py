from rest_framework import serializers
from .models import CustomUsers
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ["email", "password"]

    def save(self):
        pas = self.validated_data["password"]
        if CustomUsers.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "This email already exits!"})
        user = CustomUsers.objects.create(email=self.validated_data["email"])
        user.set_password(pas)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials.", code="authorization"
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code="authorization"
            )

        attrs["user"] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUsers
        fields = [
            "id",
            "email",
            "first_name",
            "last_name"
        ]