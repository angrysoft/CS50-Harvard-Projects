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
    path("post", views.PostView.as_view(), name="post_by_id"),
    path("likes/<int:post_id>", views.likes, name="likes"),
    path("post/<int:post_id>", views.PostView.as_view(), name="post_by_id"),
    path("posts", views.Posts.as_view(), name="posts"),
    path(
        "posts/<str:filter_name>/<str:filter_arg>", views.Posts.as_view(), name="posts"
    ),
    path("following", views.following, name="following"),
]
