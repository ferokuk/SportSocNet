from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.views import RoleViewSet, UserViewSet, AchievementViewSet, AchievementImageViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'achievement-images', AchievementImageViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
