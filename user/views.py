from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control, never_cache # Fix logout browser back btn
from django.urls import conf
from .models import Profile, Tweet, Like
from .forms import ClientCreationForm, ProfileForm, TweetForm

# Create your views here.
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
    return render(request, 'profile.html', {'profile': profile})

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

@cache_control(no_store=True, no_cache=True, no_revalidate=True)
@login_required(login_url='login')
def viewTweet(request):
    page = 'tweets'
    form = TweetForm()
    user = request.user

    if request.method == "POST":
        form = TweetForm(request.POST)
        tweet = form.save(commit=False)
        tweet.author = request.user.profile
        tweet.save()
        messages.success(request, "Your tweet was posted!")

        return redirect('tweets')   
        # Refresh the page, no copy of data within form will be replicated

    tweets = Tweet.objects.all()
    context = {
        'form': form,
        'tweets': tweets,
        'user': user,
        'page': page
    }

    return render(request, 'tweets.html', context)

@login_required(login_url='login')
def likedTweet(request):
    profile = request.user.profile
    
    if request.method == "POST":
        tweet_id = request.POST.get('tweet_id')
        tweet = Tweet.objects.get(id=tweet_id)

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



