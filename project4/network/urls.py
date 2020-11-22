
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #path("newpost",views.newpost,name="newpost"),
    path("allposts",views.allposts,name="allposts"),
    path("profile/<str:userprofile>",views.profile,name="profile"),
    #path("followunfollow",views.followunfollow,name="followunfollow")
    path("following",views.following,name="following"),
    path("likepost",views.likepost,name="likepost"),
    path("editpost/<int:id>",views.editpost,name="editpost")
]
