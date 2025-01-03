from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'date_of_birth', 'patronymic']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'patronymic']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username'] # используется по умолчанию, если сортировка не указана

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        queryset = User.objects.all()
        user_id = self.request.query_params.get('id')
        if user_id is not None:
            queryset = queryset.filter(id=user_id)

        cur_filters = {
            'username': self.request.query_params.get('username'),
            'email': self.request.query_params.get('email'),
            'first_name': self.request.query_params.get('first_name'),
            'last_name': self.request.query_params.get('last_name'),
            'role': self.request.query_params.get('role'),
            'date_of_birth': self.request.query_params.get('date_of_birth'),
            'patronymic': self.request.query_params.get('patronymic'),
        }

        for field, value in cur_filters.items():
            if value:
                # Динамическое фильтрование по полям модели.
                queryset = queryset.filter(**{field: value})
        return queryset

    @action(detail=True, methods=['post'])
    def change_role(self, request, pk=None):
        """
        Кастомный метод для смены роли пользователя.
        """
        user = self.get_object()
        new_role_id = request.data.get("role_id")
        try:
            new_role = Role.objects.get(pk=new_role_id)
            user.role = new_role
            user.save()
            return Response({"detail": f"Роль пользователя {user.username} изменена на {new_role.name}."})
        except Role.DoesNotExist:
            return Response({"error": "Указанная роль не найдена."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Возвращает данные текущего пользователя.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.select_related('user').all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['user', 'date_achieved']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'date_achieved']
    ordering = ['date_achieved']

    def get_queryset(self):
        if self.action != 'list':
            return Achievement.objects.none()
        return

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

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Кастомный метод для скачивания изображения достижения.
        """
        achievement_image = self.get_object()
        return Response({"detail": f"Скачивание изображения {achievement_image.id}."})


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
