from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, Role, Achievement, AchievementImage


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Пароль пользователя (не менее 8 символов)."
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Подтверждение пароля."
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'confirm_password',
            'first_name', 'last_name', 'patronymic', 'role', 'bio',
            'date_of_birth', 'profile_image', 'weight_kg', 'height_cm'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        """Проверка данных."""
        if self.instance is None:  # Это создание
            if 'confirm_password' not in data:
                raise serializers.ValidationError({'confirm_password': 'Поле подтверждения пароля обязательно.'})
            if data['password'] != data.get('confirm_password'):
                raise serializers.ValidationError({'confirm_password': 'Пароли не совпадают.'})
            if not data.get('role'):
                raise serializers.ValidationError({'role': 'Роль обязательна.'})

        return data

    def create(self, validated_data):
        """Создание пользователя."""
        validated_data.pop('confirm_password')  # Удаляем подтверждение пароля
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление пользователя."""
        validated_data.pop('confirm_password', None)

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        return super().update(instance, validated_data)


class AchievementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementImage
        fields = '__all__'


class AchievementSerializer(serializers.ModelSerializer):
    images = AchievementImageSerializer(many=True, read_only=True)

    class Meta:
        model = Achievement
        fields = '__all__'
