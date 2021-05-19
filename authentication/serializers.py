from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from django.contrib.auth.models import Group
# from notes.models import Notes, Profile


class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4),
    groups = GroupSerializer(many=True, read_only=True)
    # first_name = serializers.CharField(max_length=255, min_length=2)
    # last_name = serializers.CharField(max_length=255, min_length=2)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'groups']
        # read_only_fields = ('groups')

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user_group = Group.objects.get_or_create(name="USER")
        user_group[0].user_set.add(user)
        return user


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']
    # optional for functional based views

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')
        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                print(user)
                data["user"] = user
            else:
                msg = "Invalid credentials"
                return exceptions.ValidationError(msg)

        else:
            msg = "Please provide both username and password"
            return exceptions.ValidationError(msg)
        return data
