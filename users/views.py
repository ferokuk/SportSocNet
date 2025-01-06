from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, User, Achievement, AchievementImage
from .serializers import RoleSerializer, UserSerializer, AchievementSerializer, AchievementImageSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        return super().get_permissions()


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.select_related('user').all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['user', 'date_achieved']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'date_achieved']
    ordering = ['-date_achieved']

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Указание текущего пользователя как владельца достижения.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_achievements(self, request):
        """
        Возвращает достижения текущего пользователя.
        """
        achievements = Achievement.objects.filter(user=request.user)
        serializer = self.get_serializer(achievements, many=True)
        return Response(serializer.data)


class AchievementImageViewSet(viewsets.ModelViewSet):
    queryset = AchievementImage.objects.select_related('achievement').all()
    serializer_class = AchievementImageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['achievement']

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        return super().get_permissions()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Завершение сессии пользователя путем аннулирования токена.
        """
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Невалидный токен"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [AllowAny()]
        return super().get_permissions()
