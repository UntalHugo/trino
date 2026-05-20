from django.db import models
from django.conf import settings  # Esto es clave para apuntar a tu usuario personalizado

class Post(models.Model):
    # Conectamos el post con el usuario. Si el usuario se borra, se borran sus posts (CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    title = models.CharField(max_length=255, verbose_name="Título")
    content = models.TextField(verbose_name="Contenido")
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="Imagen del Post")
    
    # Fechas automáticas para saber cuándo se creó y cuándo se editó
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        ordering = ['-created_at']  # Esto hace que los posts más nuevos salgan primero
        verbose_name = "Publicación"
        verbose_name = "Publicaciones"

    def __str__(self):
        return f"{self.user.username} - {self.title[:20]}"