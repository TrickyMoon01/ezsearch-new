from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, Save
from .models import Post
import requests
import os
from dotenv import load_dotenv
load_dotenv()


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


results=[]
def search(request):
    global results
    if request.method == "POST" and "save" in request.POST:
        title = request.POST.get("title")
        url = request.POST.get("url")
        print(url)
        description = request.POST.get("description")
        Post.objects.create(title=title, url=url, text=description, creator=request.user)
        return render(request, "search.html", {"results":results})

    if request.method == "POST":
        query=request.POST.get("q")
        response=requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": os.environ.get("BRAVE_API")
            },
            params={
                "q": query,
                "count": 20,
                "country": "us",
                "search_lang": "en",
            },
        )
        if response.status_code==200:
            data=response.json()
            results=data.get("web", {}).get("results", [])
    return render(request, "search.html", {"results":results})