from rest_framework import serializers
from .models import User, Role, Achievement, AchievementImage


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'date_of_birth', 'bio', 'profile_image', 'last_name', 'first_name',
                  'patronymic']


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'


class AchievementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementImage
        fields = '__all__'
