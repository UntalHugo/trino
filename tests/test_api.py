import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def usuario(db):
    return User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='TestPass123!'
    )


@pytest.fixture
def usuario2(db):
    return User.objects.create_user(
        username='testuser2',
        email='test2@test.com',
        password='TestPass123!'
    )


@pytest.fixture
def token(client, usuario):
    res = client.post('/api/auth/login/', {
        'username': 'testuser',
        'password': 'TestPass123!'
    }, format='json')
    return res.data['access']


# ─── TESTS DE AUTENTICACIÓN ───────────────────────────────────────

@pytest.mark.django_db
def test_registro_exitoso(client):
    res = client.post('/api/users/register/', {
        'username': 'nuevo',
        'email': 'nuevo@test.com',
        'password': 'TestPass123!',
        'password2': 'TestPass123!'
    }, format='json')
    assert res.status_code == 201


@pytest.mark.django_db
def test_login_exitoso(client, usuario):
    res = client.post('/api/auth/login/', {
        'username': 'testuser',
        'password': 'TestPass123!'
    }, format='json')
    assert res.status_code == 200
    assert 'access' in res.data
    assert 'refresh' in res.data


@pytest.mark.django_db
def test_login_fallido(client):
    res = client.post('/api/auth/login/', {
        'username': 'noexiste',
        'password': 'mal'
    }, format='json')
    assert res.status_code == 401


# ─── TESTS DE POSTS ───────────────────────────────────────────────

@pytest.mark.django_db
def test_crear_post_autenticado(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    res = client.post('/api/posts/posts/', {
        'content': 'Post de prueba'
    }, format='json')
    assert res.status_code == 201


@pytest.mark.django_db
def test_crear_post_sin_autenticar(client):
    res = client.post('/api/posts/posts/', {
        'content': 'Post sin auth'
    }, format='json')
    assert res.status_code == 401


@pytest.mark.django_db
def test_idor_no_puede_borrar_post_ajeno(client, usuario, usuario2):
    # usuario crea un post
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + client.post(
        '/api/auth/login/',
        {'username': 'testuser', 'password': 'TestPass123!'},
        format='json'
    ).data['access'])
    post_res = client.post('/api/posts/posts/', {'content': 'Post de testuser'}, format='json')
    post_id = post_res.data['id']

    # usuario2 intenta borrarlo
    token2 = client.post('/api/auth/login/', {
        'username': 'testuser2',
        'password': 'TestPass123!'
    }, format='json').data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')
    res = client.delete(f'/api/posts/posts/{post_id}/')
    assert res.status_code == 403


# ─── TESTS DE BÚSQUEDA ────────────────────────────────────────────

@pytest.mark.django_db
def test_busqueda_no_expone_email(client, token, usuario):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    res = client.get('/api/search/?q=testuser')
    assert res.status_code == 200
    for u in res.data['users']:
        assert 'email' not in u


# ─── TESTS DE COMENTARIOS ─────────────────────────────────────────

@pytest.mark.django_db
def test_comentario_post_inexistente_devuelve_404(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    res = client.post('/api/posts/9999/comments/', {
        'content': 'Comentario en post inexistente'
    }, format='json')
    assert res.status_code == 404