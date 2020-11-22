from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Posts
import datetime
import json
from django.core.paginator import Paginator
from django.http import JsonResponse


def index(request):
    if request.user.is_authenticated:
        
        loggedinuser=User.objects.get(username=request.user.username) 
        postslikedbyuser=loggedinuser.likes.all()
        if request.method=="POST":
            content=request.POST["content"]
            date=datetime.datetime.now()
            
            post=Posts(author=loggedinuser,content=content,date=date,totallikes=0)
            post.save()
        posts=Posts.objects.all().order_by('date')
        posts=posts[::-1]
        paginator=Paginator(posts,10)
        return render(request, "network/index.html",{"posts":paginator.get_page(request.GET.get('page')),"postliked":postslikedbyuser})
    else:
        return HttpResponseRedirect(reverse('login'))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def allposts(request):
    posts=Posts.objects.all().order_by('date')
    posts=posts[::-1]
    paginator=Paginator(posts,10)
    return render(request,"network/allposts.html",{"posts":paginator.get_page(request.GET.get('page'))})

@login_required
def profile(request,userprofile):
    #qurie to get the table of user
    use=User.objects.get(username=userprofile)
    #get all tweets of current user
    Postsofuser=use.posted.all().order_by('date')
    Postsofuser=Postsofuser[::-1]
    
    # get all users other then the user who is viewing his/her profile
    
    users=User.objects.exclude(username=userprofile)
    loggedinuser=User.objects.get(username=request.user)
    

    if request.method=="POST":
        
        #get the following list of the userprofile
        followedlist=loggedinuser.follows.all()
        flag=0
        # the user is unfollowed if name already esists.
        for follower in followedlist:
            if follower.username==use.username:
                flag=1
                loggedinuser.follows.remove(use)
                loggedinuser.save()
                break
        # else the user is followed by the  logged in user.
        if flag==0:
            loggedinuser.follows.add(use)
            loggedinuser.save()
    #count the number of followers of the user whose profile is being displayed.
    numFollowers=use.followers.all().count()
    numFollowed=use.follows.all().count()
    #check if the logged in user already followed the current viewing profile
    isfollower=loggedinuser.follows.filter(username=userprofile).exists()
    paginator=Paginator(Postsofuser,10)
    return render(request,"network/profile.html",{
        "use":use,
        "posts":paginator.get_page(request.GET.get('page')),
        "users":users,
        "numFollowers":numFollowers,
        "numFollowed":numFollowed,
        "isfollower":isfollower
        })

def following(request):
    user_current=User.objects.get(username=request.user)
    following_users=user_current.follows.all()
    postslikedbyuser=user_current.likes.all()
    posts_followed=Posts.objects.filter(author__in=following_users).order_by('date')
    posts_followed=posts_followed[::-1]
    paginator=Paginator(posts_followed,10)

    l={"user_current":user_current,"user_follows":following_users,"posts":paginator.get_page(request.GET.get('page')),"postsliked":postslikedbyuser}
    return render(request,"network/following.html",l)

def likepost(request):
    if (request.method=="POST"):
        current_user=User.objects.get(username=request.user.username)
        #get the data from ajax request
        data=json.loads(request.body)
        post_id=data['id']
        like=data['like']
        try:
            post=Posts.objects.get(pk=post_id)
        except KeyError:
            return JsonResponse({'message':"KeyError"})
        current_user.likes.remove(post)
        if like:
            current_user.likes.add(post)
        current_user.save()
        likes=post.totallikes
        if like:
            likes=post.totallikes+1
        else:
            likes=post.totallikes-1
        post.totallikes=likes
        post.save()
        return JsonResponse({
            'message':"post liked successfully","totallikes":post.totallikes
            })
    else:
       # l={"f":request.method}
        #return render(request,"network/error.html",l)
        return JsonResponse({'error':"post method required"},status=400)
    

def editpost(request,id):
    if request.method=="POST":
        
        data=json.loads(request.body)
        new_text=data['new_text']
        try:
            post=Posts.objects.get(pk=id)
        except KeyError:
            return JsonResponse({"message":"KeyError"})
        post.content=new_text
        post.date=datetime.datetime.now()
        post.save()
        
        return JsonResponse({
            "message":"post edited successfully","content":post.content,"date":post.date
            })


