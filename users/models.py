from datetime import date
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
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
    Расширенная модель пользователя.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Имя пользователя",
        help_text="Уникальное имя пользователя."
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(300))],
        verbose_name="Вес (кг)",
        help_text="Вес пользователя в килограммах."
    )
    height_cm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(300))],
        verbose_name="Рост (см)",
        help_text="Рост пользователя в сантиметрах."
    )
    role = models.ForeignKey(
        'Role',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Роль",
        help_text="Роль пользователя.",
        related_name="users",
        related_query_name="user"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Биография",
        help_text="Краткая информация о пользователе."
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения",
        help_text="Дата рождения пользователя."
    )
    patronymic = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Отчество",
        help_text="Отчество пользователя (необязательно)."
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        verbose_name="Изображение профиля",
        help_text="Аватар пользователя.",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Дата регистрации"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    def calculate_age(self):
        """Вычисляет возраст пользователя."""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def calculate_bmi(self):
        """Вычисляет индекс массы тела (BMI)."""
        if self.weight_kg and self.height_cm:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m ** 2), 2)
        return None

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.username = self.username.lower()
        super().save(*args, **kwargs)


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
