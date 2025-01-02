from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Role, User, Achievement, AchievementImage
from .serializers import RoleSerializer, UserSerializer, AchievementSerializer, AchievementImageSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]


class AchievementImageViewSet(viewsets.ModelViewSet):
    queryset = AchievementImage.objects.all()
    serializer_class = AchievementImageSerializer
    permission_classes = [IsAuthenticated]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавляет токен в черный список
            return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Невалидный токен"}, status=status.HTTP_400_BAD_REQUEST)
