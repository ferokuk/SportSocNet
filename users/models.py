from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """
    Модель роли пользователя.
    """
    name = models.CharField(max_length=50, help_text="Название роли", verbose_name="Название роли")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Модель пользователя.
    """
    role = models.ForeignKey(Role, max_length=50, help_text="Роль", verbose_name="Роль", null=True, # TODO NULL=FALSE
                             on_delete=models.PROTECT)
    bio = models.TextField(blank=True, null=True, help_text="Биография", verbose_name="Биография")
    date_of_birth = models.DateField(null=True, help_text="Дата рождения", verbose_name="Дата рождения") # TODO NULL=FALSE
    patronymic = models.CharField(max_length=100, blank=True, null=True, help_text="Отчество (необязательно)",
                                  verbose_name="Отчество")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True,
                                      help_text="Изображение профиля", verbose_name="Изображение профиля")
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


    def __str__(self):
        return self.username


class Achievement(models.Model):
    """
    Модель достижения пользователя.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="achievements",
        verbose_name="Пользователь"
    )
    title = models.CharField(max_length=100, verbose_name="Название достижения")
    description = models.TextField(blank=True, verbose_name="Описание достижения")
    date_achieved = models.DateField(null=True, blank=True, verbose_name="Дата достижения")

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class AchievementImage(models.Model):
    """
    Модель изображения для достижения.
    """
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Достижение"
    )
    image = models.ImageField(upload_to="achievements/", verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    class Meta:
        verbose_name = "Изображение достижения"
        verbose_name_plural = "Изображения достижений"

    def __str__(self):
        return f"Изображение для {self.achievement.title}"
