from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework import serializers
from users.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=CustomUser.UserType)

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'username', 'password', 'email', 'user_type', 'company_name')
        read_only_fields = ('id',)

    def validate(self, attrs):
        user_type = attrs.get('user_type')
        company_name = attrs.get('company_name')
        if user_type == CustomUser.UserType.PRIVATE and not company_name:
            raise serializers.ValidationError("Enter campaign name")
        return attrs


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
            'full_name', 'username', 'email', 'first_name', 'last_name', 'phone_number',
            'telegram_id',
            'tg_username')
