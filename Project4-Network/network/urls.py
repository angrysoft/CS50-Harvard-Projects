from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path(
        "user_profile/<str:username>", views.UserProfile.as_view(), name="user_profile"
    ),
    path("posts", views.Posts.as_view(), name="posts"),
    path(
        "posts/<str:filter_name>/<str:filter_arg>", views.Posts.as_view(), name="posts"
    ),
    path("following", views.following, name="following"),
]
