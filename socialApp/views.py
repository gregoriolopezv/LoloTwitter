from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PostForm
from django.contrib.auth.decorators import login_required

# feed o inicio
def feed(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'socialApp/feed.html', context)

#registrar usuario
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado exitosamente!')
            return redirect('feed')
    else:
         form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, 'socialApp/register.html', context)

#vista Posteo
@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, 'post enviado!')
            return redirect('feed')
    else:
         form = form=PostForm()
    return render(request, 'socialApp/post.html', {'form': form})

#perfil 
def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        user = User.objects.get(username=username)
        posts = current_user.posts.all()
    
    return render(request, 'socialApp/profile.html', context = {'user': user, 'posts': posts})

def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'sigues a {username}')
    return redirect('profile', username)


def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'dejaste de seguir a a {username}')
    return redirect('profile', username)