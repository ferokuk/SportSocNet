from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from users.views import RoleViewSet, UserViewSet, AchievementViewSet, AchievementImageViewSet, LogoutView
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
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include(router.urls)),
    path('api/v1/get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/v1/delete_token/', LogoutView.as_view(), name='token_delete'),
    path('api/v1/get_token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
