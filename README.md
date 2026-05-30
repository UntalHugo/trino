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

- API: http://localhost:8000/api/
- Feed: http://localhost:8000/feed/
- Admin: http://localhost:8000/admin/

---

## 🏭 Modo producción

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
| web | Python 3.12-slim + Gunicorn | 8000 |
| db | PostgreSQL 16 | 5432 |
| redis | Redis 7 Alpine | 6379 |

---

## 📡 Endpoints principales

| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| POST | /api/auth/login/ | No | Login JWT |
| POST | /api/users/register/ | No | Registro |
| GET | /api/users/profile/ | JWT | Ver perfil |
| PATCH | /api/users/profile/ | JWT | Editar perfil |
| POST | /api/users/follow/\<username\>/ | JWT | Seguir/dejar de seguir |
| GET | /api/posts/feed/ | JWT | Feed personalizado |
| POST | /api/posts/ | JWT | Crear post |
| POST | /api/posts/\<id\>/like/ | JWT | Like toggle |
| GET | /api/search/?q=texto | JWT | Búsqueda global |

---

## 👥 Equipo

| Persona | Rol |
|---------|-----|
| Tobias | Backend, Docker, OAuth, Posts, Interactions |
| Hugo | Tests, PRs, README |