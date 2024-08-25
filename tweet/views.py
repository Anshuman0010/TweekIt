from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetFrom,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def index(request):
    return render(request, 'index.html', {'Tweet' : Tweet})

def tweet_list(request):
    tweets = Tweet.objects.all()
    return render(request, 'tweet_list.html', {'tweets' : tweets})
@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetFrom(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetFrom()
    return render(request, 'tweet_form.html', {'form' : form})
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk= tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetFrom(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetFrom(instance=tweet)
    return render(request, 'tweet_form.html', {'form' : form})
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet':tweet})
    
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form' : form})


def login_req(request):
    return render(request, 'registration/login.html', {'form' : form})

def logout(request):
    return render(request, 'registration/logout.html', {'form' : form})