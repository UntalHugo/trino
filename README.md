# 🐦 Trino — Red Social tipo Twitter

Proyecto final de Programación V. API REST completa con autenticación JWT, publicaciones, interacciones sociales y vista web estilo Twitter.

---

## 🛠️ Tecnologías

- Python 3.12 + Django 5.2
- Django REST Framework + SimpleJWT
- PostgreSQL 16
- Redis 7
- Cloudinary (imágenes)
- Docker + Docker Compose
- pytest-django (tests automatizados)

---

## 🚀 Levantar el proyecto con Docker

### 1. Clonar el repositorio
```bash
git clone https://github.com/UntalHugo/trino.git
cd trino
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
```
Completar el `.env` con tus credenciales reales (Cloudinary, Google OAuth, etc).

### 3. Levantar todo el stack
```bash
docker compose up --build
```

### 4. Aplicar migraciones
```bash
docker compose exec web python manage.py migrate
```

### 5. Crear superusuario
```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Abrir en el navegador
- Feed: http://localhost:8000/feed/
- Admin: http://localhost:8000/admin/

---

## 🔒 Seguridad implementada

- Autenticación JWT con blacklist (logout real)
- Permiso `IsOwnerOrReadOnly` — usuarios no pueden modificar contenido ajeno
- Rate limiting: 20 req/hora anónimos, 200 req/hora autenticados
- Email no expuesto en búsqueda pública
- Headers de seguridad HTTPS en producción
- CORS configurado con orígenes explícitos
- Credenciales en variables de entorno, nunca en el código

---

## 🌐 Modo producción

```bash
cp .env.prod.example .env.prod
```
Completar `.env.prod` con `DEBUG=False` y una `SECRET_KEY` segura.

```bash
docker compose -f docker-compose.prod.yml up --build
```

---

## 📦 Servicios Docker

| Servicio | Imagen | Puerto |
|----------|--------|--------|
| web | Python 3.12-slim | 8000 |
| db | PostgreSQL 16 | interno |
| redis | Redis 7 Alpine | interno |

---

## 📡 Endpoints principales

| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| POST | /api/users/register/ | No | Registro de usuario |
| POST | /api/auth/login/ | No | Login → access + refresh token |
| POST | /api/auth/refresh/ | No | Renovar access token |
| POST | /api/auth/logout/ | JWT | Logout (blacklist token) |
| GET/PATCH | /api/users/profile/ | JWT | Ver/editar perfil propio |
| POST | /api/users/follow/\<username\>/ | JWT | Seguir/dejar de seguir |
| GET | /api/posts/posts/ | JWT | Listar posts |
| POST | /api/posts/posts/ | JWT | Crear post |
| GET | /api/posts/posts/feed/ | JWT | Feed personalizado paginado |
| POST | /api/posts/\<id\>/like/ | JWT | Toggle like |
| GET/POST | /api/posts/\<id\>/comments/ | JWT | Ver/crear comentarios |
| GET | /api/messages/ | JWT | Mensajes directos |
| GET | /api/notifications/ | JWT | Ver notificaciones |
| GET | /api/search/?q=texto | JWT | Buscar posts, usuarios, hashtags |

---

## 🧪 Tests

```bash
pytest tests/test_api.py -v
```

Cubre: registro, login, creación de posts, permisos IDOR, búsqueda sin emails, comentarios con post inexistente.

---

## 👥 Equipo

| Persona | Contribuciones |
|---------|----------------|
| Hugo | Modelo User, JWT, registro, perfil, follow/unfollow, CRUD posts, feed, hashtags, menciones, upload imágenes, seguridad (9 fixes), tests automatizados |
| Tobias | Docker, PostgreSQL, Redis, likes, comentarios, mensajes, notificaciones, búsqueda, OAuth Google/GitHub, templates frontend |