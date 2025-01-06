from datetime import date
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User, Role, Achievement, AchievementImage


@pytest.mark.django_db
def test_role_creation():
    role = Role.objects.create(name='Admin')

    assert role.name == 'Admin'
    assert str(role) == 'Admin'


@pytest.mark.django_db
def test_user_creation():
    role = Role.objects.create(name='Admin')
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword',
        role=role,
        date_of_birth=date(1990, 5, 15),
        weight_kg=70,
        height_cm=175
    )

    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.role.name == 'Admin'


@pytest.mark.django_db
def test_user_calculate_age():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword',
        date_of_birth=date(1990, 5, 15)
    )

    assert user.calculate_age() == 34  # Текущий год - 2025, возраст будет 34 года


@pytest.mark.django_db
def test_user_calculate_bmi():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword',
        weight_kg=70,
        height_cm=175
    )

    assert user.calculate_bmi() == 22.86  # Рассчитываем BMI для 70 кг и 175 см


@pytest.mark.django_db
def test_achievement_creation():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    achievement = Achievement.objects.create(
        user=user,
        title='First Login',
        description='User logged in for the first time.',
        date_achieved=date(2024, 1, 7)
    )

    assert achievement.title == 'First Login'
    assert achievement.description == 'User logged in for the first time.'
    assert achievement.user.username == 'testuser'
    assert achievement.date_achieved == date(2024, 1, 7)
    assert str(achievement) == 'First Login (testuser)'


@pytest.mark.django_db
def test_achievement_image_creation():
    achievement = Achievement.objects.create(
        user=User.objects.create_user(username='testuser', email='test@example.com', password='testpassword'),
        title='First Login',
        description='User logged in for the first time.',
        date_achieved=date(2024, 1, 7)
    )

    image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    achievement_image = AchievementImage.objects.create(
        achievement=achievement,
        image=image_file
    )

    assert achievement_image.image.name.startswith('achievements/')
    assert achievement_image.achievement.title == 'First Login'
    assert str(achievement_image) == 'Изображение для First Login'
