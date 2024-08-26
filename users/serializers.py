from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework import serializers

from users.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=CustomUser.UserType.choices)
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'username', 'password', 'email', 'user_type')
        read_only_fields = ('id',)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = CustomUser.objects.filter(Q(username=username) |
                                             Q(email=username)).first()
            if user and check_password(password, user.password):
                return user

        else:
            msg = "Должно включать 'username_or_email' и 'password'"
            raise serializers.ValidationError(msg, code='authorization')
        msg = "Неверное имя пользователя или пароль"
        raise serializers.ValidationError(msg, code='authorization')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
        'id', 'full_name', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'telegram_id',
        'tg_username')
