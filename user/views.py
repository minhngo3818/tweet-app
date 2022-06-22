from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control, never_cache # Fix logout browser back btn
from django.urls import conf
from django.db.models import Q
from .models import Profile, Tweet, Like, Comment, LikeComment
from .forms import ClientCreationForm, ProfileForm, TweetForm, CommentForm
from .utils import paginateTweet

"""USER & PROFILE FUNCTIONS"""
@never_cache
def viewHome(request):
    return render(request, 'homepage.html')

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        username = request.POST['username']
        print(username)
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, 'Username Or Password is not correct')

    return render(request, 'login-register.html', {'page': 'login'})


@login_required(login_url='login')
def userLogout(request):
    logout(request)
    return redirect('login')

def userRegister(request):
    form = ClientCreationForm()

    if request.method == 'POST':
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('edit-profile')
        else:
            messages.success(request, 'An error has occured during registration')

    context = {'page': 'register', 'form': form}
    return render(request, 'login-register.html', context)

@login_required(login_url='login')
def viewProfile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile, 'page': 'profile'})

@login_required(login_url='login')
def viewOtherProfile(request, pk):
    other_profile = Profile.objects.get(id=pk)

    context = {'other_profile': other_profile}
    return render(request, 'other-profile.html', context)

@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form':form}
    return render(request, 'edit-profile.html', context)


"""TWEET FUNCTIONS"""
@cache_control(no_store=True, no_cache=True, no_revalidate=True)
@login_required(login_url='login')
def viewTweets(request):
    form = TweetForm()
    comment_form = CommentForm()
    user = request.user

    if request.method == "POST":
        form = TweetForm(request.POST)
        tweet = form.save(commit=False)
        tweet.author = user.profile
        tweet.save()
        messages.success(request, "Your tweet was posted!")

        return redirect('tweets')   
        # Refresh the page, no copy of data within form will be replicated

    tweets = Tweet.objects.all()
    comments = Comment.objects.all()

    context = {
        'page': 'tweets',
        'form': form,
        'comment_form': comment_form,
        'tweets': tweets,
        'user': user, 
    }

    return render(request, 'tweets.html', context)

@login_required(login_url='login')
def likedTweet(request):
    profile = request.user.profile
    
    if request.method == "POST":
        tweet_id = request.POST.get('tweet_id')
        tweet = Tweet.objects.get(id=tweet_id)

        if profile != tweet.author:
            if profile in tweet.liked.all():
                tweet.liked.remove(profile)
            else:
                tweet.liked.add(profile)

        like, created = Like.objects.get_or_create(owner=profile, tweet=tweet)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
  
            else:
                like.value = 'Like'

        like.save()

    return redirect('tweets')

# Work on this function next
@login_required(login_url='login')
def editMyTweet(request, pk):
    user = request.user
    my_tweet = user.profile.tweets.get(id=pk)
    edit_form = TweetForm(instance=my_tweet)
    tweets = Tweet.objects.all()

    if request.method == 'POST':
        edit_form = TweetForm(request.POST, instance=my_tweet)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Your tweet was updated successfully!')

        return redirect('tweets')

    context = {
        'page': 'edit-my-tweet',
        'my_tweet': my_tweet,
        'edit_form': edit_form,
        'tweets': tweets,
        'user' : user,
        }

    return render(request, 'tweets.html', context)

@login_required(login_url='login')
def deleteMyTweet(request, pk):
    if request.method == 'POST':
        profile = request.user.profile
        my_tweet = profile.tweets.get(id=pk)
        my_tweet.delete()
        messages.success(request, 'Your tweet was deleted successfully')

        return redirect('tweets')
    

"""COMMENT FUNCTIONS"""
@login_required(login_url='login')
def commentTweet(request, pk):
    if request.method == 'POST':
        comment_tweet = Tweet.objects.get(id=pk)
        comment_form = CommentForm(request.POST)
        comment = comment_form.save(commit=False)
        comment.tweet = comment_tweet
        comment.author = request.user.profile
        comment.save()

        return redirect('tweets')
    # In confusion of link to tweet_id and comment_id
    # will be two cases: on Tweet and reply on Comment

@login_required(login_url='login')
def likeComment(request, pk):
    if request.method == "POST":
        profile = request.user.profile
        comment = Comment.objects.get(id=pk)
        if profile != comment.author:
            if profile in comment.liked.all():
                comment.liked.remove(profile)
            else:
                comment.liked.add(profile)

        like_comment, created = LikeComment.objects.get_or_create(owner=profile, comment=comment)
        if not created:
            if like_comment.value == 'Like':
                like_comment.value = 'Unlike'
  
            else:
                like_comment.value = 'Like'

        like_comment.save()

        return redirect('tweets')   

@login_required(login_url='login')
def editComment(request, pk):

    user = request.user
    my_comment = user.profile.comments.get(id=pk)
    edit_form = CommentForm(instance=my_comment)
    tweets = Tweet.objects.all()

    if request.method == 'POST':
        edit_form = CommentForm(request.POST, instance=my_comment)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Your comment was updated successfully!')

        return redirect('tweets')

    context = {
        'page': 'edit-my-comment',
        'my_comment': my_comment,
        'edit_form': edit_form,
        'tweets': tweets,
        'user' : user,
        }

    return render(request, 'tweets.html', context)

@login_required(login_url='login')
def deleteComment(request, pk):
    if request.method == "POST":
        profile = request.user.profile
        comment = profile.author_comment.get(id=pk)
        comment.delete()
        messages.success(request, "Your comment was deleted successfully!")

        return redirect('tweets')

@login_required(login_url='login')
def replyComment(request, pk):
    if request.method == 'POST':
        parent = Comment.objects.get(id=pk)
        reply_form = CommentForm(request.POST)
        reply = reply_form.save(commit=False)
        reply.parent = parent
        reply.author = request.user.profile
        reply.save()

        return redirect('tweets')
