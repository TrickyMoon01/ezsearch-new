"""
URL configuration for ezsearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from main_app import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register_view, name="register"),
    path("new_post/", views.save, name="new_post"),
    path("posts/", views.posts, name="posts"),
    path("posts/<int:id>/", views.post, name="post"),
    path("posts/<int:id>/edit/", views.update_post, name="update_post"),
    path("posts/<int:id>/delete/", views.delete_post, name="delete_post"),
    path("search/", views.search, name="search")
]