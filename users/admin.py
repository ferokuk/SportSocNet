from django.contrib import admin
from .models import Role, User, Achievement, AchievementImage


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Админка для модели Role.
    """
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админка для модели User.
    """
    list_display = ('id', 'username', 'email', 'last_name', 'first_name', 'role', 'date_of_birth', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {
            'fields': (
                'username', 'password', 'email', 'last_name', 'first_name', 'patronymic', 'role', 'bio',
                'profile_image',
                'date_of_birth')
        }),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Даты', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """
    Админка для модели Achievement.
    """
    list_display = ('id', 'title', 'user', 'date_achieved')
    list_filter = ('date_achieved',)
    search_fields = ('title', 'user__username')
    ordering = ('-date_achieved',)
    autocomplete_fields = ('user',)


@admin.register(AchievementImage)
class AchievementImageAdmin(admin.ModelAdmin):
    """
    Админка для модели AchievementImage.
    """
    list_display = ('id', 'achievement', 'image', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('achievement__title',)
    ordering = ('-uploaded_at',)


