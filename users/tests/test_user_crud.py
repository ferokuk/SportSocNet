from django.urls import reverse
from icecream import ic
from rest_framework import status
import pytest
from rest_framework.test import APIClient

from users.models import User, Role


@pytest.mark.django_db
def test_create_user():
    client = APIClient()
    url = reverse('users-list')  # URL для создания пользователя
    role = Role.objects.create(name='Admin')
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'date_of_birth': '1990-05-15',
        'role': role.id,  # Предположим, что роль с ID = 1 существует
    }

    response = client.post(url, data, format='json')
    ic(response.data)
    assert response.status_code == status.HTTP_201_CREATED  # Ожидаем статус 201
    assert response.data['username'] == 'newuser'
    assert response.data['email'] == 'newuser@example.com'


@pytest.mark.django_db
def test_get_users_list():
    client = APIClient()

    # Создадим пользователя для теста
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123',
    )

    url = reverse('users-list')  # URL для получения списка пользователей
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0  # Ожидаем, что список не пуст
    assert response.data[0]['username'] == user.username


@pytest.mark.django_db
def test_get_user_detail():
    client = APIClient()

    # Создаем пользователя для теста
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123',
    )
    # Получаем JWT-токен для пользователя
    token_url = reverse('token_obtain_pair')
    token_response = client.post(token_url, {'username': 'testuser', 'password': 'password123'}, format='json')

    assert token_response.status_code == status.HTTP_200_OK  # Убедимся, что токен успешно получен

    access_token = token_response.data['access']

    # Устанавливаем токен в заголовок Authorization
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('users-detail', args=[user.id])  # URL для получения информации о пользователе
    response = client.get(url)
    ic(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == user.username
    assert response.data['email'] == user.email


@pytest.mark.django_db
def test_update_user():
    client = APIClient()

    # Создаем пользователя для теста
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123',
        role=Role.objects.create(name='Admin'),
    )

    # Логинимся как этот пользователь
    client.force_authenticate(user=user)

    url = reverse('users-detail', args=[user.id])  # URL для обновления данных пользователя
    data = {
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'password': 'newpassword123',
    }

    response = client.put(url, data, format='json')
    ic(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == 'updateduser'
    assert response.data['email'] == 'updateduser@example.com'


@pytest.mark.django_db
def test_delete_user():
    client = APIClient()

    # Создаем пользователя для теста
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123',
    )

    # Логинимся как этот пользователь
    client.force_authenticate(user=user)

    url = reverse('users-detail', args=[user.id])  # URL для удаления пользователя

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT  # Ожидаем статус 204 (удаление прошло успешно)

    # Проверим, что пользователь удален из базы данных
    assert not User.objects.filter(id=user.id).exists()
