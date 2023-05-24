from pyexpat import model
from rest_framework import serializers
# from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from .models import CustomUser



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', "username", "password", "first_name",
                  "last_name", "email", 'station']  # Add other fields as needed
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': True},
            'username': {'required': True},
            "station":{'required': True}
        }

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

        
# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "password", "first_name", 'station',
                  "last_name", "email")
        extra_kwargs = {
            "username": {'required': True}, 
            "password": {'required': True}, 
            "first_name": {'required': True},
            "email": {'required': True}, 
            'confirm_password'
            "password": {"write_only": True},
            "station":{'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            station=validated_data["station"],
            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validators.validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        return value

    def validate_username(self, value):
        user = self.context["request"].user
        if CustomUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."}
            )
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]

        instance.save()

        return instance


