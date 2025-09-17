from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, Save
from .models import Post


# Create your views here.
@login_required(login_url="login")
def home (request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() # saves user in auth_user table
            login(request, user) # auto login after signup
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def save(request):
    if request.method == "POST":
        form = Save(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            post.creator = request.user
            post.save()
            return redirect("post",id=post.id)
    else:
        form = Save()
    return render(request, "save.html", {"form": form})


@login_required
def update_post(request,id):
    post = get_object_or_404(Post, id=id, creator = request.user)
    if request.method == "POST":
        form = Save(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect("post",id=post.id)
    else:
        form = Save(instance=post)
    return render(request, "update_post.html", {"form": form, "post":post})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, creator=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(request, "post.html", {"post": post})


def post(request,id):
    post = get_object_or_404(Post,id=id)
    return render(request, "post.html", {"post":post})

@login_required
def posts(request):
    posts = Post.objects.filter(creator=request.user)
    return render(request, 'posts.html', {"posts": posts})
