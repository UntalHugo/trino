from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm  # Importamos el formulario que acabamos de crear

@login_required
def home_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) # request.FILES es clave para la imagen
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Vinculamos el post automáticamente al usuario logueado
            post.save()
            return redirect('home')  # Recargamos la página para ver el post nuevo
    else:
        form = PostForm()

    posts = Post.objects.all()
    
    context = {
        'posts': posts,
        'form': form  # Le pasamos el formulario al HTML
    }
    return render(request, 'home.html', context)