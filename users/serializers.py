from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _

class UserRegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=CustomUser.UserType)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'username','phone_number', 'password', 'email', 'user_type', 'company_name')
        read_only_fields = ('id',)

    def validate(self, attrs):
        user_type = attrs.get('user_type')
        company_name = attrs.get('company_name')
        if user_type == CustomUser.UserType.PRIVATE and not company_name:
            raise serializers.ValidationError("Enter campaign name")
        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number', 'password')

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        if phone_number and password:
            try:
                user = CustomUser.objects.filter(phone_number=phone_number).last()
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(_("Invalid phone number or password"))
            if user and check_password(password, user.password):
                return user

        else:
            msg = _("You must provide a phone number and password.")
            raise serializers.ValidationError(msg, code='authorization')
        msg = _("Incorrect phone number or password")
        raise serializers.ValidationError(msg, code='authorization')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'full_name', 'username', 'email', 'first_name', 'last_name', 'phone_number',
            'telegram_id',
            'tg_username')
