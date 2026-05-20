from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  # Columnas que verás en la lista
    search_fields = ('title', 'content', 'user__username')  # Buscador inteligente
    list_filter = ('created_at',)  # Filtro lateral por fecha